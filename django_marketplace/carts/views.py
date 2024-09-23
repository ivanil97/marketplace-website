from django.db.models import Prefetch
from django.shortcuts import render
from products.models import Product


def users_cart(request):
    product = (
        Product.objects.
        select_related("category").
        prefetch_related(Prefetch("discounts", to_attr="discount")).
        prefetch_related(Prefetch("seller_price", to_attr="seller")).
        prefetch_related(Prefetch("images", to_attr="image")).
        filter(id__gt=5)
    )
    context = {"products": product}
    return render(request, "templates_cart/cart.html", context)
