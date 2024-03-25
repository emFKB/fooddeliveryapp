from users.services import UserService
from items.services import ItemService, RestaurantService
from orders.services import OrderService
from authorization import AuthService

class ServiceFactory:
    _instances = {}

    @classmethod
    def get_service(cls, view):
        if view not in cls._instances:
            if view == 'user':
                cls._instances[view] = UserService()
            elif view == 'order':
                cls._instances[view] = OrderService(cls.get_service('item'))
            elif view == 'item':
                cls._instances[view] = ItemService()
            elif view == 'restaurant':
                cls._instances[view] = RestaurantService()
            elif view == 'permission_auth':
                cls._instances[view] = AuthService('127.0.0.1', '8000')
            else:
                raise ValueError(f"Service for {view} doesn't exist")
        return cls._instances[view]