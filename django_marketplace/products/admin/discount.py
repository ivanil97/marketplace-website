from django.contrib import admin

from products.models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = "pk", "action_scheme", "percent", "description_short", "from_date", "to_date", "is_active", "archived"
    list_display_links = "pk", "percent",
    ordering = "percent",
    search_fields = "description", "products",

    def description_short(self, obj: Discount) -> str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + "..."
