from django.contrib import admin

from products.models.feature import Feature


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"
    #prepopulated_fields = {"slug": ("name",)}
    ordering = "name",
    search_fields = "name",

    # def description_short(self, obj: Category) ->str:
    #     if len(obj.description) < 50:
    #         return obj.description
    #     return obj.description[:50] + "..."