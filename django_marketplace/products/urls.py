from django.urls import path, include
from django.conf import settings
from products.views_dir.viewed_products import (add_product_to_viewed,
                                                remove_product_from_viewed,
                                                get_viewed_products,
                                                get_viewed_count)



from .views import ProductDetailView, ProductsListView

app_name = "products"

urlpatterns = [
    path('viewed/add/<int:product_id>/', add_product_to_viewed, name='add_product_to_viewed'),
    path('viewed/remove/<int:product_id>/', remove_product_from_viewed, name='remove_product_from_viewed'),
    path('viewed/', get_viewed_products, name='get_viewed_products'),
    path('viewed/count/', get_viewed_count, name='get_viewed_count'),
    path('catalog/', ProductsListView.as_view(), name="products_list"),
    path('<slug:slug>/', ProductDetailView.as_view(), name="product_detail"),

]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include("debug_toolbar.urls")),
    ] + urlpatterns
