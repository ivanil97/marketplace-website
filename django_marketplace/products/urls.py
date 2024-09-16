from django.urls import path, include
from django.conf import settings

from .views import ProductDetailView, ReviewCreateView

app_name = "products"

urlpatterns = [
    path('<slug:slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('<slug:slug>/review/', ReviewCreateView.as_view(), name='review_create'),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include("debug_toolbar.urls")),
    ] + urlpatterns
