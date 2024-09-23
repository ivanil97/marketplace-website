from django.db import models


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

    class Meta:
        db_table: str = "basket"
        verbose_name: str = "Cart"
        verbose_name_plural: str = "Carts"

    def __str__(self):
        return f"Корзина № {self.pk} - {self.user.first_name}"
