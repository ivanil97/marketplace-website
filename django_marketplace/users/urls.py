from django.urls import path, include
from django.contrib.auth.views import LoginView

from .views.account import AccountView

app_name = "user"

urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name='templates_users/login.html',
             redirect_authenticated_user=True,
         ),
         name="login"),
    path('account/', AccountView.as_view(), name='account')
]
