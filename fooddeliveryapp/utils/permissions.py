from rest_framework import permissions
from fooddeliveryapp.services import AuthService

class IsAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        return AuthService.authorize(token, request.path, request.method)