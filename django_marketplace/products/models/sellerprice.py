from django.db import models

from products.models import Product


class SellerPrice(models.Model):
    """
    Модель цены товара
    Атрибуты:
        is_limited (bool): Флаг, указывающий является ли цена ограниченной по времени
        archived (bool): Флаг активности цены
        created_at (DateTimeField): Дата создания баннера
        product_id (ForeignKey): Продукт, с которым цена связана связью Many-To-One
        price (Decimal): Цена на товар
        count_products (int): Количество товаров
    """
    is_limited = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    count_products = models.IntegerField()

