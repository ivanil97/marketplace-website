from django.utils import timezone
from django.views.generic import ListView
from products.models import Product


class SaleView(ListView):
    model = Product
    template_name = "templates_products/sale_list.html"
    context_object_name = "products"

    def get_queryset(self):
        # Фильтрация товаров с активными скидками, проверка на срок действия скидки
        return Product.objects.filter(
            discounts__is_active=True,
            discounts__archived=False,
            discounts__to_date__gte=timezone.now()
        ).distinct()
