from django.core.cache.utils import make_template_fragment_key
from django.views.generic import DetailView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from products.services.product_context import product_context
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ReviewForm
from .services.review_service import add_review_to_product
from .models.product import Product
from .models.review import Review
from django.db.models import Avg


class ProductDetailView(DetailView):
    template_name = "templates_products/product_template.html"
    queryset = Product.objects.prefetch_related(
        "tags", "images",
        "seller_price", "features").annotate(
        auto_seller_price=Avg('seller_price__price'
                              ))
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        context_new = product_context(self.object, page_number=page_number)
        context.update(context_new)
        return context


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'templates_products/review_create.html'

    def form_valid(self, form):
        product_slug = self.kwargs['slug']
        user = self.request.user
        comment = form.cleaned_data['comment']
        add_review_to_product(slug=product_slug, user=user, comment=comment)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'slug': self.kwargs['slug']})


@receiver(post_save, sender=Product)
def clear_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("product_detail")
    cache.delete(key)
    print(f"Cache cleared for key: {key}")