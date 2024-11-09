from typing import Dict, Union

from django import template
from django.http import HttpRequest
from typing_extensions import Optional

from carts.models import Cart
from orders.models import OrderItem

from products.models import SellerPrice, Discount

register = template.Library()


@register.simple_tag()
def get_quantity_order(request: HttpRequest, cart_key: int) -> int:
    """
    Шаблонный тег для получения количества выбранного товара из сессии в процессе заказа
    Args:
        request (HttpRequest): request, содержащий информацию о текущем пользователе.
        cart_key (int): ID продукта в корзине
    """
    return request.session.get('cart')[str(cart_key)]['quantity']


@register.simple_tag()
def price_discount_order(request: HttpRequest, cart_item: Union[Cart, SellerPrice, OrderItem]) -> Optional[Dict[str, float]]:
    """
    Шаблонный тег для подсчета стоимости товара с учетом скидки или без нее в процессе заказа и просмотра детальной страницы заказа

    Args:
        request (HttpRequest): request, содержащий информацию о текущем пользователе.
        cart_item (Union[Cart, SellerPrice, OrderItem]): Элемент корзины, в зависимости от статуса аутентификации пользователя может быть
        объектом Cart, SellerPrice или OrderItem

    Returns:
        Optional[Dict[str, float]]: Словарь с ценой со скидкой и старой ценой, если скидка применима,
        иначе None. Ключи словаря:
            - 'discount_price': цена товара с учетом максимальной скидки.
            - 'old_price': исходная цена товара без скидки.
    """
    if isinstance(cart_item, OrderItem):
        price = cart_item.seller_price.price
        discount = Discount.objects.filter(is_active=True)
    elif request.user.is_authenticated:
        price = cart_item.sellerprice.price
        discount = cart_item.sellerprice.product.one_discount
    else:
        price = cart_item.price
        discount = cart_item.product.one_discount

    if discount:
        max_dis = max(discount, key=lambda obj: obj.percent)
        discount_price = round(price - price * max_dis.percent / 100, 2)
        return {"discount_price": discount_price, "old_price": price}

    return None
