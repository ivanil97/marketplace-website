from django.db import models


class Tag(models.Model):
    """
    Теги товаров
    Атрибуты:
        name (str): Название тега.
        products: поле для связи тега с товарами.
    """
    name = models.CharField(max_length=100, verbose_name="Name")
    products = models.ManyToManyField("Product", related_name="tags")

    def __str__(self):
        return self.name
