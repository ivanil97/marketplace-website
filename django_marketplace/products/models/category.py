from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


def category_icon_directory_path(
        instance: "Category",
        filename: str) -> str:
    return "categories/category_{pk}/icon/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Category(MPTTModel):
    """
    Модель категории товара.
    Атрибуты:
        name (str): Название категории.
        slug (str): Слаг категории.
        description (str): Описание категории.
        icon (str): Изображение категории.
        archived (bool): Указатель на архивацию категории.
        parent: Древовидная структура связи с родительской категорией.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )
    slug = models.SlugField(max_length=150)
    description = models.TextField(
        null=False, blank=True
    )
    icon = models.ImageField(
        null=True, blank=True,
        upload_to="category_icon_directory_path"
    )
    archived = models.BooleanField(default=False)
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='children',
        db_index=True,
        verbose_name='Parent category'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse(
            'products_list',
            kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
