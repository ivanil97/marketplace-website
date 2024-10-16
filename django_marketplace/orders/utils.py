from typing import List, Dict

from django.http import HttpRequest

from products.models import SellerPrice


def get_cart_from_request(request: HttpRequest) -> List[Dict]:
    """
    Функция для создания списка товаров в корзине, если она была создана неавторизированным пользователем,
    возвращает список словарей формата {"quantity": количество товара, "sellerprice": Queryset[SellerPrice]}
    :return: List[Dict]
    """
    carts_data = request.session.get('cart', {})
    cart_ids = [id_k for id_k, value_k in request.session.get('cart', {}).items() if
                not value_k.get('deleted')]

    cart_items = SellerPrice.objects.filter(pk__in=cart_ids).prefetch_related('product__images')

    cart = [
        {'quantity': carts_data[str(cart_item.id)]['quantity'],
         'sellerprice': cart_item}
        for cart_item in cart_items
    ]

    return cart