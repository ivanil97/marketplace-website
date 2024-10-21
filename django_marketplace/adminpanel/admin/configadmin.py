from constance.admin import ConstanceAdmin, Config
from django.contrib import admin, messages
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django import forms


class CacheChoiceForm(forms.Form):
    """
    Форма для установки списка ключей кеша проекта для выборочного сброса.
    options = [("cache_key1", "verbose_name_key1"), ...]
    Если cache_key это ключ кэша html-фрагмента, то его необходимо преобразовать
    from django.core.cache.utils import make_template_fragment_key
    """
    options = [
        ('slider_banners', 'api cache slider banners'),
        ('static_banners', 'api cache static banners'),
        ('limited_item_day', 'api cache limited item day'),
        (make_template_fragment_key('product_detail'), 'html fragment cache product detail'),
        (make_template_fragment_key('product_list'), 'html fragment cache product list'),
    ]
    template_name_label = ""
    cache_choice_field = forms.MultipleChoiceField(
        choices=options,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-row'})
    )


class ConfigAdmin(ConstanceAdmin):
    change_list_template = 'templates_adminpanel/config.html'

    def clear_cache(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            form = CacheChoiceForm(request.POST)
            if request.POST.get("clear_all"):
                messages.info(request, f"All caches was cleared.")
                cache.clear()
                return redirect("..")
            elif form.is_valid():
                selected_values = form.cleaned_data['cache_choice_field']
                for cache_key in selected_values:
                    cache.delete(cache_key)
                messages.info(
                    request,
                    f"Cache was deleted for: {selected_values}",
                )
                return redirect("..")
        else:
            form = CacheChoiceForm()
        context = {
            "form": form,
        }
        return render(request, "templates_adminpanel/clear_cache.html", context=context)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("clear_cache/", self.clear_cache, name="clear-cache"),
        ]
        return new_urls + urls


admin.site.unregister([Config])
admin.site.register([Config], ConfigAdmin)
