from django.db import models


class Discount(models.Model):
    """
    Модель скидок товаров.
    Атрибуты:
        action_scheme (int): Вид скидки.
        products: Поле для связи скидки с товарами.
        categories: Поле для связывания скидки с категориями товаров.
        percent (int): Процент скидки на товар.
        description (str): Описание скидки.
        from_date (datetime): Время создания скидки.
        to_date (datetime): Время окончания скидки.
        is_active (bool): Указатель на активность скидки.
        archived (bool): Указатель на архивацию скидки.
    """
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
        return f"Discount {self.percent} %"

    class Meta:
        ordering = ("-to_date",)
