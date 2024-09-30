from django.urls import path

from .views import users_cart, delete_cart, add_cart

app_name = "carts"

urlpatterns = [
    path('cart/', users_cart, name='cart'),
    path('delete-cart/<int:cart_id>/', delete_cart, name='delete_cart'),
    path('add-cart/<int:sellerprice_id>/', add_cart, name='add_cart'),
]
