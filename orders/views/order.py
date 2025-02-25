from typing import List
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from orders.models import Item, Order, PaymentAccountModel
from orders.api.serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from orders.forms.order import ItemsForm, OrderForm
from paymob.dataclasses import BillingData, Intention
from products.models import Product
from paymob.client import PaymobIntentionClient 
from paymob.client import Item as IntentionItem 



class OrderList(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def list(self, request:Request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().list(request, *args, **kwargs)
    





def items_factory(items:List[dict]):
    result = []
    products = Product.objects.filter(pk__in = [ i.get("product",0) for i in items])
    for item_dict in items:
        product = products.get(pk=item_dict['product'])
        if int(product.count) < int(item_dict['quantity']) :
            raise ValueError("الرجاءالتاكد من السلة مجددا لانه يوجد منتج غير متوفر بشكل كافى")
        item_dict['product'] = product
        item_dict['amount'] = float(product.price) * int(item_dict['quantity'])
        item = Item(**item_dict)
        result.append(item)
    return result



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request:Request):
    data = request.data.copy()
    data['user'] = request.user
    items = data.pop("items",[])
    if items :
        form = OrderForm(data)
        try : 
            items = items_factory(items)
            total_items = sum(map(lambda x : float(x.amount),items))
            if total_items > 100000 and data['delivery_price'] != 0:
                raise ValueError("التوصيل يكون مجانيا اذا كانت قيمة الطلب اكبر من 100الف جنيه")
            if total_items > 30000 and data['is_cash_payment'] :
                raise ValueError("لا يمكن انشاء طلب يكون فيه الدفع عند التوصيل و تكون قيمته اعلى من 30الف جنيه")
        except ValueError as v:
            return Response({"detail":str(v)}, status=status.HTTP_400_BAD_REQUEST)

        if form.is_valid():
            form.save()
            order : Order = form.instance
            for itm in items :
                itm.order = order
                itm.save()
            ser = OrderSerializer(order)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else :
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail":"الطلب يجب ان يحتوى على منتجات"}, status=status.HTTP_400_BAD_REQUEST)



