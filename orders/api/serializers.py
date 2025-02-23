from rest_framework import serializers
from orders.models import Address, Order , Item, PaymentMethodModel
from products.api.serializers import ProductSerializer

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'price']


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity',"order"]


class OrderSerializer(serializers.ModelSerializer):
    # Display related objects with nested serializers or string representations
    user = serializers.StringRelatedField()
    country = AddressSerializer()
    items = serializers.SerializerMethodField()#ItemSerializer(many=True)
    
    def get_items(self,obj):
        return ItemSerializer(obj.item_set,many=True).data
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_uuid',
            'user',
            'country',
            'district',
            'apartment',
            'street',
            'building',
            'floor',
            'raw_address',
            'is_cash_payment',
            'is_online_payment',
            'is_delivery_paid',
            'is_paid',
            'items',
            'note',
            'delivery_price',
            'total_price',
            'order_date',
            'created_at',
            'updated_at'
        ]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethodModel
        fields = [
            'id',
            "name",
        ]

