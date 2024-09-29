from django import template

from carts.models import Cart
from django.db.models import Prefetch

from products.models import Discount

register = template.Library()


def solve_total_price(carts):
    # Дополнительная функция для подсчета полной стоимости всех товаров
    total_price = 0
    for col in carts:
        price = col.sellerprice.price
        if col.sellerprice.product.one_discount:
            discount = col.sellerprice.product.one_discount[0].percent
            p = round((price - price * discount / 100) * col.quantity, 2)
        else:
            p = price * col.quantity
        total_price += p
    return total_price


@register.simple_tag()
def price_discount(cart):
    # Тег для подсчета стоимости товара с учетом скидки и без скидки
    price = cart.sellerprice.price
    old_price = price * cart.quantity
    if cart.sellerprice.product.one_discount:
        discount = cart.sellerprice.product.one_discount[0].percent
        p = round((price - price * discount / 100) * cart.quantity, 2)
        return {"price_discount": p, "old_price": old_price}
    else:
        return {"old_price": old_price}


@register.simple_tag()
def quantity_products(request):
    # Тег для отображения количества товаров в корзине
    return Cart.objects.filter(user=request.user.id).total_quantity()


@register.simple_tag()
def total_price(request, carts):
    # Тег для отображения полной стимости товаров корзины в header
    if carts:
        # Этот блок отработает если пользователь перешел на страницу с корзиной
        return solve_total_price(carts)
    else:
        # Этот блок отработает если пользователь находится на других страницах магазина кроме страницы с корзиной
        one_discount_queryset = Discount.objects.order_by('id')[:1]
        carts = Cart.objects.filter(user=request.user.id).prefetch_related(
            Prefetch('sellerprice__product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
        )
        return solve_total_price(carts)
