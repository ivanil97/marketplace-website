from products.models.product import Product
from products.services.review_service import get_reviews_for_product


def product_context(product: Product, **kwargs) -> dict:
    product = Product.objects.get(slug='product_slug')
    description_full: list = product['description'].splitlines()
    description_short: list = description_full[:3]
    first_image = product.images[0]
    page_number = kwargs.get("page_number")
    reviews_per_page = kwargs.get("reviews_per_page")
    reviews = get_reviews_for_product(product_id=product.pk, page_number=page_number, reviews_per_page=reviews_per_page)
    context = {
        "description_full": description_full,
        "description_short": description_short,
        "first_image": first_image,
        "reviews": reviews,
    }
    return context
