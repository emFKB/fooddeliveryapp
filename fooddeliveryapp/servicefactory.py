from users.services import UserService
from items.services import ItemService, RestaurantService
from orders.services import OrderService

class ServiceFactory:
    services = {
        'user': UserService.get_instance(),
        'order': OrderService.get_instance(),
        'item': ItemService.get_instance(),
        'restaurant': RestaurantService.get_instance(),
    }

    @classmethod
    def get_service(cls, view):
        if view in cls.services:
            return cls.services[view]
        raise ValueError(f"Service for {view} doesn't exist")