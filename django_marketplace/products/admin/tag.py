from django.contrib import admin

from products.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name",
    list_display_links = "pk", "name",
    ordering = "pk",
    search_fields = "name",
