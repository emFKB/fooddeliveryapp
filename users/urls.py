from django.urls import path
from .views import UserAPIView

urlpatterns = [
    path('signup/', UserAPIView.as_view(), name='user-signup'),
    path('search/', UserAPIView.as_view(), name='user-details'),
    path('update/<int:pk>', UserAPIView.as_view(), name='update-user')
]