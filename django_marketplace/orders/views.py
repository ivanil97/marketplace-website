from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.urls import reverse

from .models import Order


class OrderDetailView(TemplateView):
    template_name = 'templates_order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id, user=self.request.user)
        context['order'] = order
        context['products'] = order.products.all()
        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id, user=request.user)

        payment_method = request.POST.get('payment_method')
        if payment_method and order.payment_status == 'error':
            order.payment_status = 'paid'
            order.save()

        return redirect('orders:order_detail', pk=order_id)


def add_order(request):
    return HttpResponse("Оформление заказа")
