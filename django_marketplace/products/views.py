from django.http import HttpResponse
from django.http.request import HttpRequest

from django.shortcuts import render


class Categories:
    """Фейковая временная модель категорий"""
    def __init__(self, pk, name, slug, description, icon, archived, parent, discounts):
        self.pk = pk,
        self.name = name,
        self.slug = slug
        self.descr = description
        self.icon = icon
        self.archived = archived
        self.parent = parent
        self.discount = discounts

    def __str__(self):
        return f"Categories № {self.pk[0]}. Name: {self.name[0]}"


data_categories = [
    {
        "pk": 1,
        "name": "Телевизоры",
        "slug": 1,
        "description": "Новые телевизоры",
        "icon": "assets/img/icons/departments/1.svg",
        "archived": False,
        "parent": [2, 1],
        "discounts": 1
    },
]


def main_page(request: HttpRequest):
    """View функция для отображения основной страницы """
    # Запрос к базе данных
    categories = []
    for cat in data_categories:
        """Наполнение меню списком доступных категорий"""
        categories.append(Categories(**cat))
    return render(request, "products/django-frontend/about.html", context={"object": categories})


def stub_page_products(request: HttpRequest):
    # Получаем Товары по категории
    return HttpResponse(request, "Товары по заданной категории")
