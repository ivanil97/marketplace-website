from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from .user_manager import UserManager
from .role import Role

class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя с уникальным полем email для аутентификации.
    Атрибуты:
        email (str): Уникальный email пользователя, используемый для входа.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        is_active (bool): Флаг активности пользователя.
        is_staff (bool): Флаг, указывающий, является ли пользователь сотрудником (доступ в админку).
        is_superuser (bool): Флаг, указывающий на права суперпользователя.
        role (Role): Ссылка на модель Role, которая указывает роль пользователя.
        groups: Поле для связи пользователя с группами.
        user_permissions: поле для связи пользователя с индивидуальными разрешениями.
    """
    email = models.EmailField(max_length=255, unique=True, verbose_name='email адрес')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль")
    profile_picture = models.ImageField(null=True, upload_to='users/profile_pictures/', verbose_name="Фото")

    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True, verbose_name='Группы')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True, verbose_name='Разрешения')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
