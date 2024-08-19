from django.urls import path
from . import views as v

urlpatterns = [
    path('list_menu/', v.main_page, name="menu_categories"),
    path('products/', v.stub_page_products, name="get_products")
]
