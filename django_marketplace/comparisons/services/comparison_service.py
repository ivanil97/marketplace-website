from products.models.product import Product

from django.db.models import Avg


def get_comparison_list(request, limit=3):
    product_id = request.session.get('compare_list', [])
    products = Product.objects.filter(id__in=product_id).prefetch_related('images', 'seller_price').annotate(
        auto_seller_price=Avg('seller_price__price'))[:limit]
    return products


def add_to_comparison(request, slug):
    product = Product.objects.get(slug=slug)
    compare_list = request.session.get('compare_list', [])
    message = ""

    if product.id in compare_list:
        message = f"Товар '{product.name}' уже добавлен в список для сравнения."
    elif len(compare_list) >= 3:
        message = "Вы уже добавили 3 товара для сравнения."
    else:
        compare_list.append(product.id)
        request.session['compare_list'] = compare_list

    return message


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
        'count': len(products)
    }
    return context
