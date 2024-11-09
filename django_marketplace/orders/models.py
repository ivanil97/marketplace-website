from django.db import models
from django.conf import settings
from products.models import SellerPrice


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

    DELIVERY_OPTIONS = [
        ('ordinary', 'Обычная доставка'),
        ('express', 'Экспресс доставка'),
    ]

    PAYMENT_OPTIONS = [
        ('online', 'Онлайн картой'),
        ('someone', 'Онлайн со случайного чужого счета'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Не оплачен'),
        ('paid', 'Оплачен'),
        ('error', 'Ошибка оплаты')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
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
    city = models.CharField(
        blank=True,
        max_length=50,
        verbose_name='Город'
    )
    address = models.CharField(
        blank=True,
        max_length=100,
        verbose_name='Адрес'
    )
    delivery_option = models.CharField(
        default=DELIVERY_OPTIONS[0],
        max_length=20,
        choices=DELIVERY_OPTIONS,
    )
    payment_option = models.CharField(
        default=PAYMENT_OPTIONS[0],
        max_length=20,
        choices=PAYMENT_OPTIONS
    )
    payment_status = models.CharField(
        default='unpaid',
        max_length=20,
        choices=PAYMENT_STATUS
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.email}"

    def get_delivery_label(self):
        return dict(self.DELIVERY_OPTIONS).get(self.delivery_option, self.delivery_option)

    def get_payment_label(self):
        return dict(self.PAYMENT_OPTIONS).get(self.payment_option, self.payment_option)

    def get_payment_status_label(self):
        return dict(self.PAYMENT_STATUS).get(self.payment_status, self.payment_status)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Заказ'
    )
    seller_price = models.ForeignKey(
        SellerPrice,
        on_delete=models.CASCADE,
        related_name='seller_price',
        verbose_name='Цена'
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
