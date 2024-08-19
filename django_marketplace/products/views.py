from django.http.request import HttpRequest
from .models import get_categories
from django.shortcuts import render


def context_category(request: HttpRequest):
    list_categories = get_categories()
    return render(request, "products/about.html", context={"list_categories": list_categories})


def stub_page_products(request: HttpRequest, category: str):
    return render(request, "products/products.html", context={"category": category})
