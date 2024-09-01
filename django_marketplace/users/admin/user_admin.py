from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models.user import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Админка для модели User.
    Отображает пользователей с возможностью поиска, фильтрации по роли, активности и правам.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'role')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
