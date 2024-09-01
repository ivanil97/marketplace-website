from django.db import models

class Role(models.Model):
    """
    Модель для хранения ролей пользователей.
    Атрибуты:
        role_name (str): Название роли (например, Администратор, Пользователь).
    """
    role_name = models.CharField(max_length=50, verbose_name="Название роли", unique=True)

    def __str__(self):
        """
        Возвращает строковое представление объекта Role.
        """
        return self.role_name

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
