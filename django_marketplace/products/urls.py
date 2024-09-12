from django.urls import path, include
from django.conf import settings
from products.views import product_views



from .views import ProductDetailView, ProductsListView

app_name = "products"

urlpatterns = [
    path('viewed/add/<int:product_id>/', product_views.add_product_to_viewed, name='add_product_to_viewed'),
    path('viewed/remove/<int:product_id>/', product_views.remove_product_from_viewed, name='remove_product_from_viewed'),
    path('viewed/', product_views.get_viewed_products, name='get_viewed_products'),
    path('viewed/count/', product_views.get_viewed_count, name='get_viewed_count'),
    path('catalog/', ProductsListView.as_view(), name="products_list"),
    path('<slug:slug>/', ProductDetailView.as_view(), name="product_detail"),

]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include("debug_toolbar.urls")),
    ] + urlpatterns
