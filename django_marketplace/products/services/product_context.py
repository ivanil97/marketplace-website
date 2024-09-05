from products.models.product import Product
from django.db.models import Avg
from django.http import HttpRequest, HttpResponse


def product_context(product: Product, **kwargs) -> dict:
    product = Product.objects.get(slug='product_slug')
    description_full: list = product['description'].splitlines()
    description_short: list = description_full[:3]
    first_image = product.images[0]
    context = {
        "description_full": description_full,
        "description_short": description_short,
        "first_image": first_image,
    }
    return context
