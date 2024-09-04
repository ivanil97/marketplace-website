from products.models.product import Product
from django.db.models import Avg
from django.http import HttpRequest, HttpResponse


class ProductContext(Product):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = Product.objects.get(slug='product_slug')
        description_full: list = product['description'].splitlines()
        description_short: list = description_full[:3]
        seller_price = Product.objects.annotate(Avg('sellerprices__price')).all()
        first_image = product.images[0]
        context = {
            "description_full": description_full,
            "description_short": description_short,
            "seller_price": seller_price,
            "first_image": first_image,
        }
        return context
