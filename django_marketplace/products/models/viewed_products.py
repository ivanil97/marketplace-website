from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class ViewedProducts(models.Model):
    """
    Модель для хранения списка просмотренных товаров пользователем.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_products', verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='Время просмотра')

    class Meta:
        verbose_name = 'Просмотренный товар'
        verbose_name_plural = 'Просмотренные товары'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.email} - {self.product.name}'
