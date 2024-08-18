from django.contrib import admin

from products.models.product import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short",
    list_display_links = "pk", "name",
    prepopulated_fields = {"slug": ("name", )}
    ordering = "name", "pk",
    search_fields = "name", "description",

    def description_short(self, obj: Product) ->str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + "..."
