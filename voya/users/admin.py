from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from voya.employees.models import EmployeeProfile
from voya.users.forms import CustomUserChangeForm, CustomUserCreationForm

UserModel = get_user_model()


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email',
        'is_active'
    )

    ordering = ['email']

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        ('Account Data', {
            'fields': (
                'email',
                "password",
            ),
        }),
        ('Permissions', {
            'fields': (
                'is_staff',
                'is_superuser',
                'is_active',
                'groups',
                'user_permissions',
                'role',
            ),
        }),
        ('Log in Information', {
            'fields': (
                'date_joined',
                'last_login',

            ),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')
