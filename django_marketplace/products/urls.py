from django.urls import path, include
from django.conf import settings
from .views import *

app_name = "products"

urlpatterns = [
    path('catalog/', ProductsListView.as_view(), name="products_list"),
    path('<slug:slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('<slug:slug>/add-review/', ReviewCreateView.as_view(), name='review_create'),
]

if settings.DEBUG:
    urlpatterns = [
                      path('__debug__/', include("debug_toolbar.urls")),
                  ] + urlpatterns
