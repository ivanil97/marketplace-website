from products.models.product import Product
from products.models.review import Review
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


def get_reviews_for_product(product_id, page_number=1, per_page=5):
    reviews = Review.objects.filter(detail_product_id=product_id)
    paginator = Paginator(reviews, per_page)
    return paginator.get_page(page_number)


def add_review_to_product(product_id, user, comment):
    product = get_object_or_404(Product, id=product_id)
    review = Review(detail_product=product, user=user, comment=comment)
    review.save()
    return review
