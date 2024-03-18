from .Restaurants import RestaurantDAO
from .Items import ItemDAO
from collections import OrderedDict

class RestaurantService():
    @staticmethod
    def register_restaurant(restaurant_data):
        return RestaurantDAO.add_restaurant(restaurant_data=restaurant_data)
    
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
        return RestaurantDAO.get_restaurant_items(rest_id)
    
class ItemService():
    @staticmethod
    def add_item(item_data):
        return ItemDAO.add_item(item_data=item_data)
    
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

    @staticmethod
    def remove_item(item_id):
        return ItemDAO.delete_item(item_id=item_id)