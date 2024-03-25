from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from fooddeliveryapp.utils.permissions import IsAuthorized
from fooddeliveryapp.servicefactory import ServiceFactory

class RestaurantView(APIView):
    restaurant_service = ServiceFactory.get_service('restaurant')

    permission_classes = [IsAuthorized]
    
    def get(self, request, *args, **kwargs):
        response = self.restaurant_service.fetch_restaurant(request=request)
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        response= self.restaurant_service.register_restaurant(request)
        return Response(response, status=status.HTTP_201_CREATED)
    
class RestaurantMenuView(APIView):
    permission_classes = [IsAuthorized]
    restaurant_service = ServiceFactory.get_service('restaurant')

    def get(self, request, *args, **Kwargs):
        rest_id = self.kwargs.get('rest_id')
        response = self.restaurant_service.get_restaurant_menu(rest_id=rest_id)
        return Response(response, status=status.HTTP_200_OK)

class ItemView(APIView):
    permission_classes = [IsAuthorized]
    item_service = ServiceFactory.get_service('item')

    def get(self, request, *args, **kwargs):
        response = self.item_service.fetch_item(request)
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        response = self.item_service.add_item(request)
        return Response(response, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        response = self.item_service.remove_item(request=request)
        return Response({'deleted': response}, status=status.HTTP_200_OK)