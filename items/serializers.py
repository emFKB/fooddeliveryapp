from .models import Restaurant, Item
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['rest_name', 'rest_location']

    def validate(self, attributes):
        errors = {}
        rest_name = attributes.get('rest_name')
        rest_loc = attributes.get('rest_location')
        if len(rest_name) < 3:
            errors['rest_name'] = 'Restaurant name must be more than 2 characters'
        
        if len(rest_loc) < 5:
            errors['rest_location'] = 'Restaurant location must be complete address'

        if errors:
            raise ValidationError(errors)
        return attributes
        
class SearchRestaurantSerializer(serializers.Serializer):
    rest_id = serializers.IntegerField(required=False)
    rest_name = serializers.CharField(required=False)
    rest_location = serializers.CharField(required=False)

    class Meta:
        model = Restaurant
        fields = ['rest_id', 'rest_name', 'rest_location']

    def validate(self, attributes):
        errors = {}
        rest_id = attributes.get('rest_id')
        rest_name = attributes.get('rest_name')
        rest_loc = attributes.get('rest_location')
        if not rest_id and not rest_name and not rest_loc:
            errors['missing_attributes'] = 'please provide an attribute to search on restaurants'
        
        if rest_name and len(rest_name)<3:
            errors['rest_name'] = 'Restaurant name must be more than 2 characters'
        
        if errors:
            raise ValidationError(errors)
        
        return attributes

class RestaurantMenuSerializer(serializers.Serializer):
    items = ItemSerializer(many=True, read_only=True)
    rest_name = serializers.CharField(read_only = True)
    rest_location = serializers.CharField(read_only=True)
    class Meta:
        model = Restaurant
        fields = ['rest_name', 'rest_location', 'items']

class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_id', 'item_name', 'item_desc', 'item_price', 'rest_id']

    def validate(self, attributes):
        errors = {}

        if len(attributes.get('item_name')) < 1:
            errors['item_name'] = 'Item name must not be empty'

        if (attributes.get('item_price') <= 0):
            errors['item_price'] = 'Item price cannot be 0 or less'

        if errors:
            raise ValidationError(errors)
        
        return attributes
    
class SearchRestaurantItems(serializers.Serializer):
    rest_detail = RestaurantSerializer(source='rest_id', read_only=True)
    item_id = serializers.IntegerField(required=False)
    item_name = serializers.CharField(required=False)
    item_price = serializers.FloatField(required=False)
    item_desc = serializers.CharField(required=False)

    class Meta:
        model = Item
        fields = ['rest_detail', 'item_name', 'item_desc', 'item_price']

    def validate(self, attributes):
        errors = {}
        item_id = attributes.get('item_id')
        item_name = attributes.get('item_name')
        item_price = attributes.get('item_price')

        if not item_id and not item_name and not item_price:
            errors['missing_attribtes'] = 'please provide an attribute to search on items'
        
        if item_name and len(attributes.get('item_name')) < 1:
            errors['item_name'] = 'Item name must not be empty'

        if item_price and item_price <= 0:
            errors['item_price'] = 'Item price cannot be 0 or less'
        
        if errors:
            raise ValidationError(errors)
        
        return attributes
    
class DeleteItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(read_only=True)
    item_name = serializers.CharField(read_only=True)
    item_price = serializers.FloatField(read_only=True)
    item_desc = serializers.CharField(read_only=True)
    class Meta:
        model = Item
        fields = ['item_id', 'item_name', 'item_price', 'item_desc']