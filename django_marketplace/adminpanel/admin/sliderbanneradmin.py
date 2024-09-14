from django.contrib import admin
from products.models.sliderbanner import SliderBanner

@admin.register(SliderBanner)
class SliderBannerAdmin(admin.ModelAdmin):
    """
    Класс для представления модели SliderBanner в админ-панели.
    Атрибуты:
    - list_display : tuple
        Определяет, какие поля модели будут отображаться в списке объектов в админ-панели.
        В данном случае, это заголовок, цена, статус активности, дата создания и дата обновления.
    - list_filter : tuple
        Определяет фильтры для поиска объектов в админ-панели.
        В данном случае, это статус активности и дата создания.
    - search_fields : tuple
        Определяет поля модели, по которым будет производиться поиск.
    """
    list_display = ('title', 'price', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')