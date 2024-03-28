from .models import Order, OrderItem
from abc import ABCMeta, abstractstaticmethod

class OrderInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass):
        return (hasattr(__subclass, "create_order") and callable(__subclass.create_order)
                and hasattr(__subclass, "get_customer_orders_by_id") and callable(__subclass.get_customer_orders_by_id)
                and hasattr(__subclass, "get_restaurant_orders_by_id") and callable(__subclass.get_restaurant_orders_by_id)
                and hasattr(__subclass, "get_order_by_id") and callable(__subclass.get_order_by_id)
                and hasattr(__subclass, "create_orderitems") and callable(__subclass.create_orderitems))

    @abstractstaticmethod
    def create_order(order_data):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_customer_orders_by_id(cust_id):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_restaurant_orders_by_id(rest_id):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_order_by_id(order_id):
        raise NotImplementedError
    
    @abstractstaticmethod
    def create_orderitems(orderitems_data):
        raise NotImplementedError
    
class OrderDAO(OrderInterface):
    def create_order(order_data):
        return Order.objects.create(**order_data)

    def get_customer_orders_by_id(cust_id):
        return Order.objects.filter(cust_id=cust_id)

    def get_restaurant_orders_by_id(rest_id):
        return Order.objects.filter(rest_id=rest_id)
    
    def get_order_by_id(order_id):
        return Order.objects.get(order_id=order_id)
    
    def create_orderitems(orderitems_data):
        pass

class OrderItemDAO(OrderInterface):
    def create_order(order_data):
        pass

    def get_customer_orders_by_id(cust_id):
        pass

    def get_restaurant_orders_by_id(rest_id):
        pass
    
    def get_order_by_id(order_id):
        pass
    
    def create_orderitems(orderitems_data):
        return OrderItem.objects.create(**orderitems_data)