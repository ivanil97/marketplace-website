from django.urls import path, include
from django.conf import settings
app_name = "products"

urlpatterns = [
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include("debug_toolbar.urls")),
    ] + urlpatterns
