from django.http import JsonResponse
from products.services.viewed_products_service import ViewedProductsService


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
    limit = int(request.GET.get('limit', 20))  # Учитываем параметр limit из запроса
    products = ViewedProductsService.get_viewed_products(user, limit)
    products_list = list(products.values('product__id', 'product__name'))  # Определяем поля, которые нужно вернуть
    return JsonResponse({'products': products_list})

def get_viewed_count(request):
    """
    Обработчик для получения количества просмотренных товаров.
    """
    user = request.user
    count = ViewedProductsService.get_viewed_count(user)
    return JsonResponse({'count': count})
