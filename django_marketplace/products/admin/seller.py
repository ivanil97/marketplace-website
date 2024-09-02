from django.contrib import admin

from products.models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description", "email", "phone", "address",
    list_display_links = "pk", "name"
    ordering = "pk",
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}

    def description(self, obj: Seller) -> str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + "..."
