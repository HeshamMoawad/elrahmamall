from rest_framework.generics import ListAPIView
from products.models import  Brand
from products.api.serializers import BrandSerializer


class BrandList(ListAPIView):
    queryset = Brand.objects.filter(hide=False)
    serializer_class = BrandSerializer
