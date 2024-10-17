"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views_dir. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views_dir
    1. Add an import:  from my_app import views_dir
    2. Add a URL to urlpatterns:  path('', views_dir.home, name='home')
Class-based views_dir
    1. Add an import:  from other_app.views_dir import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from products.views import HomeView


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('product/', include('products.urls')),
    path('user/', include('users.urls')),
    path('cart/', include('carts.urls')),
    path('', HomeView.as_view(), name='home'),
    path('comparison/', include('comparisons.urls')),
    path('order/', include('orders.urls')),
    path('i18n/', include('django.conf.urls.i18n'))
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
