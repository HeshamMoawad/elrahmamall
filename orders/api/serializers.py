from rest_framework import serializers
from orders.models import Address, Order
from paymob.dataclasses import Item
from products.api.serializers import ProductSerializer

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'price']


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    # Display related objects with nested serializers or string representations
    user = serializers.StringRelatedField()
    country = AddressSerializer()
    items = ItemSerializer(many=True)
    
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
            'delivery_price',
            'total_price',
            'order_date',
            'created_at',
            'updated_at'
        ]