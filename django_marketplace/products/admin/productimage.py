from django.contrib import admin

from products.models.productimage import ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "pk", "product",
    list_display_links = "pk", "product",
    ordering = "pk", "product",
    search_fields = "product",
