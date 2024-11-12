from constance import config

from django.db.models import Prefetch

from products.models import SellerPrice, SliderBanner, StaticBanner, Discount


def get_slider_banners(slider_banners_amount=3):
    """
    Получает три случайных активных баннера для слайдера.
    Если баннеры отсутствуют в кеше, данные извлекаются из базы данных и кешируются на 10 минут.
    Returns:
        list: Список активных слайдеров баннеров.
    """
    banners = cache.get('slider_banners')
    if not banners:
        banners = list(SliderBanner.objects.filter(is_active=True))
        banners = random.sample(banners, min(len(banners), slider_banners_amount))
        cache.set('slider_banners', banners, timeout=config.CACHES_BANNERS)
    return banners


def get_static_banners(static_banners_amount=3):
    """
    Получает три случайных активных статических баннера.
    Если баннеры отсутствуют в кеше, данные извлекаются из базы данных и кешируются на 10 минут.
    Returns:
        list: Список активных статических баннеров.
    """
    banners = cache.get('static_banners')
    if not banners:
        banners = list(StaticBanner.objects.filter(is_active=True))
        banners = random.sample(banners, min(len(banners), static_banners_amount))
        cache.set('static_banners', banners, timeout=config.CACHES_BANNERS)
    return banners


def get_popular_items(popular_item_amount=8):
    """
    Получает 8 случайных популярных товаров
    :return: list(dict): список словарей, где каждый товар представляет 1 словарь со всеми параметрами для передачи
    в контекст view-функции
    """
    one_discount_queryset = Discount.objects.filter(is_active=True)
    popular_items_raw = list(SellerPrice.objects.filter(archived=False)
                             .prefetch_related('product__images', Prefetch('product__discounts', queryset=one_discount_queryset, to_attr='one_discount'))
                             .order_by('product__sort_index', '-product__quantity_sold'))

    popular_items = popular_items_raw[:popular_item_amount]
    return popular_items


from django.core.cache import cache
from datetime import datetime, timedelta
import random


def get_limited_items(limited_item_amount=16):
    """
    Получает 16 товаров ограниченного тиража и 1 товар для предложения дня.
    Ограниченный тираж - 16 случайных товаров с признаком is_limited кроме товара "Предложение дня".
    Предложение дня - случайный товар с признаком is_limited, который кэшируется до конца текущего дня.

    :param limited_item_amount: количество товаров ограниченного тиража.
    :return: tuple(SellerPrice, list(SellerPrice), str):
    кортеж из трех элементов для передачи во view-функцию:
    Товар для блока "Предложение дня", список товаров ограниченного тиража, строковое представление конца текущего дня в формате ISO 8601.
    """
    one_discount_queryset = Discount.objects.filter(is_active=True)
    limited_items_raw = list(SellerPrice.objects.filter(is_limited=True, archived=False)
                             .prefetch_related(
        'product__images',
        Prefetch('product__discounts', queryset=one_discount_queryset, to_attr='one_discount')))

    if not limited_items_raw:
        # Если нет доступных товаров, возвращаем None
        return None, [], None

    # Получаем кэшированный товар для "Предложения дня"
    limited_item_day = cache.get('limited_item_day')

    if limited_item_day is None:
        # Если кэш отсутствует, выбираем случайный товар и обновляем кэш
        limited_items = limited_items_raw[:limited_item_amount+1]
        limited_item_day = random.choice(limited_items)  # Выбор случайного товара
        limited_items.remove(limited_item_day)

        # Рассчитываем время окончания суток
        now = datetime.now()
        end_of_day = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
        timeout = int((end_of_day - now).total_seconds())
        cache.set('limited_item_day', limited_item_day, timeout=timeout)  # Кешируем до конца дня
    else:
        limited_items_raw.remove(limited_item_day)
        limited_items = limited_items_raw[:limited_item_amount]  # Выбираем остальные товары

    # Если кэшированный товар существует, просто определяем end_of_day
    end_of_day = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time())

    return limited_item_day, limited_items, end_of_day.isoformat()

