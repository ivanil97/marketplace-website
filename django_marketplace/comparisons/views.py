from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, ListView

from comparisons.services.comparison_service import *


class ComparisonListView(View):
    template_name = 'templates_comparisons/comparison_list.html'

    def get(self, request) -> HttpResponse:
        limit = int(request.GET.get('limit', 3))
        context = get_comparison_context(request, limit)
        return render(request, self.template_name, context)


class AddComparisonView(View):
    def post(self, request, **kwargs):
        slug = kwargs.get('slug')
        message = add_to_comparison(request, slug)
        request.session['message'] = message
        return redirect('comparisons:comparison_list')


class RemoveFromComparisonView(View):

    def post(self, request, **kwargs):
        slug = kwargs.get('slug')
        remove_from_comparison(request, slug)
        return redirect('comparisons:comparison_list')
