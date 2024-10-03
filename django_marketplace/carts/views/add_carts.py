from django.shortcuts import redirect

from products.models import SellerPrice
from ..models import Cart


def add_cart(request, sellerprice_id, count=1):
    product = SellerPrice.objects.get(id=sellerprice_id)

    if request.method == 'POST':
        count = int(request.POST.get('amount', None))
    if product.count_products < count:
        count = product.count_products
    if product.count_products == 0:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, sellerprice=product).first()

        if cart:
            cart.quantity += count
            cart.save()
        else:
            Cart.objects.create(user=request.user, sellerprice=product, quantity=count)
    else:
        cart = request.session.get('cart', {})
        str_key = str(sellerprice_id)

        if str_key in cart:
            cart[str_key]['quantity'] += count

            # Если ранее товар был удален из сессии то при добавлении этого же товара опять, меняем флаг deleted
            if cart[str_key].get('deleted'):
                cart[str_key]['quantity'] -= count
                cart[str_key]['deleted'] = False
        else:
            cart[str_key] = {'quantity': count}

        request.session['cart'] = cart

    product.count_products -= count # При добавлении товара в корзину количество товара в SellerPrice уменьшается
    product.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
