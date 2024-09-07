from django.views.generic import TemplateView


class AccountView(TemplateView):
    """
    Личный кабинет пользователя
    необходимо доработать
    """
    template_name = 'templates_users/account.html'
