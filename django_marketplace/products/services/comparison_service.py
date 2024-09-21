from products.models.product import Product


def get_comparison_list(request, limit=3):
    product_id = request.session.get('compare_list', [])
    products = Product.objects.filter(id__in=product_id)[:limit]
    return products


def add_to_comparison(request, slug):
    product = Product.objects.get(slug=slug)
    compare_list = request.session.get('compare_list', [])

    if product.id not in compare_list:
        compare_list.append(product.id)
        request.session['compare_list'] = compare_list


def remove_from_comparison(request, product_id):
    compare_list = get_comparison_list(request)

    if product_id in compare_list:
        compare_list.remove(product_id)
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
