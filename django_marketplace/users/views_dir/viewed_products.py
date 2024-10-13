from django.http import JsonResponse
from django.shortcuts import render
# from products.services.viewed_products_service import ViewedProductsService
from users.services.viewed_products_service import ViewedProductsService


def remove_product_from_viewed(request, product_id):
    """
    Обработчик для удаления товара из списка просмотренных.
    """
    user = request.user
    ViewedProductsService.remove_from_viewed(user, product_id)
    return JsonResponse({'status': 'success'})


def get_viewed_products(request):
    """
    Обработчик для получения списка просмотренных товаров.
    """
    user = request.user
    # limit = int(request.GET.get('limit', 20))  # Учитываем параметр limit из запроса
    limit = 20
    products_list = []
    products = ViewedProductsService.get_viewed_products(user, limit)
    # products_list = list(products.values('product__slug', 'product__name'))  # Определяем поля, которые нужно вернуть
    for pr in products:
        product_data = {
            "productname": pr.product.name,
            "productslug": pr.product.slug,
            "productcategory": pr.product.category.name,
            "images": pr.product.images,
        }
        products_list.append(product_data)
    return render(request, 'templates_users/products_history.html', {'products': products_list})


def get_viewed_count(request):
    """
    Обработчик для получения количества просмотренных товаров.
    """
    user = request.user
    count = ViewedProductsService.get_viewed_count(user)
    return JsonResponse({'count': count})
