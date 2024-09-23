from django.contrib import admin

from products.models import SellerPrice

@admin.register(SellerPrice)
class SellerPriceAdmin(admin.ModelAdmin):
    list_display = "pk", "price", "product", "seller", "is_limited"
    list_display_links = "pk", "price", "product", "seller"
    ordering = "pk", "price", "product", "seller"
    search_fields = "pk", "price", "product", "seller"
