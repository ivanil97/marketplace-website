from datetime import datetime, timedelta
from typing import List, Dict

from django.core.cache import cache
import random

from constance import config

from django.db.models import Prefetch

from products.models import Category, Product, SellerPrice, SliderBanner, StaticBanner, ProductImage


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
        cache.set('slider_banners', banners, timeout=config.CACHES_BANNERS)  # кеш на 10 минут
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
        cache.set('static_banners', banners, timeout=config.CACHES_BANNERS)  # кеш на 10 минут
    return banners


def get_popular_items():
    """
    Получает 8 случайных популярных товаров
    :return: list(dict): список словарей, где каждый товар представляет 1 словарь со всеми параметрами для передачи
    в контекст view-функции
    """

    popular_items_raw = list(SellerPrice.objects.filter(archived=False)
                             .prefetch_related('product__images')
                             .order_by('product__sort_index', '-product__quantity_sold'))

    popular_items = popular_items_raw[:8]

    return popular_items


def get_limited_items():
    """
    Получает 16 товаров ограниченного тиража и 1 товар для предложения дня
    Ограниченный тираж - 16 случайных товаров с признаком is_limited кроме товара "Предложение дня"
    Предложение дня - случайный товар с признаком is_limited, который кэшируется до конца текущего дня
    :return: tuple(SellerPrice, list(SellerPrice)):
    кортеж из двух элементов для передачи во view-функцию:
    Товар для блока предложение дня, список товаров ограниченного тиража
    """
    limited_items_raw = list(SellerPrice.objects.filter(is_limited=True, archived=False)
                             .prefetch_related('product__images'))

    if limited_items_raw:
        limited_item_day = cache.get('limited_item_day')
        if not limited_item_day:
            limited_items = limited_items_raw[:17]
            limited_item_day = random.sample(limited_items, 1)[0]
            limited_items.remove(limited_item_day)

            now = datetime.now()
            end_of_day = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
            timeout = int((end_of_day - now).total_seconds())
            cache.set('limited_item_day', limited_item_day, timeout=timeout)  # кеш до конца дня
        else:
            limited_items_raw.remove(limited_item_day)
            limited_items = limited_items_raw[:16]

        return limited_item_day, limited_items

    else:
        return None
