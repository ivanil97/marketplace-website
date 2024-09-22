from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from users.models import User


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    View-функция для представления профиля пользователя
    """
    login_url = 'user:login'
    template_name = 'templates_users/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = self.request.user
        context['user'] = user_data
        return context