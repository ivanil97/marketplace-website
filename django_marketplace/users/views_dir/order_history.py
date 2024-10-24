from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from orders.models import Order


class UserOrderHistoryView(LoginRequiredMixin, TemplateView):
    """
    View-функция для представления истории заказов в личном кабинете пользователя
    """
    login_url = 'user:login'
    template_name = 'templates_users/user_order_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_history = Order.objects.filter(user_id=self.request.user.id)
        context['orders'] = order_history
        return context
