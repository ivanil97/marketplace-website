from django.contrib import admin
from products.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "pk", "detail_product", "user", "date"
    list_display_links = "pk", "detail_product", "user", "date"
