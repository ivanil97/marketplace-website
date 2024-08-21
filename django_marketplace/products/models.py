from django.db import models


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


def get_categories() -> list[Categories]:
    data_categories = [
        {
            "pk": 1,
            "name": "Телевизоры",
            "slug": "TV",
            "description": "Новые телевизоры",
            "icon": "assets/img/icons/departments/1.svg",
            "archived": False,
            "parent": [2, 1],
            "discounts": 1
        },
        {
            "pk": 2,
            "name": "Компьютеры",
            "slug": "computers",
            "description": "Новые компьютеры",
            "icon": "assets/img/icons/departments/2.svg",
            "archived": False,
            "parent": [2, 1],
            "discounts": 1
        },
        {
            "pk": 3,
            "name": "phones",
            "slug": 3,
            "description": "Новые смартфоны",
            "icon": "assets/img/icons/departments/3.svg",
            "archived": True,
            "parent": [2, 1],
            "discounts": 1
        },
        {
            "pk": 4,
            "name": "Прочая бытовая техника",
            "slug": "another",
            "description": "Новая бытовая техника",
            "icon": "assets/img/icons/departments/4.svg",
            "archived": True,
            "parent": [2, 1],
            "discounts": 1
        },
    ]
    return [Categories(**category) for category in data_categories if not category["archived"]]
