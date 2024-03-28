from rest_framework import permissions
#from fooddeliveryapp.services import AuthService
from  ..servicefactory import ServiceFactory

class IsAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        auth_service = ServiceFactory.get_service('permission_auth')
        return auth_service.authorize(token, request.path, request.method)