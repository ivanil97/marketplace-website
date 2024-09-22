from django.urls import path, include
from django.conf import settings
from products.views_dir.viewed_products import (remove_product_from_viewed,
                                                get_viewed_products,
                                                get_viewed_count)

from .views import *

app_name = "products"

urlpatterns = [
    path('comparison/', ComparisonListView.as_view(), name='comparison_list'),
    path('comparison/remove/', RemoveFromComparisonView.as_view(), name='remove_from_comparison'),
    path('comparison/add/<slug:slug>/', AddComparisonView.as_view(), name='add_to_comparison'),

    path('viewed/remove/<int:product_id>/', remove_product_from_viewed, name='remove_product_from_viewed'),
    path('viewed/', get_viewed_products, name='get_viewed_products'),
    path('viewed/count/', get_viewed_count, name='get_viewed_count'),

    path('catalog/', ProductsListView.as_view(), name="products_list"),

    path('<slug:slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('<slug:slug>/add-review/', ReviewCreateView.as_view(), name='review_create'),
]

if settings.DEBUG:
    urlpatterns = [
                      path('__debug__/', include("debug_toolbar.urls")),
                  ] + urlpatterns