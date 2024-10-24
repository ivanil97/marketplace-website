from django.contrib.auth.views import LogoutView

from carts.models import Cart


class LogoutUser(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Получаем данные о корзинах из БД
        carts = Cart.objects.filter(user=request.user.id).prefetch_related('sellerprice').all()
        carts_session = {str(col.sellerprice.id): {'quantity': col.quantity} for col in carts}

        # Выполняем выход пользователя
        response = super().dispatch(request, *args, **kwargs)

        # Загружаем данные о корзине пользователя в сессию
        request.session['cart'] = carts_session
        return response
