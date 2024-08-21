from django.views.generic import TemplateView
from .services import get_slider_banners, get_static_banners

class HomeView(TemplateView):
    """
    Представление для главной страницы. Отображает баннеры слайдера и статические баннеры.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        Формирует контекст для передачи данных в шаблон.
        """
        context = super().get_context_data(**kwargs)
        context['slider_banners'] = get_slider_banners()
        context['static_banners'] = get_static_banners()
        return context


