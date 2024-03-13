from rest_framework import serializers
from .models import OrderItem, Order
from items.serializers import ItemSerializer
from rest_framework.validators import ValidationError
from users.models import User
from items.models import Restaurant

class OrderItemsSerializer(serializers.ModelSerializer):
    items_details = ItemSerializer(source='item_id', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'items_details']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'ouid', 'cust_id', 'rest_id', 'order_items']

class ItemRequestSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

class CreateOrderRequestSerializer(serializers.Serializer):
    cust_id = serializers.IntegerField(required=False)
    rest_id = serializers.IntegerField(required=True)
    items = ItemRequestSerializer(many=True, required=True)
    total = serializers.FloatField(required=False)

class CreateOrderResponseSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    cust_name = serializers.CharField()
    rest_name = serializers.CharField()
    total = serializers.FloatField()

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        rest_id = attrs.get('rest_id')
        cust_id = attrs.get('cust_id')
        total = attrs.get('total')

        if not rest_id and not cust_id and not total:
            raise ValidationError("Request body missing")

        if total <= 0:
            raise ValidationError('Total cannot be 0 or less')
        
        return attrs

class AddOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'