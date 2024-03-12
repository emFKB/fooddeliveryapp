from .Orders import OrderDAO, OrderItemDAO

class OrderService:
    @staticmethod
    def create_order(order_data):
        return OrderDAO.create_order(order_data=order_data)
    
    @staticmethod
    def get_customer_orders(cust_id):
        return OrderDAO.get_customer_orders_by_id(cust_id=cust_id)
    
    @staticmethod
    def get_restaurant_orders(rest_id):
        return OrderDAO.get_restaurant_orders_by_id(rest_id=rest_id)
    
    @staticmethod
    def get_order_by_id(order_id):
        return OrderDAO.get_order_by_id(order_id=order_id)
    
    @staticmethod
    def add_orderitems(orderitems_data):
        return OrderItemDAO.create_orderitems(orderitems_data)