from django.db import models
from products.models.product import Product


class ProductImage(models.Model):
    image = models.ImageField(
        null=True, blank=True,
        upload_to="productimage_image_directory_path",
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT, 
        related_name='images',
    )
