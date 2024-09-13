def get_comparison_list(request):
    return request.session.get('compare_list', [])


def add_to_comparison(request, product_id):
    compare_list = set(request.session.get('compare_list', []))
    compare_list.add(product_id)
    request.session['compare_list'] = list(compare_list)


def remove_from_compare_list(request, product_id):
    compare_list = set(request.session.get('compare_list', []))
    compare_list.discard(product_id)
    request.session['compare_list'] = list(compare_list)


