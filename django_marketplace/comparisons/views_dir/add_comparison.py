from django.shortcuts import redirect
from django.views.generic import View

from comparisons.services.comparison_service import *


class AddComparisonView(View):
    def post(self, request, **kwargs):
        slug = kwargs.get('slug')
        add_to_comparison(request, slug, limit=3)
        return redirect('comparisons:comparison_list')
