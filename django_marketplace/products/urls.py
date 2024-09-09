from django.urls import path, include
from django.conf import settings

from .views import ProductDetailView

app_name = "products"

urlpatterns = [
    path('<int:pk>', ProductDetailView.as_view(), name="product_detail")
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include("debug_toolbar.urls")),
    ] + urlpatterns
