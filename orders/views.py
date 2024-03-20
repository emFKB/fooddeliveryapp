from rest_framework.views import APIView
from .services import OrderService
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthorized

class OrdersCreateView(APIView):
    permission_classes = [IsAuthorized]
    def post(self, request, *args, **kwarsg):
        order_service = OrderService()
        response = order_service.create_order(request=request)
        return Response(response, status=status.HTTP_201_CREATED)
    
class FetchOrderView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthorized()]
        
    def get(self, request, *args, **kwargs):
        order_service = OrderService()
        response = order_service.fetch_orders(request=request)
        return Response(response, status=status.HTTP_200_OK)
    
