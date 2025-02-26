# from typing import List
import hashlib
import hmac
import json
from rest_framework.generics import ListAPIView
import uuid
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from orders.models import Item, Order, PaymentAccountModel, PaymentMethodModel , Links
# from orders.api.serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
# from orders.forms.order import ItemsForm, OrderForm
from paymob.dataclasses import BillingData, Intention, PaymentIntention
# from products.models import Product
from paymob.client import PaymobIntentionClient 
from paymob.client import Item as IntentionItem 
from django.shortcuts import get_object_or_404
from orders.api.serializers import PaymentMethodSerializer
import logging

# Get logger instance
logger = logging.getLogger(__name__)



class PaymentMethodsList(ListAPIView):
    queryset = PaymentMethodModel.objects.all()
    serializer_class = PaymentMethodSerializer

class ItemAdaptor:
    def __new__(cls,item:Item):
        product = item.product
        return IntentionItem(
            name=product.name if len(product.name) < 40 else product.name[:40],
            amount=product.price * item.quantity ,
            description=product.description if len(product.description) < 50 else product.description[:50],
            quantity=item.quantity
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_link(request:Request):

    # check order_uuid is exist if not return 400 bad request
    order_uuid= request.query_params.get("order_uuid",None)
    if not order_uuid :
        return Response({"detail":" order_uuid field required"},status.HTTP_400_BAD_REQUEST)

    # check payment_id is exist if not return 400 bad request
    payment_method_id= request.query_params.get("payment_method_id",None)
    if not payment_method_id :
        return Response({"detail":" payment_method_id field required"},status.HTTP_400_BAD_REQUEST)
    
    # check Paymob account that in database is exist if not return 400 bad request
    pay_acc = PaymentAccountModel.objects.filter(take=True).first()
    if not pay_acc :
        return Response({"detail":"no Account to pay with in paymob"},status.HTTP_400_BAD_REQUEST)

    order = get_object_or_404(Order, order_uuid=order_uuid)
    method = get_object_or_404(PaymentMethodModel, pk=payment_method_id , account=pay_acc)

    items = order.item_set.all()

    payment = PaymobIntentionClient(pay_acc.secret_key,pay_acc.public_key)

    special_reference = uuid.uuid4()

    if order.is_online_payment : 
        price = int(order.total_price)
        items = [ItemAdaptor(item) for item in items]
        items = items + [
                IntentionItem(
                    name="خدمة التوصيل",
                    amount=order.delivery_price ,
                    description="دفع خدمة التوصيل ",
                    quantity=1
                        )

        ]
    elif order.is_cash_payment :
        price = int(order.delivery_price)
        items = [
                IntentionItem(
                    name="خدمة التوصيل",
                    amount=order.delivery_price ,
                    description="دفع خدمة التوصيل فقط و باقى المبلغ عند الاستلام",
                    quantity=1
                        )
            ]
    else :
        return Response({"detail":"no payment type defined"},status.HTTP_400_BAD_REQUEST)

    intention = payment.create_intention(Intention(
            amount=price,
            payment_methods=[
                method.payment_method_id
            ],
            items=items,
            special_reference=str(special_reference),
            billing_data=BillingData(
                first_name = request.user.first_name if request.user.first_name else request.user.phone_number,
                last_name= request.user.last_name if request.user.last_name else request.user.phone_number,
                phone_number=request.user.phone_number,
                email= request.user.email,
                apartment=order.apartment,
                building=order.building,
                city=order.district,
                country=order.country.name if order.country else order.district ,
                floor=order.floor,
                street=order.street,

            ),

            notification_url=pay_acc.notification_url,
            redirection_url=pay_acc.redirection_url 
            ))
    
    new_link = Links(
        order = order,
        special_reference = str(special_reference),
        price=price , 
        payemnt_method=method,
    )
    
    if isinstance(intention,PaymentIntention):
        new_link.client_secret = intention.client_secret,
        url = payment.get_payment_url(intention.client_secret)
        new_link.payment_link = url
        new_link.paymob_order_id = intention.intention_order_id
        new_link.price = float(intention.intention_detail.amount) /100
        new_link.save()
        return Response({"url":url})
    else :
        new_link.save()
        return Response({"detail":intention.errors})




def extract_keys(data:dict):
    print(data)
    return {
        "amount_cents":data.get("amount_cents"),
        "created_at":data.get("created_at"),
        "currency":data.get("currency"),
        "error_occured":data.get("error_occured"),
        "has_parent_transaction":data.get("has_parent_transaction"),
        "id":data.get("id"),
        "integration_id":data.get("integration_id"),
        "is_3d_secure":data.get("is_3d_secure"),
        "is_auth":data.get("is_auth"),
        "is_capture":data.get("is_capture"),
        "is_refunded":data.get("is_refunded"),
        "is_standalone_payment":data.get("is_standalone_payment"),
        "is_voided":data.get("is_voided"),
        "order":data.get("order").get("id"),
        "owner":data.get("owner"),
        "pending":data.get("pending"),
        "source_data.pan":data.get("source_data").get("pan"),
        "source_data.sub_type":data.get("source_data").get("sub_type"),
        "source_data.type":data.get("source_data").get("type"),
        "success":data.get("success"),
    }

def generate_hmac(data:dict,hmac_key:str):
    keys_vals = extract_keys(data)
    raw_string =  "".join([json.dumps(val).replace('"','') for val in keys_vals.values()])
    return hmac.new(
        hmac_key.encode("utf-8"),
        raw_string.encode("utf-8"),
        hashlib.sha512
    ).hexdigest() 


@api_view(['GET',"POST"])
def payment_status(request:Request):
    recive_hmac = request.query_params.get("hmac",None)
    data = request.data.get("obj")
    account_hmac = PaymentAccountModel.objects.filter(take=True).first()
    # print(f"\n{recive_hmac}\n{data}\n{account_hmac}")
    if account_hmac and recive_hmac:
        gen_hmac = generate_hmac(data,account_hmac.hmac_key)
        print(f"\n{gen_hmac}\n{recive_hmac}\n{data.get('order',{}).get('id',{})}")
        if gen_hmac == recive_hmac:
            link = get_object_or_404(Links, paymob_order_id=data.get("order",{}).get("id",{}))
            success = data.get("success",False)
            link.is_paid = success
            order = link.order
            if order.is_cash_payment :
                if order.delivery_price == link.price :
                    order.is_delivery_paid = success
            elif order.is_online_payment :
                if order.total_price == link.price :
                    order.is_paid = success

            order.save()
            link.save()
            print("success")
            return Response({"detail":"success"})
        print("faild")
    return Response({"detail":"no account to pay with in paymob"},status.HTTP_400_BAD_REQUEST)
    # {
    # "type": "TRANSACTION",
    # "obj": {
    #     "id": 192036465,
    #     "pending": false,
    #     "amount_cents": 100000,
    #     "success": true,
    #     "is_auth": false,
    #     "is_capture": false,
    #     "is_standalone_payment": true,
    #     "is_voided": false,
    #     "is_refunded": false,
    #     "is_3d_secure": true,
    #     "integration_id": 4097558,
    #     "profile_id": 164295,
    #     "has_parent_transaction": false,
    #     "order": {
    #         "id": 217503754,
    #         "created_at": "2024-06-13T11:32:09.628623",
    #         "delivery_needed": false,
    #         "merchant": {
    #             "id": 164295,
    #             "created_at": "2022-03-24T21:13:47.852384",
    #             "phones": [
    #                 "+201024710769"
    #             ],
    #             "company_emails": [
    #                 "mohamedabdelsttar97@gmail.com"
    #             ],
    #             "company_name": "Parmagly",
    #             "state": "",
    #             "country": "AED",
    #             "city": "DUBAI",
    #             "postal_code": "",
    #             "street": ""
    #         },
    #         "collector": null,
    #         "amount_cents": 100000,
    #         "shipping_data": {
    #             "id": 108010028,
    #             "first_name": "dumy",
    #             "last_name": "dumy",
    #             "street": "dumy",
    #             "building": "dumy",
    #             "floor": "dumy",
    #             "apartment": "sympl",
    #             "city": "dumy",
    #             "state": "dumy",
    #             "country": "UAE",
    #             "email": "dumy@dumy.com",
    #             "phone_number": "+201125773493",
    #             "postal_code": "NA",
    #             "extra_description": "",
    #             "shipping_method": "UNK",
    #             "order_id": 217503754,
    #             "order": 217503754
    #         },
    #         "currency": "AED",
    #         "is_payment_locked": false,
    #         "is_return": false,
    #         "is_cancel": false,
    #         "is_returned": false,
    #         "is_canceled": false,
    #         "merchant_order_id": null,
    #         "wallet_notification": null,
    #         "paid_amount_cents": 100000,
    #         "notify_user_with_email": false,
    #         "items": [],
    #         "order_url": "NA",
    #         "commission_fees": 0,
    #         "delivery_fees_cents": 0,
    #         "delivery_vat_cents": 0,
    #         "payment_method": "tbc",
    #         "merchant_staff_tag": null,
    #         "api_source": "OTHER",
    #         "data": {}
    #     },
    #     "created_at": "2024-06-13T11:33:44.592345",
    #     "transaction_processed_callback_responses": [],
    #     "currency": "AED",
    #     "source_data": {
    #         "pan": "2346",
    #         "type": "card",
    #         "tenure": null,
    #         "sub_type": "MasterCard"
    #     },
    #     "api_source": "IFRAME",
    #     "terminal_id": null,
    #     "merchant_commission": 0,
    #     "installment": null,
    #     "discount_details": [],
    #     "is_void": false,
    #     "is_refund": false,
    #     "data": {
    #         "gateway_integration_pk": 4097558,
    #         "klass": "MigsPayment",
    #         "created_at": "2024-06-13T08:34:07.076347",
    #         "amount": 100000.0,
    #         "currency": "AED",
    #         "migs_order": {
    #             "acceptPartialAmount": false,
    #             "amount": 1000.0,
    #             "authenticationStatus": "AUTHENTICATION_SUCCESSFUL",
    #             "chargeback": {
    #                 "amount": 0,
    #                 "currency": "AED"
    #             },
    #             "creationTime": "2024-06-13T08:34:00.850Z",
    #             "currency": "AED",
    #             "description": "PAYMOB Parmagly",
    #             "id": "217503754",
    #             "lastUpdatedTime": "2024-06-13T08:34:06.883Z",
    #             "merchantAmount": 1000.0,
    #             "merchantCategoryCode": "7299",
    #             "merchantCurrency": "AED",
    #             "status": "CAPTURED",
    #             "totalAuthorizedAmount": 1000.0,
    #             "totalCapturedAmount": 1000.0,
    #             "totalRefundedAmount": 0.0
    #         },
    #         "merchant": "TESTMERCH_C_25P",
    #         "migs_result": "SUCCESS",
    #         "migs_transaction": {
    #             "acquirer": {
    #                 "batch": 20240613,
    #                 "date": "0613",
    #                 "id": "BMNF_S2I",
    #                 "merchantId": "MERCH_C_25P",
    #                 "settlementDate": "2024-06-13",
    #                 "timeZone": "+0200",
    #                 "transactionId": "123456789"
    #             },
    #             "amount": 1000.0,
    #             "authenticationStatus": "AUTHENTICATION_SUCCESSFUL",
    #             "authorizationCode": "326441",
    #             "currency": "AED",
    #             "id": "192036465",
    #             "receipt": "416508326441",
    #             "source": "INTERNET",
    #             "stan": "326441",
    #             "terminal": "BMNF0506",
    #             "type": "PAYMENT"
    #         },
    #         "txn_response_code": "APPROVED",
    #         "acq_response_code": "00",
    #         "message": "Approved",
    #         "merchant_txn_ref": "192036465",
    #         "order_info": "217503754",
    #         "receipt_no": "416508326441",
    #         "transaction_no": "123456789",
    #         "batch_no": 20240613,
    #         "authorize_id": "326441",
    #         "card_type": "MASTERCARD",
    #         "card_num": "512345xxxxxx2346",
    #         "secure_hash": "",
    #         "avs_result_code": "",
    #         "avs_acq_response_code": "00",
    #         "captured_amount": 1000.0,
    #         "authorised_amount": 1000.0,
    #         "refunded_amount": 0.0,
    #         "acs_eci": "02"
    #     },
    #     "is_hidden": false,
    #     "payment_key_claims": {
    #         "extra": {},
    #         "user_id": 302852,
    #         "currency": "AED",
    #         "order_id": 217503754,
    #         "amount_cents": 100000,
    #         "billing_data": {
    #             "city": "dumy",
    #             "email": "dumy@dumy.com",
    #             "floor": "dumy",
    #             "state": "dumy",
    #             "street": "dumy",
    #             "country": "UAE",
    #             "building": "dumy",
    #             "apartment": "sympl",
    #             "last_name": "dumy",
    #             "first_name": "dumy",
    #             "postal_code": "NA",
    #             "phone_number": "+201125773493",
    #             "extra_description": "NA"
    #         },
    #         "redirect_url": "https://uae.paymob.com/unifiedcheckout/payment-status?payment_token=ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDJsa0lqb3pNREk0TlRJc0ltRnRiM1Z1ZEY5alpXNTBjeUk2TVRBd01EQXdMQ0pqZFhKeVpXNWplU0k2SWtWSFVDSXNJbWx1ZEdWbmNtRjBhVzl1WDJsa0lqbzBNRGszTlRVNExDSnZjbVJsY2w5cFpDSTZNakUzTlRBek56VTBMQ0ppYVd4c2FXNW5YMlJoZEdFaU9uc2labWx5YzNSZmJtRnRaU0k2SW1SMWJYa2lMQ0pzWVhOMFgyNWhiV1VpT2lKa2RXMTVJaXdpYzNSeVpXVjBJam9pWkhWdGVTSXNJbUoxYVd4a2FXNW5Jam9pWkhWdGVTSXNJbVpzYjI5eUlqb2laSFZ0ZVNJc0ltRndZWEowYldWdWRDSTZJbk41YlhCc0lpd2lZMmwwZVNJNkltUjFiWGtpTENKemRHRjBaU0k2SW1SMWJYa2lMQ0pqYjNWdWRISjVJam9pUlVjaUxDSmxiV0ZwYkNJNkltUjFiWGxBWkhWdGVTNWpiMjBpTENKd2FHOXVaVjl1ZFcxaVpYSWlPaUlyTWpBeE1USTFOemN6TkRreklpd2ljRzl6ZEdGc1gyTnZaR1VpT2lKT1FTSXNJbVY0ZEhKaFgyUmxjMk55YVhCMGFXOXVJam9pVGtFaWZTd2liRzlqYTE5dmNtUmxjbDkzYUdWdVgzQmhhV1FpT21aaGJITmxMQ0psZUhSeVlTSTZlMzBzSW5OcGJtZHNaVjl3WVhsdFpXNTBYMkYwZEdWdGNIUWlPbVpoYkhObExDSnVaWGgwWDNCaGVXMWxiblJmYVc1MFpXNTBhVzl1SWpvaWNHbGZkR1Z6ZEY5a01EUmtNV0U0TkRrMk1tSTBOemt5T1dJeVpHTXhOalJoTURReU5qaGlZeUo5LkFPc3l2S1A4a3Fob0E5aVFOSEZfQWFaZl9HQi1NcU5kcXhrQmhlZm1feVpIZHJ3ci1xbkUxWklKT2FxekRFMkp5cXhCWXVEdnZ1VVZweGV3bFVGTTlB&trx_id=192036465",
    #         "integration_id": 4097558,
    #         "lock_order_when_paid": false,
    #         "next_payment_intention": "pi_test_d04d1a84962b47929b2dc164a04268bc",
    #         "single_payment_attempt": false
    #     },
    #     "error_occured": false,
    #     "is_live": false,
    #     "other_endpoint_reference": null,
    #     "refunded_amount_cents": 0,
    #     "source_id": -1,
    #     "is_captured": false,
    #     "captured_amount": 0,
    #     "merchant_staff_tag": null,
    #     "updated_at": "2024-06-13T11:34:07.272638",
    #     "is_settled": false,
    #     "bill_balanced": false,
    #     "is_bill": false,
    #     "owner": 302852,
    #     "parent_transaction": null
    # },
    # "issuer_bank": null,
    # "transaction_processed_callback_responses": ""
    # }
