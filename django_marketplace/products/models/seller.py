from django.db import models


class Seller(models.Model):
    """Продавец с конкретным списком товаров"""
    name = models.CharField(max_length=256, verbose_name="Имя", db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    description = models.TextField(blank=True)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=256)
    image = models.ImageField(blank=True, upload_to="sellers_avatars")
    #user = models.ForeignKey("User", on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
