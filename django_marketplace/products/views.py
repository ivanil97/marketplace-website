from constance import config
from django.core.cache.utils import make_template_fragment_key
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin

from products.services.product_context import product_context
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.generic import TemplateView

from products.forms import ReviewForm, SearchForm

from django.db.models.signals import post_save
from products.models.review import Review
from django.db.models import Count, Min, Max, Avg
from django.db.models import Prefetch

from comparisons.services.comparison_service import *
from products.services.products_list_services import filter_queryset, get_context_data
from products.services.review_service import add_review_to_product
from users.services.viewed_products_service import ViewedProductsService
from products.services.index_services import get_slider_banners, get_static_banners, get_popular_items, get_limited_items
from products.models import Product
from products.models import Discount
from products.models import Review


class ProductDetailView(DetailView):
    template_name = "templates_products/product_template.html"
    queryset = Product.objects.prefetch_related(
        "tags", "images",
        "seller_price",
        "features",
        Prefetch("discounts", to_attr="discount", queryset=Discount.objects.filter(is_active=True)),
        Prefetch("seller_price", to_attr="seller")
    ).annotate(auto_seller_price=Avg('seller_price__price'))

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

    def get_object(self, queryset=None):
        obj = cache.get(f'product_detail_{self.kwargs["slug"]}')
        if not obj:
            obj = super().get_object()
            cache.set(f'product_detail_{self.kwargs["slug"]}', obj, 60 * 15)  # 15 минут
        return obj


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'templates_products/product_template.html'
    login_url = 'user/login/'

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
        return redirect('products:product_detail', slug=product_slug)

    def get_success_url(self):
        if self.kwargs['slug']:
            return reverse_lazy('products:product_detail', kwargs={'slug': self.kwargs['slug']})
        else:
            # Если slug пустой, перенаправляем на другую страницу или показываем ошибку
            return reverse_lazy('products:products_list')  # или другая подходящая страница



class ProductsListView(ListView):
    """
    Представление для отображения списка продуктов.
    """

    model = Product
    template_name = "templates_products/products_list.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        """
        Получает отфильтрованный набор продуктов на основе запроса.

        :return: Отфильтрованный набор продуктов.
        """
        if self.request.method == 'POST':
            form = SearchForm(self.request.POST)
            if form.is_valid():
                return filter_queryset(self.request, form)
        return filter_queryset(self.request)

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос.

        :param request: HTTP-запрос.
        :return: Ответ на запрос.
        """
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Получает контекст для шаблона.

        :param kwargs: Дополнительные аргументы.
        :return: Словарь с контекстом для шаблона.
        """
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()

        filter_context = get_context_data(self.request, products)
        context.update({
            'filter_context': filter_context,
        })
        return context


class HomeView(TemplateView):
    """
    Представление для главной страницы. Отображает баннеры слайдера и статические баннеры.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        Формирует контекст для передачи данных в шаблон.
        Проверяет наличие данных в базе данных и избегает ошибок при отсутствии данных.
        """
        context = super().get_context_data(**kwargs)

        # Получаем баннеры и популярные товары
        context['slider_banners'] = get_slider_banners() or []
        context['static_banners'] = get_static_banners() or []
        context['popular_items'] = get_popular_items() or []

        # Получаем ограниченное предложение и проверяем на наличие данных
        limited_item_day, limited_items, end_of_day = get_limited_items()
        float(limited_item_day.price)
        discount_price = round(limited_item_day.price - (limited_item_day.price * config.LIMITED_DISCOUNT) / 100, 2)

        # Проверяем, есть ли данные о лимитированном товаре
        if limited_item_day is None:
            context['limited_item_day'] = None
            context["limited_item_discount"] = None
            context['limited_items'] = []
            context['end_of_day'] = end_of_day
        else:
            context['limited_item_day'] = limited_item_day
            context["limited_item_discount"] = discount_price

            context['limited_items'] = limited_items
            context['end_of_day'] = end_of_day

        return context


class DiscountListView(ListView):
    model = Discount
    template_name = 'templates_products/discounts_list.html'
    context_object_name = 'discounts'

    def get_queryset(self):
        return Discount.objects.filter(is_active=True, archived=False).order_by('-to_date')


@receiver(post_save, sender=Product)
def clear_cache(sender, instance, **kwargs):
    key = make_template_fragment_key("product_detail")
    cache.delete(key)
    print(f"Cache cleared for key: {key}")
