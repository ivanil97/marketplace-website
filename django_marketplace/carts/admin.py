from django.contrib import admin
from django.db.models import QuerySet
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = "pk", "username", "price_product", "quantity", "created",
    list_display_links = "pk", "username",
    ordering = "quantity",
    search_fields = "username",

    def get_queryset(self, request) -> QuerySet:
        query = (
            super().get_queryset(request).
            select_related("user").
            select_related("sellerprice")
        )
        return query

    def username(self, obj: Cart):
        return obj.user.first_name

    def price_product(self, obj: Cart):
        return f"{obj.sellerprice.price} RUB"
