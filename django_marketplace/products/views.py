from django.core.cache.utils import make_template_fragment_key
from django.views.generic import DetailView
from products.models.product import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from products.services import ProductContext


class ProductDetailView(DetailView):
    template_name = "templates_products/product_template.html"
    queryset = Product.objects.prefetch_related("tags", "images", "reviews", "sellerprices", "features")
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = ProductContext()
        context.update(context_new)
        return context


@receiver(post_save, sender=Product)
def clear_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("product_detail",)
    cache.delete(key)
