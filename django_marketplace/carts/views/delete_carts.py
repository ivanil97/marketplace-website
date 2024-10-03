from django.shortcuts import redirect

from products.models import SellerPrice
from carts.models import Cart


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(id=cart_id)
        product = SellerPrice.objects.get(id=cart.sellerprice.id)

        product.count_products += cart.quantity # При удалении товара из корзинв количество товара в SellerPrice увеличичвается
        cart.delete()
    else:
        cart = request.session.get('cart', {})
        product = SellerPrice.objects.get(id=cart_id)

        str_key = str(cart_id)
        product.count_products += request.session['cart'][str_key]['quantity']

        # На самом деле мы товар из сессии не удаляем а помечаем его спец-флагом "deleted"
        request.session['cart'][str_key]['deleted'] = True
        request.session['cart'] = cart

    product.save()
    return redirect("carts:cart")
