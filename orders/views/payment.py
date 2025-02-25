# from typing import List
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
        price=price
    )
    
    if isinstance(intention,PaymentIntention):
        new_link.client_secret = intention.client_secret,
        url = payment.get_payment_url(intention.client_secret)
        new_link.payment_link = url
        new_link.save()
        return Response({"url":url})
    else :
        new_link.save()
        return Response({"detail":intention.errors})

