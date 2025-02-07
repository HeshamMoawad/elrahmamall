from rest_framework.generics import ListAPIView
from products.models import Product
from products.api.serializers import ProductSerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.filter(hide=False)
    serializer_class = ProductSerializer
