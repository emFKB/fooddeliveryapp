from rest_framework.views import APIView
from .services import OrderService
from items.services import ItemService, RestaurantService
from users.services import UserService
from .serializers import (CreateOrderSerializer, CreateOrderRequestSerializer,
                          AddOrderItemSerializer, CreateOrderResponseSerializer)
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class OrdersCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request_data, *args, **kwarsg):
        request_serializer = CreateOrderRequestSerializer(data=request_data.data)
        if request_serializer.is_valid():
            with transaction.atomic():
                cust = request_data.user.user_id
                rest = request_serializer.validated_data['rest_id']
                total = 0
                items = request_serializer.validated_data['items']
                for item in items:
                    total += item['quantity'] * ItemService.get_item_by_id(item_id=item['item_id']).item_price
                
                order_dict = {"cust_id":cust, "rest_id": rest , "total":float(total)}
                order_serializer = CreateOrderSerializer(data=order_dict)
                if order_serializer.is_valid():
                    order = OrderService.create_order(order_serializer.validated_data)
                    for item in items:
                        item_dict = {"order_id":order.order_id, "item_id":ItemService.get_item_by_id(item_id=item['item_id']).item_id, "quantity":item['quantity']}
                        orderitems_serializer = AddOrderItemSerializer(data=item_dict)
                        if orderitems_serializer.is_valid():
                            OrderService.add_orderitems(orderitems_serializer.validated_data)
                    response_dict = {'order_id': order.order_id, 'cust_name': order.cust_id.username, 'rest_name': order.rest_id.rest_name, 'total': order.total}
                    order_response = CreateOrderResponseSerializer(data=response_dict)
                    if order_response.is_valid():
                        return Response(order_response.validated_data, status=status.HTTP_201_CREATED)
                    
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)