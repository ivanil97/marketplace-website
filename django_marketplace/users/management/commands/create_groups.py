from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    """
    Кастомная команда для создания предустановленных групп с привилегиями.
    Создает группы с заранее определенными разрешениями, чтобы упростить управление ролями.
    python manage.py create_groups
    """
    help = 'Создает группы с предустановленными правами доступа.'

    def handle(self, *args, **options):
        """
        Основной метод, выполняющий логику команды.
        Аргументы:
            *args: Дополнительные аргументы.
            **options: Дополнительные параметры.
        """
        # Определение групп и соответствующих разрешений
        groups_permissions = {
            'Администратор': [
                'add_user', 'change_user', 'delete_user', 'view_user',  # Примеры разрешений для модели User
                'add_group', 'change_group', 'delete_group', 'view_group',
            ],
            'Пользователь': [
                'view_user',  # Пользователь может только просматривать информацию
            ],
        }

        # Цикл по группам и привязка разрешений
        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана.'))
            else:
                self.stdout.write(f'Группа "{group_name}" уже существует.')

            # Получение разрешений и их назначение группе
            for perm in permissions:
                try:
                    # Получаем разрешение по его коду
                    permission = Permission.objects.get(codename=perm,
                                                        content_type=ContentType.objects.get_for_model(User))
                    group.permissions.add(permission)
                    self.stdout.write(f'Разрешение "{perm}" добавлено в группу "{group_name}".')
                except Permission.DoesNotExist:
                    self.stdout.write(f'Разрешение "{perm}" не найдено.')

        self.stdout.write(self.style.SUCCESS('Все группы и разрешения успешно обработаны.'))
