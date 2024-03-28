from abc import ABCMeta, abstractstaticmethod
from .models import Restaurant
from collections import OrderedDict

class RestaurantInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "add_restaurant") and callable(subclass.add_restaurant) 
                and hasattr(subclass, "get_restaurant_by_id") and callable(subclass.get_restaurant_by_id)
                and hasattr(subclass, "get_restaurant_by_attributes") and callable(subclass.get_restaurant_by_attributes))

    @abstractstaticmethod
    def add_restaurant(restaurant_data):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_restaurant_by_id(rest_id: int):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_restaurant_by_attributes(request_data: OrderedDict):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_all_restaurant():
        raise NotImplementedError
    

class RestaurantDAO(RestaurantInterface):
    def add_restaurant(restaurant_data):
        return Restaurant.objects.create(**restaurant_data)
    
    def get_restaurant_by_id(rest_id: int):
        return Restaurant.objects.get(rest_id=rest_id)
    
    def get_restaurant_items(rest_id:int):
        restaurant = Restaurant.objects.get(rest_id = rest_id)
        return restaurant
    
    def get_restaurant_by_attributes(request_data: OrderedDict):
        rest_id = request_data.get('rest_id')
        rest_name = request_data.get('rest_name')
        rest_loc = request_data.get('rest_location')
        if rest_id:
            restaurant = Restaurant.objects.filter(rest_id=rest_id)
        elif (rest_name and rest_loc):
            restaurant = Restaurant.objects.filter(rest_name__icontains=rest_name)\
                .filter(rest_location__icontains = rest_loc)
        elif (rest_name):
            restaurant = Restaurant.objects.filter(rest_name__icontains=rest_name)
        elif (rest_loc):
            restaurant = Restaurant.objects.filter(rest_location__icontains = rest_loc)
        else:
            return None
        
        return restaurant
    
    def get_all_restaurant():
        return Restaurant.objects.all()