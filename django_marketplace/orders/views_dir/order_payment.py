from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from orders.forms import PaymentDataForm
from orders.models import Order


class OrderPaymentView(TemplateView, FormView):
    template_name = 'templates_order/payment.html'
    form_class = PaymentDataForm
    success_url = 'orders:payment_progress'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_order = Order.objects.filter(id=self.kwargs.get('pk')).first()
        context['order'] = current_order
        return context

    def form_valid(self, form):
        card_number = form.cleaned_data['card_number']
        current_order = Order.objects.filter(id=self.kwargs.get('pk')).first()
        if current_order:
            if len(card_number) != 8 or int(card_number) % 2 != 0:
                current_order.payment_status = current_order.PAYMENT_STATUS[2]
            else:
                current_order.payment_status = current_order.PAYMENT_STATUS[1]
            current_order.save()

        return redirect(reverse(self.success_url, kwargs={'pk': current_order.pk}))


class ProgressPaymentView(TemplateView):
    template_name = 'templates_order/progress_payment.html'