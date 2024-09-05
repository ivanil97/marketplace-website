from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,

)


from .views.account import AccountView
from .views.register import RegisterView
from .views.password_reset import UserPasswordResetView

app_name = "user"

urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name='templates_users/login.html',
             redirect_authenticated_user=True,
         ),
         name="login"),
    path('logout/',
         LogoutView.as_view(
             next_page=reverse_lazy("home"),
         ),
         name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', AccountView.as_view(), name='account'),
    path('password-reset/', UserPasswordResetView.as_view(), name="password_reset"),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name="templates_users/password_reset_confirm.html",
            success_url=reverse_lazy("user:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        'password-reset-complete/',
        PasswordResetCompleteView.as_view(template_name="templates_users/password_reset_complete.html"),
        name="password_reset_complete"
    ),
]
