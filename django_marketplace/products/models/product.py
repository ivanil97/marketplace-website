from django.db import models
from mptt.models import TreeForeignKey


class Product(models.Model):
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
