from abc import ABCMeta, abstractstaticmethod
from .models import Item
from collections import OrderedDict

class ItemInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "add_item") and callable(subclass.add_item) 
                and hasattr(subclass, "get_item_by_id") and callable(subclass.get_item_by_id)
                and hasattr(subclass, "get_item_by_attributes") and callable(subclass.get_item_by_attributes)
                and hasattr(subclass, "delete_item") and callable(subclass.delete_item))
    
    @abstractstaticmethod
    def add_item(item_data):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_item_by_id(item_id):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_item_by_attributes(attributes):
        raise NotImplementedError
    
    @abstractstaticmethod
    def delete_item(item_id):
        raise NotImplementedError
    
class ItemDAO(ItemInterface):
    def add_item(item_data):
        return Item.objects.create(**item_data)
    
    def get_item_by_id(item_id):
        return Item.objects.get(item_id=item_id)
    
    def get_items_by_ids(item_ids):
        return Item.objects.filter(item_id__in=item_ids)

    def get_item_by_attributes(attributes):
        item_id = attributes.get('item_id')
        item_name = attributes.get('item_name')
        item_price = attributes.get('item_price')

        if item_id:
            return Item.objects.filter(item_id=item_id)
        elif item_name and item_price:
            return Item.objects.filter(item_name__icontains=item_name).filter(item_price=item_price)
        elif item_name:
            return Item.objects.filter(item_name__icontains=item_name)
        elif item_price:
            return Item.objects.filter(item_price=item_price)
        else:
            return None

    def delete_item(item_id):
        try:
            item = ItemDAO.get_item_by_id(item_id)
            item.delete()
            return True
        except Item.DoesNotExist:
            return False