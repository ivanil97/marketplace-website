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
    """
    Архивирование скидок.
    Все выбранные скидки будут отмечены как архивные.
    """
    query.update(archived=True)


@admin.action(description="Unarchived discounts")
def mark_unarchived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    """
    Удаление скидок из архива.
    Все выбранные скидки будут отмечены как активные и не архивные.
    """
    query.update(archived=False)


@admin.action(description="Make inactive discounts")
def mark_inactive(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    """
    Деактивация скидок.
    Выбранные скидки будут помечены как неактивные.
    """
    query.update(is_active=False)


@admin.action(description="Make active discounts")
def mark_active(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    """
    Активация скидок.
    Выбранные скидки будут активированы и доступны для использования.
    """
    query.update(is_active=True)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения скидок в административном интерфейсе.
    Определены действия по архивированию, активации/деактивации скидок.
    """
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
    list_display_links = ("pk", "percent",)
    ordering = ("percent",)
    search_fields = ("description", "products__name",)

    def description(self, obj: Discount) -> str:
        """
        Отображение первых 50 символов описания скидки в списке скидок.
        """
        return obj.description if len(obj.description) < 50 else obj.description[:50] + "..."
