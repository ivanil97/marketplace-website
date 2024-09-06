from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from products.models.category import Category


@admin.action(description="Archived categories")
def mark_archived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    query.update(archived=True)


@admin.action(description="Unarchived categories")
def mark_unarchived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    query.update(archived=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    actions = [
        mark_unarchived,
        mark_archived,
    ]
    list_display = "pk", "name", "description", "parent", "archived",
    list_display_links = "pk", "name",
    prepopulated_fields = {"slug": ("name",)}
    ordering = "name",
    search_fields = "name", "description",

    def description(self, obj: Category) -> str:
        return obj.description if len(obj.description) < 50 else obj.description[:50] + "..."
