from django.urls import path
from .views import OrdersCreateView, FetchOrderView

urlpatterns = [
    path('order/checkout/', OrdersCreateView.as_view(), name='order-checkout'),
    path('order/get/', FetchOrderView.as_view(), name='orders-get')
]