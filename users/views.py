from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import UserService
from .serializers import (FetchUserSerializer, CreateUserSerializer, UpdateUserSerializer,
                          CreateUserResponseSerializer)
from django.http import Http404
from collections import OrderedDict
from rest_framework_simplejwt.tokens import RefreshToken

# class UserController(generics.CreateAPIView, generics.RetrieveAPIView, generics.RetrieveUpdateAPIView):
#     serializer_class = FetchUserSerializer
#     def get_object(self):
#         UserService.get_user(self.kwargs.get('pk'))

#     def perform_create(self, serializer = CreateUserSerializer):
#         user = UserService.create_user(serializer.validated_data)
#         serializer.instance = user

class UserAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        if self.request.method in ["GET", "PUT"]:
            return [permissions.IsAuthenticated()]
        
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
            user = UserService.create_user(serializer.validated_data)
            response_data = {'user_id':user.user_id, 'uid':user.uid, 'email':user.email, 'is_staff':user.is_staff, 'created_at':user.created_at}
            response_serializer = CreateUserResponseSerializer(data=response_data)
            if (response_serializer.is_valid()):
                return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user = UserService.get_user(user_id=kwargs.get('pk'))
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = UserService.get_user(OrderedDict(email=email)).first()
        except user.DoesNotExist:
            return Response({'error': 'User does not exist'}, status==status.HTTP_200_OK)
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_id': user.user_id,
                'uid': user.uid,
                'username': user.username,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)