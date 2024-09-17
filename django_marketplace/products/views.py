from django.core.cache.utils import make_template_fragment_key
from django.views.generic import DetailView, ListView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from products.services.product_context import product_context
from django.urls import reverse_lazy
from django.views.generic import CreateView
from products.forms import ReviewForm
from products.services.review_service import add_review_to_product
from products.models.product import Product
from products.models.review import Review
from django.db.models import Avg
from django.db.models import Prefetch

from products.services.viewed_products_service import ViewedProductsService
import enum


class ProductDetailView(DetailView):
    template_name = "templates_products/product_template.html"
    queryset = Product.objects.prefetch_related(
        "tags", "images",
        "seller_price", "features").prefetch_related(Prefetch("seller_price", to_attr="seller")).annotate(
        auto_seller_price=Avg('seller_price__price'
                         ))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = product_context(self.object, page_number=1)
        context.update(context_new)

        """Добавление товара в список просмотренных"""
        user = self.request.user
        if user.is_authenticated:
            ViewedProductsService.add_to_viewed(user, self.object.id)

        return context


@receiver(post_save, sender=Product)
def clear_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("product_detail",)
    cache.delete(key)


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'templates_products/review_product.html'

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        user = self.request.user
        comment = form.cleaned_data['comment']
        add_review_to_product(product_id=product_id, user=user, comment=comment)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.kwargs['product_id']})


class ProductsListView(ListView):
    model = Product
    template_name = "templates_products/products_list.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        category_id = self.request.GET.get('category', None)
        print(category_id)
        if category_id:
            queryset = self.model.objects.prefetch_related(
            "tags", "images",
            "seller_price", "features").annotate(
            auto_seller_price=Avg('seller_price__price')).\
                order_by('auto_seller_price').all().filter(category_id=category_id)
        else:
            queryset = self.model.objects.prefetch_related(
            "tags", "images",
            "seller_price", "features").annotate(
            auto_seller_price=Avg('seller_price__price')).\
                order_by('auto_seller_price').all()
        return queryset


from django.views.generic import TemplateView
from .index_services import get_slider_banners, get_static_banners, get_popular_items, get_limited_items


class HomeView(TemplateView):
    """
    Представление для главной страницы. Отображает баннеры слайдера и статические баннеры.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        Формирует контекст для передачи данных в шаблон.
        """
        context = super().get_context_data(**kwargs)
        context['slider_banners'] = get_slider_banners()
        context['static_banners'] = get_static_banners()
        context['popular_items'] = get_popular_items()
        context['limited_item_day'] = get_limited_items()[0]
        context['limited_items'] = get_limited_items()[1]
        return context
