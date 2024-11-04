from typing import Dict

from django.db.models import Prefetch
from django.http import HttpRequest

from carts.models import Cart
from products.models import SellerPrice, Discount


def get_cart_data(request: HttpRequest) -> Dict:
    """
    Функция получает данные корзины пользователя на основе его статуса аутентификации.
    Функция проверяет, аутентифицирован ли пользователь:
    - Если аутентифицирован, она извлекает данные из корзины пользователя
    - Если не аутентифицирован, она извлекает данные из сессии пользователя

    Функция создает словарь, содержащий два ключа:
    - 'cart_items': Queryset элементов корзины или цен продавцов, в зависимости от аутентификации пользователя.
    - 'cart_products': Список продуктов, связанных с элементами корзины.

    :param request: Объект HTTP-запроса, содержащий информацию о пользователе и сессии.
    :type request: HttpRequest
    :return: Словарь, содержащий элементы корзины и продукты.
    :return: Dict
    """
    one_discount_queryset = Discount.objects.filter(is_active=True)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user.id)
        cart_items = carts.prefetch_related(
            Prefetch('sellerprice__product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
        )
        cart_products = [i_cart.sellerprice.product for i_cart in carts]
        cart = {
            'cart_items': cart_items,
            'cart_products': cart_products
        }

    else:
        cart_ids = [id_k for id_k, value_k in request.session.get('cart', {}).items() if
                    not value_k.get('deleted')]

        cart_items = SellerPrice.objects.filter(pk__in=cart_ids).prefetch_related(
            Prefetch('product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
        )

        cart_products = [i_cart.product for i_cart in cart_items]
        cart = {
            'cart_items': cart_items,
            'cart_products': cart_products
        }

    return cart
