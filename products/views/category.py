from rest_framework.generics import ListAPIView
from products.models import  Category
from products.api.serializers import CategorySerializer


class CategoryList(ListAPIView):
    queryset = Category.objects.filter(hide=False)
    serializer_class = CategorySerializer
