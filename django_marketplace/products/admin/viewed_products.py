from django.contrib import admin
from products.models import ViewedProducts

@admin.register(ViewedProducts)
class ViewedProductsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'viewed_at')
    search_fields = ('user__email', 'product__name')
    list_filter = ('viewed_at',)
    ordering = ('-viewed_at',)
