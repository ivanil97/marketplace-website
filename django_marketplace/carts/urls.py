from django.urls import path

from .views import users_cart

app_name = "carts"

urlpatterns = [
    path('cart/', users_cart, name='cart'),
]
