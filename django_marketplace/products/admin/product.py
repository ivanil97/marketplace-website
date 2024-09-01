from django.contrib import admin

from products.models.product import Product
from products.models import Tag
from products.models import Feature


class TagInline(admin.TabularInline):
    model = Product.tags.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]
    list_display = "pk", "name", "description_short",
    list_display_links = "pk", "name",
    prepopulated_fields = {"slug": ("name", )}
    ordering = "name", "pk",
    search_fields = "name", "description",

    def description_short(self, obj: Product) ->str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + "..."
