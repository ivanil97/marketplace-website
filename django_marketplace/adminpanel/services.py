from django.core.cache import cache
import random
from adminpanel.models.sliderbanner import SliderBanner
from adminpanel.models.staticbanner import StaticBanner


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


