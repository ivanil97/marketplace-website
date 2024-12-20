from django.db import models

from products.models import Category


class StaticBanner(models.Model):
    """
    Модель для хранения информации о статических баннерах.

    Атрибуты:
    - title (CharField): Заголовок баннера.
    - image (ImageField): Изображение баннера.
    - link (URLField): Ссылка для перехода при клике на баннер.
    - is_active (BooleanField): Флаг активности баннера.
    - description (TextField): Описание баннера. Необязательное поле.
    - price (DecimalField): Цена, связанная с баннером. Необязательное поле.
    - created_at (DateTimeField): Дата создания баннера.
    - updated_at (DateTimeField): Дата последнего обновления баннера.
    """
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    image = models.ImageField(upload_to='banners/static/', verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', verbose_name="Категория")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статический баннер"
        verbose_name_plural = "Статические баннеры"

    def __str__(self):
        '''Для наглядного наименования записей в админке'''
        return self.title