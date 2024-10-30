from django.shortcuts import redirect
from django.views.generic import View

from comparisons.services.comparison_service import *


class RemoveFromComparisonView(View):

    def post(self, request, **kwargs):
        slug = kwargs.get('slug')
        remove_from_comparison(request, slug)
        return redirect('comparisons:comparison_list')
