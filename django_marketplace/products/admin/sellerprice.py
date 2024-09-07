from django.contrib import admin

from products.models.sellerprice import SellerPrice

@admin.register(SellerPrice)
class SellerPriceAdmin(admin.ModelAdmin):
    list_display = "pk", "price", "product_id",
    list_display_links = "pk", "price", "product_id",
    ordering = "pk", "price", "product_id"
    search_fields = "pk", "price", "product_id"
