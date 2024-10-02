from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Order
from django.shortcuts import render


class OrderDetailView(TemplateView):
    template_name = 'templates_order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id, user=self.request.user)
        context['order'] = order
        context['products'] = order.products.all()
        return context
