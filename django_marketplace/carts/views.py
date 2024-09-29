from django.db.models import Prefetch
from django.shortcuts import render
from products.models import Product, ProductImage, Discount
from .models import Cart


def users_cart(request):
    """Сервис для просмотра списка товаров в корзине"""
    one_image_queryset = ProductImage.objects.order_by('id')[:1]
    one_discount_queryset = Discount.objects.order_by('id')[:1]
    carts = Cart.objects.filter(user=request.user.id).prefetch_related(
        Prefetch('sellerprice__product__images', queryset=one_image_queryset, to_attr='one_image'),
        Prefetch('sellerprice__product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
    )
    context = {
        "carts": carts,
    }
    return render(request, "templates_cart/cart.html", context)
