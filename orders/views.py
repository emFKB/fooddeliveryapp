from rest_framework.views import APIView
from fooddeliveryapp.servicefactory import ServiceFactory
from rest_framework.response import Response
from rest_framework import status
from fooddeliveryapp.utils.permissions import IsAuthorized

class OrdersCreateView(APIView):
    permission_classes = [IsAuthorized]
    order_service = ServiceFactory.get_service('order')
    def post(self, request, *args, **kwarsg):
        response = self.order_service.create_order(request=request)
        return Response(response, status=status.HTTP_201_CREATED)
    
class FetchOrderView(APIView):
    order_service = ServiceFactory.get_service('order')

    permission_classes = [IsAuthorized]
    
    def get(self, request, *args, **kwargs):
        response = self.order_service.fetch_orders(request=request)
        return Response(response, status=status.HTTP_200_OK)
    
