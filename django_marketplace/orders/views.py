from django.http import HttpResponse
from django.shortcuts import render


def add_order(request):
    return HttpResponse("Оформление заказа")
