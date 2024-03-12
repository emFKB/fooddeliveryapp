from django.urls import path
from .views import OrdersCreateView

urlpatterns = [
    path('order/checkout/', OrdersCreateView.as_view(), name='order-checkout'),
]