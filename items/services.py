from .Restaurants import RestaurantDAO
from .Items import ItemDAO
from collections import OrderedDict
from .serializers import (
    CreateRestaurantSerializer, SearchRestaurantSerializer,
    CreateItemSerializer, SearchRestaurantItems, RestaurantMenuSerializer,
    DeleteItemSerializer, RestaurantSerializer
    )
from rest_framework.validators import ValidationError
from fooddeliveryapp.utils.Exceptions import NotFoundException

class RestaurantService():
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def register_restaurant(self, request):
        serializer = CreateRestaurantSerializer(data=request.data)

        if serializer.is_valid():
            restaurant = RestaurantDAO.add_restaurant(restaurant_data=serializer.validated_data)
            return serializer.data
        raise ValidationError(serializer.errors)
    
    @staticmethod
    def get_all_restaurant():
        return RestaurantDAO.get_all_restaurant()

    @staticmethod
    def get_restaurant(attributes: OrderedDict = None, rest_id:int = None):
        if (attributes):
            return RestaurantDAO.get_restaurant_by_attributes(attributes)
        elif rest_id:
            return RestaurantDAO.get_restaurant_by_id(rest_id = rest_id)
        else:
            return None
        
    @staticmethod 
    def get_restaurant_menu(rest_id:int ):
        restaurant = RestaurantDAO.get_restaurant_items(rest_id)
        serializer = RestaurantMenuSerializer(restaurant)
        if serializer.is_valid:
            return serializer.data
        raise ValidationError(serializer.errors)
    
    def fetch_restaurant(self, request):
        if len(request.query_params)==0:
            restaurants = RestaurantDAO.get_all_restaurant()
            response = RestaurantSerializer(restaurants, many=True)
            return response.data
        serializer = SearchRestaurantSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = RestaurantDAO.get_restaurant_by_attributes(serializer.validated_data)
            if queryset:
                serialized_data = [serializer.to_representation(restaurant) for restaurant in queryset]
                return serialized_data
            else:
                raise NotFoundException("Restaurant not found")
        raise ValidationError(serializer.errors)
    
class ItemService():
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def add_item(self, request):
        serializer = CreateItemSerializer(data=request.data)
        if (serializer.is_valid()):
            item = ItemDAO.add_item(serializer.validated_data)
            return serializer.data
        raise ValidationError(serializer.errors)
    
    @staticmethod
    def get_item(attributes: OrderedDict = None, item_id:int = None):
        if attributes:
            return ItemDAO.get_item_by_attributes(attributes=attributes)
        elif item_id:
            return ItemDAO.get_item_by_id(item_id=item_id)
        else:
            return None
        
    @staticmethod
    def get_item_by_id(item_id):
        return ItemDAO.get_item_by_id(item_id=item_id)

    def remove_item(self, request):
        serializer = DeleteItemSerializer(data=request.data)
        if (serializer.is_valid()):
            item = ItemDAO.delete_item(serializer.validated_data.get('item_id'))
            if item:
                return item
            else:
                return item
        raise ValidationError(serializer.errors)
    
    def fetch_item(self, request):
        serializer = SearchRestaurantItems(data=request.query_params)
        if serializer.is_valid():
            queryset = ItemDAO.get_item_by_attributes(attributes=serializer.validated_data)
            if queryset:
                serialized_data = [serializer.to_representation(item) for item in queryset]
                return serialized_data
            else:
                raise NotFoundException("No Item Found")
        raise ValidationError(serializer.errors)

        
    def calculate_item_total(self, items):
        total = 0
        item_ids = [item['item_id'] for item in items]
        for item in items:
            total += item['quantity'] * ItemDAO.get_item_by_id(item_id=item['item_id']).item_price
        return total
