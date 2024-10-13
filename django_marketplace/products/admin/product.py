import os

from django.contrib import admin, messages
from django.db.models import Prefetch, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from core.settings import BASE_DIR
from core.task import task_is_active, create_task_load_file
from products.models import (
    Tag,
    Seller,
    Product,
    Discount,
    SellerPrice,
    ProductFeature,
    ProductImage,
)


class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage


@admin.action(description="Archived products")
def mark_archived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    query.update(archived=True)


@admin.action(description="Unarchived products")
def mark_unarchived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        query: QuerySet
) -> None:
    query.update(archived=False)


class SellerFilter(admin.SimpleListFilter):
    title = 'Sellers'
    parameter_name = 'sellers'

    def lookups(self, request, model_admin) -> list:
        return [(seller.pk, seller.name) for seller in Seller.objects.all()]

    def queryset(self, request, queryset) -> QuerySet:
        return queryset.filter(seller_price__seller__id=self.value()) if self.value() else queryset


class TagInline(admin.TabularInline):
    model = Product.tags.through
    verbose_name = "Choice tags"


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    verbose_name = "Choice features"


class DiscountInline(admin.TabularInline):
    model = Product.discounts.through
    max_num = 1
    verbose_name = "Choice discount"


class SellerPriceInline(admin.TabularInline):
    model = SellerPrice
    # max_num = 1
    verbose_name = "Choice seller and price"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        DiscountInline,
        SellerPriceInline,
        TagInline,
        ProductFeatureInline,
        ProductImageInline,
    ]
    list_display = (
        "pk",
        "name",
        "description",
        "count",
        "discount",
        "price",
        "category",
        "archived",
    )
    list_display_links = "pk", "name",
    list_filter = "category", "archived", SellerFilter,
    prepopulated_fields = {"slug": ("name",)}
    ordering = "name", "pk",
    search_fields = "name", "description",
    list_per_page = 40
    change_list_template = "templates_adminpanel/product_change_list.html"

    def process_import(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            return render(request, "templates_adminpanel/product_import_from_json.html")
        if task_is_active():
            self.message_user(
                request,
                "Import already is working. Can't start new one.",
                level=messages.WARNING
            )
        else:
            path_to_json = os.path.join(BASE_DIR, 'import')
            create_task_load_file.delay(path_to_json)
            self.message_user(request, "Import started.")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import_products_from_json/', self.process_import, name='import_product'),
        ]
        return custom_urls + urls

    def get_queryset(self, request) -> QuerySet:
        query = (
            super().get_queryset(request).
            select_related("category").
            prefetch_related(Prefetch("discounts", to_attr="discount")).
            prefetch_related(Prefetch("seller_price", to_attr="seller"))
        )
        return query

    def description(self, obj: Product) -> str:
        return obj.description if len(obj.description) < 50 else obj.description[:50] + "..."

    def category(self, obj: Product) -> str:
        return obj.category.name

    def discount(self, obj: Product) -> str:
        return f"{obj.discount[0].percent} %" if obj.discount != [] else "No discount"

    def price(self, obj: Product) -> str:
        return f"{obj.seller[0].price}" if obj.seller != [] else "price is not stuff"

    def count(self, obj: Product) -> str:
        return f"{obj.seller[0].count_products} шт." if obj.seller != [] else "products are not have"
