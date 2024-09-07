from django.core.cache.utils import make_template_fragment_key
from django.views.generic import DetailView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from products.services import product_context
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import ReviewForm
from .services.review_service import get_reviews_for_product, add_review_to_product
from .models.product import Product
from .models.review import Review
from django.db.models import Avg


class ProductDetailView(DetailView):
    template_name = "templates_products/product_template.html"
    queryset = Product.objects.prefetch_related(
        "tags", "images",
        "sellerprices", "features").annotate(
        seller_price=Avg('sellerprices__price'
                         ))
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = product_context(self.object, page_number=1, reviews_per_page=5)
        # context_new = product_context(self.object, self.object_id, page_number=1, reviews_per_page=5)
        context.update(context_new)
        return context


@receiver(post_save, sender=Product)
def clear_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("product_detail",)
    cache.delete(key)


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = ''

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        user = self.request.user
        comment = form.cleaned_data['comment']
        add_review_to_product(product_id=product_id, user=user, comment=comment)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.kwargs['product_id']})
