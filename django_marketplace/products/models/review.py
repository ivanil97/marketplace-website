from django.db import models
from .product import Product
from users.models import User


class Review(models.Model):
    detail_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.detail_product} : {self.comment}"
