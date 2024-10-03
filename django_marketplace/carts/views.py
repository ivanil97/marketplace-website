import json

from django.db.models import Prefetch
from django.db.models.fields.files import ImageFieldFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from products.models import SellerPrice, ProductImage, Discount
from .models import Cart
from django.forms.models import model_to_dict
from pydantic import BaseModel
from uuid import UUID


class CartModel(BaseModel):
    id: int
    sellerprice: "SellerPriceModel"
    quantity: int


class DiscountsModel(BaseModel):
    id: int
    percent: int


class ImgModel(BaseModel):
    id: int
    #image: str


class ProductModel(BaseModel):
    id: int
    name: str
    description: str
    one_image: list[ImgModel]
    one_discount: list[DiscountsModel]


class SellerPriceModel(BaseModel):
    id: int
    product: ProductModel
    count_products: int
    price: float


def users_cart(request):
    one_image_queryset = ProductImage.objects.order_by('id')[:1]
    one_discount_queryset = Discount.objects.order_by('id')[:1]

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user.id)
        carts = carts.prefetch_related(
            Prefetch('sellerprice__product__images', queryset=one_image_queryset, to_attr='one_image'),
            Prefetch('sellerprice__product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
        )
        n = [CartModel.model_validate(book, from_attributes=True).dict() for book in carts]
        for col in n:
            col['sellerprice']['id'] = col['id']

        print("Результат с картами", n)
    else:
        list_id_ses = [int(col) for col in request.session['cart'].keys()]
        carts = SellerPrice.objects.filter(pk__in=list_id_ses).prefetch_related(
            Prefetch('product__images', queryset=one_image_queryset, to_attr='one_image'),
            Prefetch('product__discounts', queryset=one_discount_queryset, to_attr='one_discount')
        )

        n = [SellerPriceModel.model_validate(book, from_attributes=True).dict() for book in carts]

        print("Результат с картами", n)

        # f = [model_to_dict(obj, fields=["product"]) for obj in carts]
        # print(f)


    context = {"carts": carts}
    return render(request, "templates_cart/cart.html", context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(id=cart_id)
        product = SellerPrice.objects.get(id=cart.sellerprice.id)

        product.count_products += cart.quantity
        cart.delete()
    else:
        cart = request.session.get('cart', {})
        product = SellerPrice.objects.get(id=cart_id)

        str_key = str(cart_id)
        product.count_products += request.session['cart'][str_key]['quantity']
        cart.pop(str_key)
        request.session['cart'] = cart

    product.save()
    return redirect("carts:cart")


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
        else:
            cart[str_key] = {'quantity': count}

        request.session['cart'] = cart

    product.count_products -= count
    product.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


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

    if f > quantity:
        product.count_products += 1
    else:
        product.count_products -= 1

    product.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
