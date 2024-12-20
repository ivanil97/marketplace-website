from constance import config
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from carts.models import Cart
from carts.templatetags.carts_tags import total_price
from orders.forms import OrderProceedForm
from orders.models import Order, OrderItem
from orders.utils import get_cart_data
from users.models import User


class OrderProcessView(TemplateView, FormView):
    template_name = 'templates_order/order_filling_form.html'
    form_class = OrderProceedForm
    success_url = 'orders:order_payment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = get_cart_data(self.request)['cart_items']

        context['cart'] = cart
        context['express_delivery_cost'] = config.EXPRESS_DELIVERY_COST
        context['delivery_cost'] = config.DELIVERY_COST
        context['free_delivery_minimal_cost'] = config.FREE_DELIVERY_MINIMAL_COST

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
        if total_carts_price > config.FREE_DELIVERY_MINIMAL_COST:
            delivery_cost = 0
        else:
            delivery_option = form.cleaned_data['delivery_option']
            if delivery_option == 'express':
                delivery_cost = config.EXPRESS_DELIVERY_COST
            else:
                delivery_cost = config.DELIVERY_COST

        new_order = Order.objects.create(
            user=self.request.user,
            total_price=total_carts_price + delivery_cost,
            city=form.cleaned_data['city'],
            address=form.cleaned_data['address'],
            payment_option=form.cleaned_data['payment_option'],
            delivery_option=form.cleaned_data['delivery_option']
        )
        new_order.save()

        for i_item in cart_products:
            new_item = OrderItem.objects.create(
                order=new_order,
                seller_price=i_item['seller_price'],
                quantity=i_item['quantity']
            )
            new_item.save()

        carts_to_delete = Cart.objects.filter(user=self.request.user.id)
        if carts_to_delete:
            carts_to_delete.delete()

        return redirect(reverse(self.success_url, kwargs={'pk': new_order.pk}))
