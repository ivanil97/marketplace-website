from django.urls import path

from .views import add_order

app_name = "orders"

urlpatterns = [
    path('order/', add_order, name='order'),
]
