from django.contrib import admin

from products.models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description", "email", "phone", "address",
    list_display_links = "pk", "name",
    ordering = "name",
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}

    def description(self, obj: Seller) -> str:
        return obj.description if len(obj.description) < 50 else obj.description[:50] + "..."
