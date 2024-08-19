from django.urls import path
from . import views as v

urlpatterns = [
    path('list_menu/', v.context_category, name="menu_categories"),
    path('products/<slug:category>/', v.stub_page_products, name="get_products")
]
