from django import template

from carts.models import Cart, CartQuerySet
from django.db.models import Prefetch, QuerySet

from products.models import Discount, SellerPrice

from carts.utils import solve_total_price, prepare_data
from core.custom_querysets import one_discount_queryset


register = template.Library()


@register.simple_tag()
def price_discount(request, cart: dict) -> dict:
    """Шаблонный тег для подсчета стоимости товара с учетом скидки или без нее"""
    old_price: int = cart['sellerprice']["price"]
    if request.user.is_authenticated:
        quantity: int = cart['quantity']
        price: int = cart['sellerprice']["price"]
    else:
        quantity: int = request.session['cart'][str(cart['id'])]['quantity']
        price: int = cart['sellerprice']["price"]

    if quantity == 0:
        quantity: int = 1

    if cart['sellerprice']['product']['one_discount']:
        discount: dict = cart['sellerprice']['product']['one_discount']
        max_dis: dict = max(discount, key=lambda obj: obj.get("percent", 1))

        p: float = round((price - price * max_dis.get("percent", 1) / 100) * quantity, 2)
        old_price: float = round(old_price * quantity, 2)

        return {"price_discount": p, "old_price": old_price}
    else:
        old_price: float = round(old_price * quantity, 2)
        return {"old_price": old_price}


@register.simple_tag()
def quantity_products(request) -> int:
    """Шаблонный тег для отображения количества товаров в корзине"""
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user.id).total_quantity()
    else:
        return sum(value_k['quantity'] for value_k in request.session.get('cart', {}).values() if not value_k.get('deleted'))


@register.simple_tag()
def total_price(request, carts: CartQuerySet) -> dict:
    """Шаблонный тег для отображения полной стимости товаров корзины в header"""
    if carts:
        # Этот блок отработает если пользователь перешел на страницу с корзиной
        if request.user.is_authenticated:
            prepare: list[dict] = prepare_data(request, carts)
        else:
            prepare: list[dict] = prepare_data(request, carts)
        return solve_total_price(prepare)

    else:
        # Этот блок отработает если пользователь находится на других страницах магазина кроме страницы с корзиной
        if request.user.is_authenticated:
            carts: CartQuerySet = Cart.objects.filter(user=request.user.id).prefetch_related(
                Prefetch('sellerprice__product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
            )
            prepare: list[dict] = prepare_data(request, carts)
        else:
            list_id_ses: list[int] = [int(col) for col in request.session.get('cart', {}).keys()]
            carts: QuerySet = SellerPrice.objects.filter(pk__in=list_id_ses).prefetch_related(
                Prefetch('product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
            )
            prepare: list[dict] = prepare_data(request, carts)
        return solve_total_price(prepare)


@register.simple_tag()
def get_quantity(request, cart: dict) -> int:
    """Шаблонный тег для получения количества выбраного товара из сессии"""
    return request.session['cart'][str(cart['id'])]['quantity']


@register.simple_tag()
def get_url(request, lan: str) -> str:
    return f"/{lan}/{request.get_full_path()[4:]}"
