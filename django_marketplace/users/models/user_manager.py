from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Кастомный менеджер для работы с пользователями.
    Отвечает за создание пользователей и суперпользователей.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя.
        Аргументы:
            email (str): Уникальный email пользователя.
            password (str): Пароль для пользователя.
            **extra_fields: Дополнительные поля пользователя.
        Возвращает:
            user (User): Новый объект пользователя.
        """
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с административными правами.
        Аргументы:
            email (str): Уникальный email суперпользователя.
            password (str): Пароль для суперпользователя.
            **extra_fields: Дополнительные поля суперпользователя.
        Возвращает:
            user (User): Новый объект суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
