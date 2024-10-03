from django.db import models

from products.models import Discount


class CartQuerySet(models.QuerySet):

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    """
    Модель корзины.
    Атрибуты:
        user (User): Связь с моделью User.
        sellerprice (SellerPrice): Связь с моделью SellerPrice.
        quantity (int): Количество выбранного пользователем товара.
        created (datetime): Время добавления товара в корзину.
    """
    user = models.ForeignKey(
        "users.User",
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name="user_cart",
        verbose_name="Пользователь"
    )
    sellerprice = models.ForeignKey(
        "products.SellerPrice",
        on_delete=models.CASCADE,
        related_name="seller_cart",
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    session_key = models.CharField(max_length=32, blank=True, null=True)
    objects = CartQuerySet.as_manager()

    class Meta:
        db_table: str = "basket"
        verbose_name: str = "Cart"
        verbose_name_plural: str = "Carts"

    def __str__(self):
        if self.user:
            return f"Корзина № {self.pk} - {self.user.first_name}"
        return f"Корзина № {self.pk} - Анонимный пользователь"
