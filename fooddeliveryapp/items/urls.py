from django.urls import path
from .views import RestaurantView, ItemView, RestaurantMenuView

urlpatterns = [
    path('restaurant/register/', RestaurantView.as_view(), name='register-restaurant'),
    path('restaurant/search/', RestaurantView.as_view(), name='get-restaurant-by-attr'),
    path('restaurant/<int:rest_id>/items/', RestaurantMenuView.as_view(), name='get-restaurant-menu'),
    path('item/add/', ItemView.as_view(), name='add-item'),
    path('item/search/', ItemView.as_view(), name='get-item-by-attr'),
    path('item/delete/', ItemView.as_view(), name='remove-item'),
]