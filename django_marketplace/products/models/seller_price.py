from django.db import models


class SellerPrice(models.Model):
    """
    Промежуточная модель между моделью Product и Seller.
    Атрибуты:
        product (Product): Ссылка на модель Product.
        seller (Seller): Ссылка на модель Seller.
        price (float): Цена товара.
        is_limited (bool): Указатель на ограниченное количество товара.
        count_products (int): Количество товара.
        archived (bool): Указатель на архивацию товара.
        created_at (datetime): Время создания товара.
    """
    product = models.ForeignKey(
        "Product",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="seller_price"
    )
    seller = models.ForeignKey(
        "Seller",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="seller_user"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_limited = models.BooleanField(default=False)
    count_products = models.IntegerField(default=1)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seller {self.seller.name} | Product {self.product.name}"

    def display_price(self):
        return f"{self.price}" # Вывести с учетом скидки!!!
