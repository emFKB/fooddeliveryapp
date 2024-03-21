from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from fooddeliveryapp.servicefactory import ServiceFactory
from .serializers import (RoleSerializer, PermissionSerializer)
from .models import Role, Permission
from .permissions import IsAuthorized

class UserAPIView(APIView):
    user_service = ServiceFactory.get_service('user')

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        if self.request.method in ["GET", "PUT"]:
            return [IsAuthorized()]
        
    def get(self, request, *args, **kwargs):
        
        response= self.user_service.fetch_user(request=request)
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        response = self.user_service.create_user(request=request)
        return Response(response, status=status.HTTP_201_CREATED)
        
    def put(self, request, *args, **kwargs):
        response= self.user_service.update_user(request=request)
        return Response(response, status=status.HTTP_201_CREATED)
    
class LoginUserView(APIView):
    user_service = ServiceFactory.get_service('user')

    def post(self, request, *args, **kwargs):
        response= self.user_service.login_user(request=request)
        return Response(response, status=status.HTTP_200_OK)
        
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
