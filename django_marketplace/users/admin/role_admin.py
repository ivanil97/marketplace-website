from django.contrib import admin
from users.models.role import Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Админка для модели Role.
    Отображает список ролей с возможностью поиска и фильтрации.
    """
    list_display = ('role_name',)
    search_fields = ('role_name',)
    ordering = ('role_name',)
