from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from products.models import Discount


@admin.action(description="Archived discounts")
def mark_archived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    query.update(archived=True)


@admin.action(description="Unarchived discounts")
def mark_unarchived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    query.update(archived=False)


@admin.action(description="Make inactive discounts")
def mark_inactive(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    query.update(is_active=False)


@admin.action(description="Make active discounts")
def mark_active(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    query.update(is_active=True)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
        mark_active,
        mark_inactive,
    ]
    list_display = (
        "pk",
        "action_scheme",
        "percent",
        "description",
        "from_date",
        "to_date",
        "is_active",
        "archived",
    )
    list_display_links = "pk", "percent",
    ordering = "percent",
    search_fields = "description", "products",

    def description(self, obj: Discount) -> str:
        return obj.description if len(obj.description) < 50 else obj.description[:50] + "..."
