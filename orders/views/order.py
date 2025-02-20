from typing import List
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from orders.models import Item, Order
from orders.api.serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from orders.forms.order import OrderForm
from products.models import Product


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
        item_dict['product'] = product
        item = Item(**item_dict)
        item.save()
        result.append(item)
    # Item.objects.bulk_create(result)
    return result


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request:Request):
    data = request.data.copy()
    data['user'] = request.user.pk
    data['items'] = items_factory(data['items']) if len(data['items']) > 0 else []
    form = OrderForm(data)
    if form.is_valid():
        form.save()
        return Response({}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)