from django.db import models
from products.models.product import Product


def productimage_image_directory_path(instance: "ProductImage", filename: str) -> str:
    return f"products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


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
