from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from comparisons.services.comparison_service import *


class ComparisonListView(View):
    template_name = 'templates_comparisons/comparison_list.html'

    def get(self, request) -> HttpResponse:
        limit = int(request.GET.get('limit', 3))
        context = get_comparison_context(request, limit)
        return render(request, self.template_name, context)
