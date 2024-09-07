from django.core.cache import cache
import random

from products.models import Category, Product, SellerPrice, SliderBanner, StaticBanner


def get_slider_banners():
    """
    Получает три случайных активных баннера для слайдера.
    Если баннеры отсутствуют в кеше, данные извлекаются из базы данных и кешируются на 10 минут.
    Returns:
        list: Список активных слайдеров баннеров.
    """
    banners = cache.get('slider_banners')
    if not banners:
        banners = list(SliderBanner.objects.filter(is_active=True))
        banners = random.sample(banners, min(len(banners), 3))
        cache.set('slider_banners', banners, timeout=600)  # кеш на 10 минут
    return banners


def get_static_banners():
    """
    Получает три случайных активных статических баннера.
    Если баннеры отсутствуют в кеше, данные извлекаются из базы данных и кешируются на 10 минут.
    Returns:
        list: Список активных статических баннеров.
    """
    banners = cache.get('static_banners')
    if not banners:
        banners = list(StaticBanner.objects.filter(is_active=True))
        banners = random.sample(banners, min(len(banners), 3))
        cache.set('static_banners', banners, timeout=600)  # кеш на 10 минут
    return banners


def get_popular_items():
    """
    Получает 8 случайных популярных товаров
    :return: list(dict): список словарей, где каждый товар представляет 1 словарь со всеми параметрами для передачи
    в контекст view-функции
    """
    popular_items_raw = Product.objects.filter(archived=False).order_by('?').prefetch_related('prices').prefetch_related('images') #TODO: добавить условия сортировки в соответствии с ТЗ
    popular_items_raw = popular_items_raw[:8]
    popular_items = list(popular_items_raw.values())

    for i_index, i_item in enumerate(popular_items_raw):
        item_prices = [
            seller_price.price
            for seller_price in
            i_item._prefetched_objects_cache['prices']]

        if item_prices:
            average_item_price = sum(item_prices) // len(item_prices)
            popular_items[i_index]['item_price'] = average_item_price

        if i_item._prefetched_objects_cache['images']:
            popular_items[i_index]['image'] = i_item._prefetched_objects_cache['images'][0].image

        popular_items[i_index]['category'] = Category.objects.get(id=i_item.category_id)
        print(popular_items[i_index], end='\n')

    return popular_items

def get_limited_items():
    limited_items = list(SellerPrice.objects.filter(is_limited=True))
