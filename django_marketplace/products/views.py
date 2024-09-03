from django.core.cache.utils import make_template_fragment_key
from django.db.models import Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from products.models.product import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache


class ProductDetailView(DetailView):
    template_name = "templates_products/product_template.html"
    queryset = Product.objects.prefetch_related("tags").select_related("images", "reviews", "sellerprices", "features")
    context_object_name = "product"


class ProductDescView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = Product.objects.get(pk=pk)
        description_full: list = product['description'].splitlines()
        description_short: list = description_full[:3]
        seller_price = Product.objects.all().annotate(Avg('sellerprices__price'))
        first_image = Product.objects.select_related("images")[0]
        context = {
            "description_full": description_full,
            "description_short": description_short,
            "seller_price": seller_price,
            "first_image": first_image,
        }
        return render(request, "templates_products/product_template.html", context=context)


@receiver(post_save, sender=Product)
def clear_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("product_detail",)
    cache.delete(key)
