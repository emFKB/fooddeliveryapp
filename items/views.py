from rest_framework.views import APIView
from .services import RestaurantService, ItemService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .permissions import IsAuthorized

class RestaurantView(APIView):
    restaurant_service = RestaurantService()
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthorized()]
        else:
            return [AllowAny()]
    
    def get(self, request, *args, **kwargs):
        response = self.restaurant_service.fetch_restaurant(request=request)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        response= self.restaurant_service.register_restaurant(request)
        return Response(response, status=status.HTTP_201_CREATED)
    
class RestaurantMenuView(APIView):
    def get(self, request, *args, **Kwargs):
        rest_id = self.kwargs.get('rest_id')
        restaurant_service = RestaurantService()
        response = restaurant_service.get_restaurant_menu(rest_id=rest_id)
        return Response(response, status=status.HTTP_200_OK)

class ItemView(APIView):
    item_service = ItemService()
    def get_permissions(self):
        if self.request.method in ["POST", 'DELETE']:
            return [IsAuthorized()]
        else:
            return [AllowAny()]
    def get(self, request, *args, **kwargs):
        response = self.item_service.fetch_item(request)
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        response = self.item_service.add_item(request)
        return Response(response, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        response = self.item_service.remove_item(request=request)
        return Response({'deleted': response}, status=status.HTTP_200_OK)