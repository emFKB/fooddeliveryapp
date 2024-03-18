from rest_framework.views import APIView
from .services import OrderService
from items.services import ItemService
from .serializers import (CreateOrderSerializer, CreateOrderRequestSerializer,
                          AddOrderItemSerializer, CreateOrderResponseSerializer)
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .permissions import IsAuthorized

class OrdersCreateView(APIView):
    permission_classes = [IsAuthorized]
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
    
class FetchOrderView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthorized()]
        
    def get(self, request, *args, **kwargs):
        try:
            if request.query_params.get('order_id'):
                try:
                    order = OrderService.get_order_by_id(order_id=request.query_params.get('order_id'))
                    
                    if order.cust_id.user_id == request.user.user_id:
                        items = []
                        for item in order.items.all():
                            items.append({
                                'item_id': item.item_id.item_id,
                                'item_name': item.item_id.item_name,
                                'item_price': item.item_id.item_price,
                                'quantity': item.quantity,
                            })
                        response = {'order_id': order.order_id,
                                    'rest_id': order.rest_id.rest_id,
                                    'rest_name': order.rest_id.rest_name,
                                    'cust_name': request.user.username,
                                    'items': items,
                                    'total': order.total}
                        return Response(response, status=status.HTTP_200_OK)
                    return Response("Unauthorized", status=status.HTTP_403_FORBIDDEN)
                except:
                    return Response("Does not exist", status=status.HTTP_404_NOT_FOUND)
            
            if request.user.is_staff:
                orders = OrderService.get_restaurant_orders(rest_id=request.user.user_id)
            else:
                orders = OrderService.get_customer_orders(cust_id=request.user.user_id)
            
            response_data = []
            for order in orders:
                items_data = []
                for item in order.items.all():
                    items_data.append({
                        "item_id": item.item_id.item_id,
                        "quantity": item.quantity,
                        "item_name": item.item_id.item_name,
                        "item_price": item.item_id.item_price,
                    })
                order_data = {
                    "order_id": order.order_id,
                    "total": order.total,
                    "rest_id": order.rest_id.rest_id,
                    "rest_name": order.rest_id.rest_name,
                    "cust_name": request.user.username,
                    "items": items_data,
                }
                response_data.append(order_data)
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            if NotImplementedError:
                return Response("Not Implemented!", status=status.HTTP_501_NOT_IMPLEMENTED)
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
    
