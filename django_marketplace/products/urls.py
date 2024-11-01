from django.urls import path, include
from django.conf import settings
from .views import *
from .views_dir import SaleView

app_name = "products"

urlpatterns = [
    path('discounts/', DiscountListView.as_view(), name='discounts_list'),
    path('catalog/', ProductsListView.as_view(), name="products_list"),
    path('catalog/sale/', SaleView.as_view(), name='sale_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('add-review/<slug:slug>/', ReviewCreateView.as_view(), name='review_create'),
]

if settings.DEBUG:
    urlpatterns = [
                      path('__debug__/', include("debug_toolbar.urls")),
                  ] + urlpatterns
