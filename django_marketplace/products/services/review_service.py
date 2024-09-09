from products.models.product import Product
from products.models.review import Review
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


def get_reviews_for_product(product_id, page_number=1):
    reviews = Review.objects.filter(product__id=product_id)
    paginator = Paginator(reviews)
    page_obj = paginator.get_page(page_number)
    return page_obj


def add_review_to_product(product_id, user, comment):
    product = get_object_or_404(Product, id=product_id)
    review = Review(detail_product=product, user=user, comment=comment)
    review.save()
    return review
