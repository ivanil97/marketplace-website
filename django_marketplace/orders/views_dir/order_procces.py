from django.contrib.auth import login
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from carts.models import Cart
from carts.templatetags.carts_tags import total_price
from orders.forms import OrderProceedForm
from orders.models import Order
from orders.utils import get_cart_data
from users.models import User


class OrderProcessView(TemplateView, FormView):
    template_name = 'templates_order/order_filling_form.html'
    form_class = OrderProceedForm
    success_url = 'orders:order_payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user.id).prefetch_related('sellerprice__product__images')
        else:
            cart = get_cart_data(self.request)['cart_items']

        context['cart'] = cart
        if 'user_exists' in self.request.session:
            context['user_exists'] = True
            del self.request.session['user_exists']

        return context

    def form_valid(self, form):
        # получение данных корзины
        carts = get_cart_data(self.request)['cart_items']
        cart_products = get_cart_data(self.request)['cart_products']
        total_carts_price = total_price(self.request, carts)['total_price']

        # проверка существования пользователя при попытке его регистрации при оформлении заказа
        if not self.request.user.is_authenticated:
            name = form.cleaned_data["first_name"]
            name_parts = name.split()
            first_name, last_name = (name_parts + [None])[:2]

            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user_check = User.objects.filter(email=email)
            if not user_check:
                new_user = User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number
                )
                new_user.set_password(password)
                new_user.save()
                login(self.request, new_user)
            else:
                self.request.session['user_exists'] = True
                return redirect('orders:order_proceed')

        # создание нового заказа на основании полученных данных о корзине и пользователе
        new_order = Order.objects.create(
            user=self.request.user,
            total_price=total_carts_price,
            city=form.cleaned_data['city'],
            address=form.cleaned_data['address'],
            payment_option=form.cleaned_data['payment_option'],
            delivery_option=form.cleaned_data['delivery_option']
        )
        new_order.products.set(cart_products)

        return redirect(reverse(self.success_url, kwargs={'pk': new_order.pk}))
