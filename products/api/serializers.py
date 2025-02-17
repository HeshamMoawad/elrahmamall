from rest_framework import serializers
from products.models import Category, Brand, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description' ,'is_sale']



class BrandSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: Brand):
        if obj.image:
            return obj.image.url
        return None

    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'image']


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    brand = BrandSerializer(read_only=True)
    details = serializers.SerializerMethodField()
    image_1 = serializers.SerializerMethodField()
    image_2 = serializers.SerializerMethodField()
    image_3 = serializers.SerializerMethodField()
    # image_4 = serializers.SerializerMethodField()

    def get_image_1(self, obj: Product):
        if obj.image_1:
            return obj.image_1.url
        return None
    def get_image_2(self, obj: Product):
        if obj.image_2:
            return obj.image_2.url
        return None
    def get_image_3(self, obj: Product):
        if obj.image_3:
            return obj.image_3.url
        return None

    def get_details(self,obj:Product):
        return obj.details.splitlines() if obj.details else None

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'categories', 'brand', 'count', 'details', "image_1", "image_2", "image_3" ]


class ProductHomeSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    # details = serializers.SerializerMethodField()

    # def get_details(self,obj:Product):
    #     details = obj.details
    #     if details :
    #         details = {key:value for key,value in map(lambda x : x.split(":") ,details.splitlines())}
    #     return details

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'brand', 'count', 'details', "image_1", "image_2", "image_3" ]



class HomeSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self,obj):
        return ProductHomeSerializer(obj.product_set.filter(hide=False), many=True).data
    class Meta:
        model = Category
        fields = ['id', 'name', 'description'  , 'products' , 'is_sale']

