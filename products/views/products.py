from rest_framework.generics import ListAPIView
from products.models import Product , Category
from products.api.serializers import ProductSerializer
from rest_framework import filters

class ProductsList(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['categories__name','pk']

    def get_queryset(self):
        queryset = Product.objects.filter(hide=False)
        
        product_id = self.request.query_params.get('id', None)
        if product_id is not None:
            return queryset.filter(pk=product_id)
        
        category = self.request.query_params.get('category', None)
        if category is not None:
            return queryset.filter(categories=category)
        
        return queryset
