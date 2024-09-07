from django.db import models


class ProductFeature(models.Model):
    """
    Модель описывающая характеристику товара.
    Атрибуты:
        product (Product): Связь с моделью Product к которому принадлежит характеристика.
        feature (Feature): Связь с моделью Feature опрделяющая характеристику товара.
        value (str): Значение характеристики.
    """
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, blank=True, null=True, related_name="features")
    feature = models.ForeignKey("Feature", on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return str(self.product)
