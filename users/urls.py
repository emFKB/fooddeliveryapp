from django.urls import path
from .views import UserAPIView, LoginUserView, RoleView, PermissionView, RolePermissionView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', UserAPIView.as_view(), name='user-signup'),
    path('search/', UserAPIView.as_view(), name='user-details'),
    path('update/', UserAPIView.as_view(), name='update-user'),
    path('login/', LoginUserView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('roles/', RoleView.as_view(), name='create-role'),
    path('permissions/', PermissionView.as_view(), name='create-permission'),
    path('role-permissions/', RolePermissionView.as_view(), name='assign-permissions-to-role'),

]