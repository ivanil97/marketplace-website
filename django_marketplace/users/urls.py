from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views_dir import (
    AccountView,
    ProfileView,
    UserOrderHistoryView,
    RegisterView,
    UserPasswordResetView,
    LoginUser,
    LogoutUser,
    get_viewed_products,
    get_viewed_count,
    remove_product_from_viewed,
)

app_name = "user"

urlpatterns = [
    path('login/',
         LoginUser.as_view(
             template_name='templates_users/login.html',
             redirect_authenticated_user=True,
             extra_context={'simple_header': True},
         ),
         name="login"
         ),

    path('logout/',
         LogoutUser.as_view(
             next_page=reverse_lazy("home"),
         ),
         name="logout"
         ),

    path('register/',
         RegisterView.as_view(),
         name='register'
         ),

    path('account/',
         AccountView.as_view(),
         name='account'
         ),

    path('account/profile/',
         ProfileView.as_view(),
         name='user_profile'
         ),

    path('account/order_history/',
         UserOrderHistoryView.as_view(),
         name='user_order_history',
         ),

    path('password-reset/',
         UserPasswordResetView.as_view(),
         name="password_reset"
         ),

    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="templates_users/password_reset_confirm.html",
             success_url=reverse_lazy("user:password_reset_complete"),
             extra_context={'simple_header': True},
         ),
         name="password_reset_confirm",
         ),

    path(
        'password-reset-complete/',
        PasswordResetCompleteView.as_view(
            template_name="templates_users/password_reset_complete.html",
            extra_context={'simple_header': True},
        ),
        name="password_reset_complete",
    ),

    path('viewed/remove/<int:product_id>/',
         remove_product_from_viewed,
         name='remove_product_from_viewed'
         ),

    path('viewed/count/',
         get_viewed_count,
         name='get_viewed_count'
         ),

    path('viewed-products/',
         get_viewed_products,
         name='viewed_products'
         ),
]
