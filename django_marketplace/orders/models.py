from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    """
    Модель заказа пользователя.
    Атрибуты:
        user (ForeignKey): Пользователь, который сделал заказ.
        products (ManyToManyField): Товары, включенные в заказ.
        total_price (DecimalField): Общая стоимость заказа.
        status (CharField): Статус заказа.
        created_at (DateTimeField): Дата создания заказа.
        updated_at (DateTimeField): Дата последнего обновления заказа.
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processed', 'Обрабатывается'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    products = models.ManyToManyField(
        Product,
        related_name='orders',
        verbose_name='Товары'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Общая стоимость'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.email}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
