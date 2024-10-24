import enum
from django.db.models import Avg, Count, Sum, Min, Max
from products.models import Product, SellerPrice
from products.forms import SearchForm


class ProductListEnum(enum.Enum):
    POP_ASC = 'quantity_sold'
    POP_DEC = '-quantity_sold'
    PR_ASC = 'auto_seller_price'
    PR_DEC = '-auto_seller_price'
    REV_ASC = 'rev_count'
    REV_DEC = '-rev_count'
    DATE_ASC = 'created_at'
    DATE_DEC = '-created_at'
    NONE = '1'


def filter_queryset(request, form=None):
    """
    Фильтрует набор продуктов на основе параметров запроса и формы.

    :param request: HTTP-запрос.
    :param form: Форма для фильтрации продуктов.
    :return: Отфильтрованный набор продуктов.
    """
    queryset = Product.objects.prefetch_related(
        "tags", "images", "seller_price", "features"
    ).annotate(
        auto_seller_price=Avg('seller_price__price'),
        rev_count=Count('review'),
        quantity=Sum('seller_price__count_products'),
    )

    category_id = request.GET.get('category')
    curr_sort = request.GET.get('sort', 'auto_seller_price')

    if form and form.is_valid():
        price = form.cleaned_data.get('price')
        title = form.cleaned_data.get('name')
        in_stock = form.cleaned_data.get('in_stock')
        if title:
            queryset = queryset.filter(name__icontains=title)

        if price:
            price_range = price.split(';')
            queryset = queryset.filter(
                auto_seller_price__range=(price_range[0], price_range[1])
            )
        if in_stock:
            queryset = queryset.filter(quantity__gt=0)

    if category_id:
        queryset = queryset.filter(category_id=category_id)

    if curr_sort != '1':
        queryset = queryset.order_by(curr_sort)

    return queryset.all()


def get_context_data(request, products):
    """
    Формирует контекст для отображения списка продуктов.

    :param request: HTTP-запрос.
    :param products: Набор продуктов для отображения.
    :return: Словарь с контекстом для шаблона.
    """
    curr_sort = request.GET.get('sort', 'auto_seller_price')
    price_range = SellerPrice.objects.aggregate(Min('price'), Max('price'))
    min_price = price_range['price__min'] or 0
    max_price = price_range['price__max'] or 0
    context = {
        'products': products,
        'POP_ASC': ProductListEnum.POP_ASC,
        'POP_DEC': ProductListEnum.POP_DEC,
        'PR_ASC': ProductListEnum.PR_ASC,
        'PR_DEC': ProductListEnum.PR_DEC,
        'REV_ASC': ProductListEnum.REV_ASC,
        'REV_DEC': ProductListEnum.REV_DEC,
        'DATE_ASC': ProductListEnum.DATE_ASC,
        'DATE_DEC': ProductListEnum.DATE_DEC,
        'NONE': ProductListEnum.NONE,
        'curr_sort': curr_sort,
        'form': SearchForm(request.POST or None),
        'min_price': min_price,
        'max_price': max_price,
    }
    if 'form' in context and context['form'].is_valid():
        price = context['form'].cleaned_data.get('price')
        if price:
            price_range = price.split(';')
            context['price_from'] = price_range[0]
            context['price_to'] = price_range[1]
    return context
