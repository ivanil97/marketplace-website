from products.models.product import Product
from products.models.review import Review
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


def get_reviews_for_product(product_slug, page_number=1, per_page=5):
    reviews = Review.objects.filter(detail_product_id=product_slug).order_by('-date')
    paginator = Paginator(reviews, per_page)
    return paginator.get_page(page_number)


def add_review_to_product(slug, user, comment):
    product = get_object_or_404(Product, slug=slug)
    review = Review(detail_product=product, user=user, comment=comment)
    review.save()
    return review
