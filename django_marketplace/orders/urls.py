from django.urls import path
from .views_dir import OrderProcessView, OrderPaymentView, ProgressPaymentView
from orders.views import OrderDetailView, add_order

app_name = "orders"

urlpatterns = [
    path('oreder=<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/', add_order, name='order'),
    path('proceed/', OrderProcessView.as_view(), name='order_proceed'),
    path('proceed/<int:pk>/payment', OrderPaymentView.as_view(), name='order_payment'),
    path('proceed/<int:pk>/payment_progress', ProgressPaymentView.as_view(), name='payment_progress'),
]