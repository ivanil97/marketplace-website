import json

from django.shortcuts import redirect
from products.models import SellerPrice
from carts.models import Cart


def edit_cart(request):
    body = json.loads(request.body)
    cart_id = body.get("cart_id")
    quantity = body.get("quantity")

    if request.user.is_authenticated:
        cart = Cart.objects.get(id=cart_id)
        product = SellerPrice.objects.get(id=cart.sellerprice.id)
        f = cart.quantity

        cart.quantity = quantity
        cart.save()
    else:
        product = SellerPrice.objects.get(id=cart_id)
        cart = request.session.get('cart', {})
        str_key = str(product.id)
        f = cart[str_key]['quantity']

        cart[str_key]['quantity'] = quantity
        request.session['cart'] = cart

    # Если количество которое пришло с frontend больше предыдущего увеличиваем на 1 иначе уменьшаем в SellerPrice
    if f > quantity:
        product.count_products += 1
    else:
        product.count_products -= 1

    product.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
