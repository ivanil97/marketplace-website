from django.db.models import Avg
from django.contrib import messages

from products.models.product import Product


def get_comparison_list(request, limit=3):
    product_id = request.session.get('compare_list', [])
    products = Product.objects.filter(id__in=product_id).prefetch_related('images', 'seller_price').annotate(
        auto_seller_price=Avg('seller_price__price'))[:limit]
    return products


def add_to_comparison(request, slug, limit=3):
    product = Product.objects.get(slug=slug)
    compare_list = request.session.get('compare_list', [])

    if product.id in compare_list:
        messages.warning(request, f"{product.name} уже добавлен в список для сравнения.")
        return

    if len(compare_list) >= limit:
        messages.warning(request, f"Вы можете сравнивать только {limit} товара(ов) одновременно.")
        return

    compare_list.append(product.id)
    request.session['compare_list'] = compare_list
    messages.success(request, f"{product.name} был добавлен в список для сравнения.")


def remove_from_comparison(request, slug):
    product = Product.objects.get(slug=slug)
    compare_list = request.session.get('compare_list', [])

    if product.id in compare_list:
        compare_list.remove(product.id)
        request.session['compare_list'] = compare_list


def get_comparison_count(request):
    return len(request.session.get('compare_list', []))


def get_comparison_context(request, limit=3):
    products = get_comparison_list(request, limit)

    context = {
        'products': products,
        'count': len(products),

    }
    return context
