from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import ReviewForm
from .services.review_service import get_reviews_for_product, add_review_to_product

from .models.product import Product
from .models.review import Review


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = ''

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        user = self.request.user
        comment = form.cleaned_data['comment']
        add_review_to_product(product_id=product_id, user=user, comment=comment)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.kwargs['product_id']})