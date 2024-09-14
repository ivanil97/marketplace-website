from django.db import models
from mptt.models import TreeForeignKey


class Product(models.Model):
    """
    Модель товара.
    Атрибуты:
        name (str): Название товара.
        slug (str): Слаг товара.
        description (str): Описание товара.
        archived (bool): Указатель на архивацию товара.
        category: Древовидная структура связи с родительской категорией.
    """
    name = models.CharField(
        max_length=256,
        verbose_name="Наименование"
    )
    slug = models.SlugField(max_length=150)
    description = models.TextField(null=False, blank=True)
    archived = models.BooleanField(default=False)
    category = TreeForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория'
    )
    sort_index = models.IntegerField(default=1)
    quantity_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name
