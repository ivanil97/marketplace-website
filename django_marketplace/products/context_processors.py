from django.http import HttpRequest

from .models import Category


def list_categories(request: HttpRequest) -> dict:
    categories: list[Category] = Category.objects.filter(archived=False)
    return {"list_categories": categories}
