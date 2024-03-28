from .Orders import OrderDAO, OrderItemDAO
from django.db import transaction
from .serializers import (CreateOrderSerializer, CreateOrderRequestSerializer,
                          AddOrderItemSerializer, CreateOrderResponseSerializer)
from items.services import ItemService
from fooddeliveryapp.utils.Exception_Handler import NotFoundException, UnauthorizedException, InvalidException
from rest_framework.validators import ValidationError
from django.core.exceptions import ObjectDoesNotExist

class OrderService:
    __item_service = None

    def __init__(self, item_service = None):
        self.__item_service = item_service
    
    def create_order(self, request):
        try:
            request_serializer = CreateOrderRequestSerializer(data=request.data)
            
            if not request_serializer.is_valid():
                raise ValidationError(request_serializer.errors)
            
            with transaction.atomic():
                cust = request.user.user_id
                rest = request_serializer.validated_data['rest_id']
                items = request_serializer.validated_data['items']
                total = self.__item_service.calculate_item_total(items, rest)
                
                order_dict = {"cust_id":cust, "rest_id": rest , "total":float(total)}
                order_serializer = CreateOrderSerializer(data=order_dict)

                if not order_serializer.is_valid():
                    raise ValidationError(order_serializer.errors)
                
                order = OrderDAO.create_order(order_serializer.validated_data)
                self.__add_orderitems(items, order.order_id)

                response_dict = {'order_id': order.order_id, 'cust_name': order.cust_id.username, 'rest_name': order.rest_id.rest_name, 'total': order.total}
                order_response = CreateOrderResponseSerializer(data=response_dict)

                if not order_response.is_valid():
                    raise ValidationError(order_serializer.errors)
                
                return order_response.validated_data
            
        except ObjectDoesNotExist:
            raise InvalidException("Item does not exist")
    
    def get_customer_orders(self, cust_id):
        return OrderDAO.get_customer_orders_by_id(cust_id=cust_id)
    
    def get_restaurant_orders(self, rest_id):
        return OrderDAO.get_restaurant_orders_by_id(rest_id=rest_id)
    
    def get_order_by_id(self, order_id):
        return OrderDAO.get_order_by_id(order_id=order_id)
    
    def __add_orderitems(self, items, order_id):
        try:
            for item in items:
                item_dict = {"order_id": order_id, "item_id": ItemService.get_item_by_id(item_id=item['item_id']).item_id, "quantity": item['quantity']}
                orderitems_serializer = AddOrderItemSerializer(data=item_dict)
                if not orderitems_serializer.is_valid():
                    raise ValidationError(orderitems_serializer.errors)
                OrderItemDAO.create_orderitems(orderitems_serializer.validated_data)
                    
        except ObjectDoesNotExist:
            raise InvalidException("Item Does not exist")
    
    def fetch_orders(self, request):
        if request.query_params.get('order_id'):
            return self.__fetch_single_order(request=request)
        
        if request.user.is_staff:
            orders = self.get_restaurant_orders(rest_id=request.user.user_id)
        else:
            orders = self.get_customer_orders(cust_id=request.user.user_id)
        
        return self.__fetch_multiple_orders(request=request, orders=orders)
            
                
    def __get_order_items(self, order):
        items = []
        for item in order.items.all():
            items.append({
                'item_id': item.item_id.item_id,
                'item_name': item.item_id.item_name,
                'item_price': item.item_id.item_price,
                'quantity': item.quantity,
            })
        return items
    
    def __fetch_single_order(self, request):
        try:
            order = OrderDAO.get_order_by_id(order_id=request.query_params.get('order_id'))
            if order:
                if order.cust_id.user_id != request.user.user_id:
                    raise UnauthorizedException("Unauthorized request")
                items = self.__get_order_items(order)
                response = {'order_id': order.order_id,
                            'rest_id': order.rest_id.rest_id,
                            'rest_name': order.rest_id.rest_name,
                            'cust_name': request.user.username,
                            'items': items,
                            'total': order.total}
                return response  
        except ObjectDoesNotExist:
            raise NotFoundException("Order does not exist")
        
    def __fetch_multiple_orders(self, request, orders):
        orders_response = []
        for order in orders:
            items_data = self.__get_order_items(order)
            order_data = {
                "order_id": order.order_id,
                "total": order.total,
                "rest_id": order.rest_id.rest_id,
                "rest_name": order.rest_id.rest_name,
                "cust_name": request.user.username,
                "items": items_data,
            }
            orders_response.append(order_data)
        return orders_response