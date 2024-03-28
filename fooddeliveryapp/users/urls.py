from django.urls import path
from .views import CreateUserAPIView, LoginUserView, RoleView, PermissionView, RolePermissionView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), name='user-signup'),
    path('search/', CreateUserAPIView.as_view(), name='user-details'),
    path('update/', CreateUserAPIView.as_view(), name='update-user'),
    path('login/', LoginUserView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('roles/', RoleView.as_view(), name='create-role'),
    path('permissions/', PermissionView.as_view(), name='create-permission'),
    path('role-permissions/', RolePermissionView.as_view(), name='assign-permissions-to-role'),

]