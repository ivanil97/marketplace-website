from products.models import Discount, ProductImage


one_discount_queryset = Discount.objects.filter(is_active=True, archived=False)

one_image_queryset = ProductImage.objects.order_by('id')[:1]
