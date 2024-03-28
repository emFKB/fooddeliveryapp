from .Restaurants import RestaurantDAO
from .Items import ItemDAO
from collections import OrderedDict
from .serializers import (
    CreateRestaurantSerializer, SearchRestaurantSerializer,
    CreateItemSerializer, SearchRestaurantItems, RestaurantMenuSerializer,
    DeleteItemSerializer, RestaurantSerializer
    )
from rest_framework.validators import ValidationError
from fooddeliveryapp.utils.Exceptions import NotFoundException, InvalidException
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

class RestaurantService():    
    def register_restaurant(self, request):
        serializer = CreateRestaurantSerializer(data=request.data)

        if serializer.is_valid():
            restaurant = RestaurantDAO.add_restaurant(restaurant_data=serializer.validated_data)
            cache.delete('restaurants')
            return serializer.data
        raise ValidationError(serializer.errors)
    
    def get_all_restaurant(self):
        cache_restaurant = cache.get('restaurants', None)
        if not cache_restaurant:
            rest = RestaurantDAO.get_all_restaurant()
            cache_restaurant.set('restaurants', rest)
            return rest
        return cache_restaurant

    def get_restaurant(self, attributes: OrderedDict = None, rest_id:int = None):
        if (attributes):
            return RestaurantDAO.get_restaurant_by_attributes(attributes)
        elif rest_id:
            return RestaurantDAO.get_restaurant_by_id(rest_id = rest_id)
        else:
            return None
        
    def get_restaurant_menu(self, rest_id:int ):
        try:
            restaurant = RestaurantDAO.get_restaurant_items(rest_id)
            serializer = RestaurantMenuSerializer(restaurant)
            if serializer.is_valid:
                return serializer.data
            raise ValidationError(serializer.errors)
        except ObjectDoesNotExist:
            raise NotFoundException("Restaurant does not exist")
    
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
    def add_item(self, request):
        serializer = CreateItemSerializer(data=request.data)
        if (serializer.is_valid()):
            item = ItemDAO.add_item(serializer.validated_data)
            return serializer.data
        raise ValidationError(serializer.errors)

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

        
    def calculate_item_total(self, items, rest_id):
        total = 0
        for item in items:
            item_db = ItemDAO.get_item_by_id(item_id=item['item_id'])
            if not item_db.rest_id.rest_id == rest_id: 
                raise InvalidException("Item does not belong to the restaurant")
            total += item['quantity'] * item_db.item_price
        return total
