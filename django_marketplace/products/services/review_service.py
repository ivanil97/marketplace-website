from .models.product import Product
from .models.reviw import Review
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


def get_reviews_for_product(product_id, page_number=1, reviews_per_page=5):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.order_by("-date")
    paginator = Paginator(reviews, reviews_per_page)
    page_obj = paginator.get_page(page_number)
    return page_obj


def add_review_to_product(product_id, user, comment):
    product = get_object_or_404(Product, id=product_id)
    review = Review(detail_product=product, user=user, comment=comment)
    review.save()
    return review
