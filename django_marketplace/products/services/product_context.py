from products.models.product import Product
from products.services.review_service import get_reviews_for_product


def product_context(product: Product, **kwargs) -> dict:
    product = Product.objects.get(slug='product_slug')
    description_full: list = product['description'].splitlines()
    description_short: list = description_full[:3]
    first_image = product.images[0]
    reviews = get_reviews_for_product(**kwargs)
    context = {
        "description_full": description_full,
        "description_short": description_short,
        "first_image": first_image,
        "reviews": reviews,
    }
    return context
