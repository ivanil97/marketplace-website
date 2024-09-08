from django.db import models
from mptt.models import TreeForeignKey
from django.urls import reverse


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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})
