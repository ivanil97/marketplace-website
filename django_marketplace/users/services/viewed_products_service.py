from datetime import datetime
from products.models import ViewedProducts
from products.models import Product
from django.core.exceptions import ObjectDoesNotExist


class ViewedProductsService:
    """
    Сервис для работы со списком просмотренных товаров.
    """

    @staticmethod
    def add_to_viewed(user, product_id):
        """
        Добавляет товар в список просмотренных пользователем товаров.
        Если товар уже был в списке, перемещает его на первое место.
        """
        try:
            product = Product.objects.get(id=product_id)
            viewed_product, created = ViewedProducts.objects.get_or_create(user=user, product=product)

            if not created:
                # Если товар уже есть в списке, обновляем время просмотра
                viewed_product.viewed_at = datetime.now()
                viewed_product.save()
        except Product.DoesNotExist:
            raise ObjectDoesNotExist(f'Товар с ID {product_id} не найден.')

    @staticmethod
    def remove_from_viewed(user, product_id):
        """
        Удаляет товар из списка просмотренных.
        """
        try:
            product = Product.objects.get(id=product_id)
            ViewedProducts.objects.filter(user=user, product=product).delete()
        except Product.DoesNotExist:
            raise ObjectDoesNotExist(f'Товар с ID {product_id} не найден.')

    @staticmethod
    def is_viewed(user, product_id):
        """
        Проверяет, находится ли товар в списке просмотренных.
        """
        return ViewedProducts.objects.filter(user=user, product_id=product_id).exists()

    @staticmethod
    def get_viewed_products(user, limit=20):
        """
        Возвращает список просмотренных товаров пользователя.
        """
        return ViewedProducts.objects.filter(user=user).order_by('-viewed_at')[:limit]

    @staticmethod
    def get_viewed_count(user):
        """
        Возвращает количество просмотренных товаров пользователя.
        """
        return ViewedProducts.objects.filter(user=user).count()
