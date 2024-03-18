from rest_framework.views import APIView
from .serializers import (
    CreateRestaurantSerializer, SearchRestaurantSerializer,
    CreateItemSerializer, SearchRestaurantItems, RestaurantMenuSerializer,
    DeleteItemSerializer, RestaurantSerializer
    )
from .services import RestaurantService, ItemService
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsStaff, IsAuthorized

class RestaurantView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthorized()]
        else:
            return [AllowAny()]
    
    def get(self, request_data, *args, **kwargs):
        if len(request_data.query_params)==0:
            restaurants = RestaurantService.get_all_restaurant()
            response = RestaurantSerializer(restaurants, many=True)
            return Response(response.data)
        serializer = SearchRestaurantSerializer(data=request_data.query_params)

        if serializer.is_valid():
            queryset = RestaurantService.get_restaurant(attributes=serializer.validated_data)
            if queryset:
                serialized_data = [serializer.to_representation(restaurant) for restaurant in queryset]
                return Response(serialized_data)
            else:
                raise Http404("Data not found")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request_data, *args, **kwargs):
        serializer = CreateRestaurantSerializer(data=request_data.data)

        if serializer.is_valid():
            restaurant = RestaurantService.register_restaurant(restaurant_data=serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RestaurantMenuView(APIView):
    def get(self, request_data, *args, **Kwargs):
        rest_id = self.kwargs.get('rest_id')
        restaurant = RestaurantService.get_restaurant_menu(rest_id=rest_id)
        print(restaurant)
        serializer = RestaurantMenuSerializer(restaurant)
        if serializer.is_valid:
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemView(APIView):
    permission_classes = [IsStaff]
    def get(self, request_data, *args, **kwargs):
        try:
            serializer = SearchRestaurantItems(data=request_data.query_params)

            if serializer.is_valid():
                queryset = ItemService.get_item(attributes=serializer.validated_data)
                if queryset:
                    serialized_data = [serializer.to_representation(item) for item in queryset]
                    return Response(serialized_data)
                else:
                    raise Http404("No Data Found")
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NotImplementedError:
            return Response({'errors': 'Not Implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    def post(self, request_data, *args, **kwargs):
        serializer = CreateItemSerializer(data=request_data.data)

        if (serializer.is_valid()):
            item = ItemService.add_item(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request_data, *args, **kwargs):
        print(request_data.data)
        serializer = DeleteItemSerializer(data=request_data.data)

        if (serializer.is_valid()):
            print()
            item = ItemService.remove_item(request_data.data.get('item_id'))
            if item:
                return Response({'deleted': item}, status=status.HTTP_200_OK)
            else:
                return Response({'deleted': item}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)