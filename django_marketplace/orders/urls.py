from django.urls import path
from .views import OrderDetailView

from .views import add_order

app_name = "orders"

urlpatterns = [
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/', add_order, name='order'),
]