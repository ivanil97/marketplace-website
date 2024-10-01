from django.urls import path, include
from django.conf import settings


from comparisons.views import *

app_name = 'comparisons'

urlpatterns = [
    path('', ComparisonListView.as_view(), name='comparison_list'),
    path('remove/<slug:slug>/', RemoveFromComparisonView.as_view(), name='remove_from_comparison'),
    path('add/<slug:slug>/', AddComparisonView.as_view(), name='add_to_comparison'),
]

if settings.DEBUG:
    urlpatterns = [
                      path('__debug__/', include("debug_toolbar.urls")),
                  ] + urlpatterns
