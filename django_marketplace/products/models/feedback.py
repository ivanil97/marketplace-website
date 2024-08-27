from django.db import models


class FeadBack(models.Model):
    """Отзыв на конкретный товар"""
    article = models.TextField(null=False)
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.article
