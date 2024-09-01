from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    products = models.ManyToManyField("Product", related_name="tags")

    def __str__(self):
        return self.name
