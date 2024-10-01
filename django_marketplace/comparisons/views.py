from django.shortcuts import render
from django.views import View

from comparisons.services.comparison_service import *

class ComparisonListView(View):
    def get(self, request):
        limit = int(request.GET.get('limit', 3))
        context = get_comparison_context(request, limit)
        return render(request, 'templates_comparisons/comparison_list.html', context)


class AddComparisonView(View):
    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        add_to_comparison(request, slug)
        return render(request, 'templates_comparisons/comparison_list.html', get_comparison_context(request))


class RemoveFromComparisonView(View):
    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        remove_from_comparison(request, slug)
        return render(request, 'templates_comparisons/comparison_list.html', get_comparison_context(request))