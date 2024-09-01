from django.db import models


class Discount(models.Model):
    """Скидка на товар"""
    action_scheme = models.IntegerField()
    products = models.ManyToManyField("Product", blank=True, related_name='discounts')
    categories = models.ManyToManyField("Category", related_name='discounts')
    percent = models.IntegerField()
    description = models.TextField(blank=True)
    from_date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return "Discount " + str(self.pk)
