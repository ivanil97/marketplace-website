import json

from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from products.models import SellerPrice, ProductImage, Discount
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


def delete_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()
    product = SellerPrice.objects.get(id=cart.sellerprice.id)
    product.count_products += quantity
    product.save()
    return redirect("carts:cart")


# 1) Добавлять товары если пользователь анонимный???
# 2) Добавить значения количества выбраного товара
def add_cart(request, sellerprice_id, count=1):
    product = SellerPrice.objects.get(id=sellerprice_id)

    if request.method == 'POST':
        count = int(request.POST.get('amount', None))
    if product.count_products < count:
        count = product.count_products
    if product.count_products == 0:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.user.is_authenticated:

        carts = Cart.objects.filter(user=request.user, sellerprice=product)
        if carts.exists():
            cart = carts.first()

            if cart:
                cart.quantity += count
                cart.save()
                product.count_products -= count
                product.save()
        else:
            Cart.objects.create(user=request.user, sellerprice=product, quantity=count)

            product.count_products -= count
            product.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        print(request.user)
        return redirect(request.META.get('HTTP_REFERER', '/'))
        # carts = Cart.objects.filter(
        #     session_key=request.session.session_key,
        #     sellerprice=product
        # )
        # if carts.exists():
        #     cart = carts.first()
        #     if cart:
        #         cart.quantity += 1
        #         cart.save()
        # else:
        #     Cart.objects.create(
        #         session_key=request.session.session_key,
        #         product=product,
        #         quantity=1
        #     )


def edit_cart(request):
    body = json.loads(request.body)
    cart_id = body.get("cart_id")
    quantity = body.get("quantity")
    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()

    #updated_quantity = cart.quantity

    # one_image_queryset = ProductImage.objects.order_by('id')[:1]
    # one_discount_queryset = Discount.objects.order_by('id')[:1]
    # carts = Cart.objects.filter(user=request.user.id).prefetch_related(
    #     Prefetch('sellerprice__product__images', queryset=one_image_queryset, to_attr='one_image'),
    #     Prefetch('sellerprice__product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
    # )
    # cart_items_html = render_to_string(
    #     "templates_cart/cart.html",
    #     {"carts": carts},
    #     request=request
    # )
    # response_data = {
    #     "cart_items_html": cart_items_html,
    #     "quantity_deleted": updated_quantity,
    # }
    # return JsonResponse(response_data)
    return redirect(request.META.get('HTTP_REFERER', '/'))
