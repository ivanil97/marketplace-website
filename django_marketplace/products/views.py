from django.core.cache.utils import make_template_fragment_key
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.dispatch import receiver
from django.core.cache import cache
from products.services.product_context import product_context
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView

from products.forms import ReviewForm

from django.db.models.signals import post_save
from products.models.product import Product
from products.models.review import Review
from django.db.models import Avg
from django.db.models import Prefetch

from products.services.comparison_service import *
from products.services.review_service import add_review_to_product
from products.services.viewed_products_service import ViewedProductsService
from .index_services import get_slider_banners, get_static_banners, get_popular_items, get_limited_items


class ProductDetailView(DetailView):
    template_name = "templates_products/product_template.html"
    queryset = Product.objects.prefetch_related(
        "tags", "images",
        "seller_price", "features").prefetch_related(Prefetch("seller_price", to_attr="seller")).annotate(
        auto_seller_price=Avg('seller_price__price'
                              ))
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        context_new = product_context(self.object, page_number=page_number)
        context.update(context_new)

        """Добавление товара в список просмотренных"""
        user = self.request.user
        if user.is_authenticated:
            ViewedProductsService.add_to_viewed(user, self.object.id)

        return context


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'templates_products/review_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['product'] = product
        return context

    def form_valid(self, form):
        product_slug = self.kwargs['slug']
        user = self.request.user
        comment = form.cleaned_data['comment']
        add_review_to_product(slug=product_slug, user=user, comment=comment)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'slug': self.kwargs['slug']})


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
                auto_seller_price=Avg('seller_price__price')). \
                order_by('auto_seller_price').all().filter(category_id=category_id)
        else:
            queryset = self.model.objects.prefetch_related(
                "tags", "images",
                "seller_price", "features").annotate(
                auto_seller_price=Avg('seller_price__price')). \
                order_by('auto_seller_price').all()
        return queryset


class ComparisonListView(View):
    def get(self, request):
        limit = int(request.GET.get('limit', 3))
        context = get_comparison_context(request, limit)
        return render(request, 'templates_products/comparison_list.html', context)


class AddComparisonView(View):
    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        add_to_comparison(request, slug)
        return render(request, 'templates_products/comparison_list.html', get_comparison_context(request))

class RemoveFromComparisonView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        remove_from_comparison(request, product_id)
        return render(request, 'templates_products/comparison_list.html', get_comparison_context(request))

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


@receiver(post_save, sender=Product)
def clear_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("product_detail")
    cache.delete(key)
    print(f"Cache cleared for key: {key}")
