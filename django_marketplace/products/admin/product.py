from django.contrib import admin

from products.models import (
    Tag,
    Seller,
    Product,
    Discount,
    SellerPrice,
    ProductFeature,
)


class SellerFilter(admin.SimpleListFilter):
    """Кастомный фильтр для фильтрации товаров по продавцу"""

    title = 'Sellers'
    parameter_name = 'sellers'

    def lookups(self, request, model_admin):
        sellers = Seller.objects.all()
        return [(seller.pk, seller.name) for seller in sellers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(seller_price__seller__id=self.value())
        return queryset


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
    max_num = 1
    verbose_name = "Choice seller and price"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        DiscountInline,
        SellerPriceInline,
        TagInline,
        ProductFeatureInline,
    ]
    list_display = "pk", "name", "description", "count", "discount", "price", "category", "archived"
    list_display_links = "pk", "name",
    list_filter = "category", "archived", SellerFilter,
    prepopulated_fields = {"slug": ("name",)}
    ordering = "name", "pk",
    search_fields = "name", "description",

    def get_queryset(self, request):
        query = (
            super().get_queryset(request).
            select_related("category").
            prefetch_related("discounts").
            prefetch_related("seller_price")
        )
        return query

    def description(self, obj: Product) -> str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + "..."

    def category(self, obj: Product):
        return obj.category.name

    def discount(self, obj: Product):
        f = obj.discounts.filter(archived=False) # n + 1
        if f:
            return f"{f[0].percent} %"
        return "no discount"

    def archived(self, obj: Product):
        f = obj.seller_price.filter(archived=False)  # n + 1
        if f:
            return f"{f[0].archived}"
        return f"{obj.name} is not archived"

    def price(self, obj: Product):
        f = obj.seller_price.filter(archived=False)  # n + 1
        if f:
            return f"{f[0].price}"
        return "price is not stuff"

    def count(self, obj: Product):
        f = obj.seller_price.filter(archived=False, count_products__gt=0) # n + 1
        if f:
            return f"{f[0].count_products} шт."
        return f"products are not have"
