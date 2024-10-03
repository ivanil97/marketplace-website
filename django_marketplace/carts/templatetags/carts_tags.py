from django import template

from carts.models import Cart
from django.db.models import Prefetch

from products.models import Discount, SellerPrice


register = template.Library()


def solve_total_price(carts):
    # Дополнительная функция для подсчета полной стоимости всех товаров
    total_price = 0
    for col in carts:
        price, discount, quantity = col['price'], col['discount'], col['quantity']
        if discount:
            p = round((price - price * discount[0].percent / 100) * col.quantity, 2)
        else:
            p = price * quantity
        total_price += p
    return total_price


def prepare_data(request, carts):
    if request.user.is_authenticated:
        prepare = [
            {
                "price": col.sellerprice.price,
                "discount": col.sellerprice.product.one_discount,
                "quantity": col.quantity
            }
            for col in carts
        ]
    else:
        prepare = [
            {
                "price": col.price,
                "discount": col.product.one_discount,
                "quantity": request.session['cart'][str(col.id)]['quantity']
            }
            for col in carts
        ]
    return prepare


@register.simple_tag()
def price_discount(request, cart):
    if request.user.is_authenticated:
        # Тег для подсчета стоимости товара с учетом скидки и без скидки
        price = cart.sellerprice.price
        old_price = price * cart.quantity
        if cart.sellerprice.product.one_discount:
            discount = cart.sellerprice.product.one_discount[0].percent
            p = round((price - price * discount / 100) * cart.quantity, 2)
            return {"price_discount": p, "old_price": old_price}
        else:
            return {"old_price": old_price}
    else:

        price = cart.price
        old_price = price * request.session['cart'][str(cart.id)]['quantity']
        if cart.product.one_discount:
            discount = cart.product.one_discount[0].percent
            p = round((price - price * discount / 100) * request.session['cart'][str(cart.id)]['quantity'], 2)
            return {"price_discount": p, "old_price": old_price}
        else:
            return {"old_price": old_price}


@register.simple_tag()
def quantity_products(request):
    # Тег для отображения количества товаров в корзине
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user.id).total_quantity()
    else:
        return sum(col['quantity'] for col in request.session.get('cart', {}).values())


@register.simple_tag()
def total_price(request, carts):
    # Тег для отображения полной стимости товаров корзины в header
    if carts:
        # Этот блок отработает если пользователь перешел на страницу с корзиной
        if request.user.is_authenticated:
            prepare = prepare_data(request, carts)
        else:
            prepare = prepare_data(request, carts)
        return solve_total_price(prepare)

    else:
        # Этот блок отработает если пользователь находится на других страницах магазина кроме страницы с корзиной
        one_discount_queryset = Discount.objects.order_by('id')[:1]
        if request.user.is_authenticated:
            carts = Cart.objects.filter(user=request.user.id).prefetch_related(
                Prefetch('sellerprice__product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
            )
            prepare = prepare_data(request, carts)
        else:
            list_id_ses = [int(col) for col in request.session.get('cart', {}).keys()]
            carts = SellerPrice.objects.filter(pk__in=list_id_ses).prefetch_related(
                Prefetch('product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
            )
            prepare = prepare_data(request, carts)
        return solve_total_price(prepare)


@register.simple_tag()
def get_quantity(data_dict, sellerprice_id):
    return data_dict[str(sellerprice_id)]['quantity']
