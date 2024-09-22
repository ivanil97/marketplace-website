from products.models.product import Product
from products.services.review_service import get_reviews_for_product
# from .review_service import get_reviews_for_product



def product_context(product: Product, **kwargs) -> dict:
    description_full: list = product.description.splitlines()
    description_short: list = description_full[:3]
    first_image = product.images.first()
    page_number = kwargs.get("page_number", 1)
    reviews = get_reviews_for_product(product_slug=product.pk, page_number=page_number)
    context = {
        "description_full": description_full,
        "description_short": description_short,
        "first_image": first_image,
        "reviews": reviews,
    }
    return context
