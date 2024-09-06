from django.db import models


class Seller(models.Model):
    """
    Модель продавца.
    Атрибуты:
        name (str): Имя продавца.
        slug (str): Слаг продавца.
        description (str): Описание продавца.
        email (str): Элктронный адресс продавца.
        phone (str): Мобильный номер продавца.
        address (str): Адресс проживания продавца.
        image (str): Аватар профиля продавца.
        user (User): Связь с моделью User.
    """
    name = models.CharField(max_length=256, verbose_name="Name", db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    description = models.TextField(blank=True)
    email = models.EmailField(null=False)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=256)
    image = models.ImageField(blank=True, upload_to="sellers_avatars")
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
