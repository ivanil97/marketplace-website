from django.db import models


class Feature(models.Model):
    """
    Модель характеристик товара.
    Атрибуты:
        name (str): Название характеристики.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
