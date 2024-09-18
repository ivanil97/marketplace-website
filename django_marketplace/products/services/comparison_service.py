from products.models.product import Product


def get_comparison_list(request, limit=3):
    product_id = request.session.get('compare_list', [])
    products = Product.objects.filter(id__in=product_id)[:limit]
    return products


def add_to_comparison(request, product_id):
    compare_list = get_comparison_list(request)

    if product_id not in compare_list:
        compare_list.append(product_id)
        request.session['compare_list'] = compare_list


def remove_from_compare_list(request, product_id):
    compare_list = get_comparison_list(request)

    if product_id in compare_list:
        compare_list.remove(product_id)
        request.session['compare_list'] = compare_list


def get_comparison_count(request):
    return len(request.session.get('compare_list', []))
