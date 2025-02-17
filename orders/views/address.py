from rest_framework.generics import ListAPIView
from orders.models import  Address
from orders.api.serializers import AddressSerializer


class AddressList(ListAPIView):
    queryset = Address.objects.filter(hide=False)
    serializer_class = AddressSerializer
