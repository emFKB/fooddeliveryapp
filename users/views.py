from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import UserService
from .serializers import FetchUserSerializer, CreateUserSerializer, UpdateUserSerializer
from django.contrib.auth.hashers import make_password
from django.http import Http404

# class UserController(generics.CreateAPIView, generics.RetrieveAPIView, generics.RetrieveUpdateAPIView):
#     serializer_class = FetchUserSerializer
#     def get_object(self):
#         UserService.get_user(self.kwargs.get('pk'))

#     def perform_create(self, serializer = CreateUserSerializer):
#         user = UserService.create_user(serializer.validated_data)
#         serializer.instance = user

class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = FetchUserSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = UserService.get_user(request_data=serializer.validated_data)
            if queryset:
                serialized_data = [serializer.to_representation(user) for user in queryset]
                return Response(serialized_data)
            else:
                raise Http404("User not found")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            hashed_pass = make_password(password)
            serializer.validated_data['password'] = hashed_pass
            user = UserService.create_user(serializer.validated_data)
            response_data = serializer.data.copy()
            del response_data['password']
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user = UserService.get_user(user_id=kwargs.get('pk'))
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)