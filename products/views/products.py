import logging
from rest_framework.generics import ListAPIView
from products.models import Product , models
from products.api.serializers import ProductSerializer
from rest_framework import filters


class ProductsList(ListAPIView):
    serializer_class = ProductSerializer
    search_fields = ['categories__name','pk',"name"]

    def get_queryset(self):
        queryset = Product.objects.filter(hide=False)
        
        search_txt = self.request.query_params.get("search",None)
        if search_txt :
            return queryset.filter(name__icontains=search_txt)
        
        product_id = self.request.query_params.get('id', None)
        if product_id :
            return queryset.filter(pk=product_id)
        
        category = self.request.query_params.get('category', None)
        if category :
            return queryset.filter(categories=category)
        
        return queryset
