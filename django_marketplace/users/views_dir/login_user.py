from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.utils.translation import get_language
from django.conf import settings
from products.models import SellerPrice

from carts.models import Cart


# Разобраться с удалением в сессси удаляем а в БД остается
class LoginUser(LoginView):
    def form_valid(self, form):
        # 1 - Получаем и сохраняем данные в переменную из сессии
        data_session = self.request.session.get("cart", {})
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        # Авторизуем пользователя
        if user is not None:
            lan = get_language()
            settings.LOGIN_REDIRECT_URL = f"/{lan}" + settings.LOGIN_REDIRECT_URL.replace("/ru", "").replace("/en", "")
            login(self.request, user)

        # Проверяем данные из сесии
        if data_session:
            carts = Cart.objects.filter(user=self.request.user.id).prefetch_related('sellerprice').all()

            # Цикл для обхода товаров из сесии и БД
            for cart in carts:
                str_id = str(cart.sellerprice.id)
                data_id = data_session.get(str_id, {})

                # Если товар из сесии и из БД был найден:
                if data_id:
                    quantity_session = data_id.get('quantity', 1)

                    # Если количество товара не равно переприсваиваем новое, взятое из сесии
                    if cart.quantity != quantity_session:
                        cart.quantity = quantity_session
                        cart.save()

                    # Если товар в сесии был удален, удаляем его из БД
                    if data_id.get('deleted'):
                        cart.delete()

                    # Удаляем товар из сесии
                    data_session.pop(str_id)

            # Цикл для создания новых товаров которые не были обнаружены в БД
            for id_k, value_k in data_session.items():
                product = SellerPrice.objects.get(id=int(id_k))
                count = value_k.get('quantity', 1)
                Cart.objects.create(user=self.request.user, sellerprice=product, quantity=count)

        return super().form_valid(form)
