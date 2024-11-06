from django.contrib import admin

from voya.users.models import CustomUser


@admin.register(CustomUser)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'role')
