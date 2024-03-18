from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import UserService
from .serializers import (FetchUserSerializer, CreateUserSerializer, UpdateUserSerializer,
                          CreateUserResponseSerializer, RoleSerializer, PermissionSerializer)
from django.http import Http404
from collections import OrderedDict
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, Permission
from .permissions import IsAuthorized

class UserAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        if self.request.method in ["GET", "PUT"]:
            return [IsAuthorized()]
        
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
            response_data = {'user_id':user.user_id, 'uid':user.uid, 'email':user.email, 'is_staff':user.is_staff, 'created_at':user.created_at, 'roles': [role.role_id for role in user.roles.all()]}
            response_serializer = CreateUserResponseSerializer(data=response_data)
            if (response_serializer.is_valid()):
                return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user = UserService.get_user(user_id=request.user.user_id)
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
            refresh['username'] = user.username
            refresh['email'] = user.email
            return Response({
                'user_id': user.user_id,
                'uid': user.uid,
                'username': user.username,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
class RoleView(APIView):
    permission_classes = [IsAuthorized]
    def post(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PermissionView(APIView):
    permission_classes = [IsAuthorized]
    def post(self, request, *args, **kwargs):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RolePermissionView(APIView):
    permission_classes = [IsAuthorized]
    def post(self, request, *args, **kwargs):
        role_id = request.data.get("role_id")
        permission_ids = request.data.get("permission_ids", [])
        try:
            role = Role.objects.get(role_id=role_id)
            permissions = Permission.objects.filter(permission_id__in=permission_ids)
            role.permissions.set(permissions)
            return Response({"status": "permissions updated"}, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
