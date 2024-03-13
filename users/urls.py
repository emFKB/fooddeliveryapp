from django.urls import path
from .views import UserAPIView, LoginUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', UserAPIView.as_view(), name='user-signup'),
    path('search/', UserAPIView.as_view(), name='user-details'),
    path('update/<int:pk>', UserAPIView.as_view(), name='update-user'),
    path('login/', LoginUserView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]