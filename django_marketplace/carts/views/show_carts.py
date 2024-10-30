from django.db.models import Prefetch
from django.shortcuts import render

from products.models import ProductImage, SellerPrice, Discount
from carts.models import Cart
from carts.serializers import serializer_data_user, serializer_data_session


def users_cart(request):
    one_image_queryset = ProductImage.objects.order_by('id')[:1]
    one_discount_queryset = Discount.objects.filter(is_active=True)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user.id)
        carts = carts.prefetch_related(
            Prefetch('sellerprice__product__images', queryset=one_image_queryset, to_attr='one_image'),
            Prefetch('sellerprice__product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
        )
        ready_data = serializer_data_user(carts)
    else:
        list_id_ses = [int(id_k) for id_k, value_k in request.session.get('cart', {}).items() if not value_k.get('deleted')]
        carts = SellerPrice.objects.filter(pk__in=list_id_ses).prefetch_related(
            Prefetch('product__images', queryset=one_image_queryset, to_attr='one_image'),
            Prefetch('product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
        )
        ready_data = serializer_data_session(carts)

    context = {"carts": carts, "list_data": ready_data}
    return render(request, "templates_cart/cart.html", context)
