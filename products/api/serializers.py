from rest_framework import serializers
from products.models import Category, Brand, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description' ]



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'image']



class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    brand = BrandSerializer()
    details = serializers.SerializerMethodField()

    def get_details(self,obj:Product):
        return obj.details.splitlines() if obj.details else None

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'categories', 'brand', 'count', 'details']


class ProductHomeSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    details = serializers.SerializerMethodField()

    def get_details(self,obj:Product):
        details = obj.details
        if details :
            details = {key:value for key,value in map(lambda x : x.split(":") ,details.splitlines())}
        return details

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'brand', 'count', 'details']



class HomeSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self,obj):
        return ProductHomeSerializer(obj.product_set.filter(hide=False), many=True).data
    class Meta:
        model = Category
        fields = ['id', 'name', 'description'  , 'products']

