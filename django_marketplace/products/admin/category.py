from django.contrib import admin

from products.models.category import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "parent"
    list_display_links = "pk", "name",
    prepopulated_fields = {"slug": ("name",)}
    ordering = "name",
    search_fields = "name", "description",

    def description_short(self, obj: Category) ->str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + "..."
