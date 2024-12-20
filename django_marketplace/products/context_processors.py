from django.db.models import Count, Q
from django.http import HttpRequest

from .models import Category


def list_categories(request: HttpRequest) -> dict:
    categories: list[Category] = Category.objects.prefetch_related('children').annotate(
        product_count=Count('products', filter=Q(products__archived=False))
    ).filter(
        product_count__gt=0,
        archived=False
    )
    return {"list_categories": categories}
