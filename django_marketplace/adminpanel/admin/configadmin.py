from constance.admin import ConstanceAdmin, Config
from django.contrib import admin, messages
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django import forms


class CacheChoiceForm(forms.Form):
    """
    Форма для установки списка ключей кеша проекта для выборочного сброса.
    options = [("cache_key1", "verbose_name_key1"), ...]
    """
    options = [
        ('slider_banners', 'slider banners'),
        ('static_banners', 'static banners'),
        ('limited_item_day', 'limited item day'),
        ('product_detail', 'product detail'),
        ('product_list', 'product list'),
    ]
    template_name_label = ""
    cache_choice_field = forms.MultipleChoiceField(choices=options, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-row'}))


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
                if selected_values:
                    for cache_key in selected_values:
                        cache.delete(cache_key)
                messages.info(request, f"Cache was deleted for: {', '.join(selected_values)}")
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
