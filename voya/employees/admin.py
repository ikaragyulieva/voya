from django.contrib import admin

from voya.employees.models import EmployeeProfile


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'first_name',
        'last_name',
        'job_title',
        'is_active',
    )

    search_fields = (
        'first_name',
        'last_name',
        'job_title',
        'user__email',
    )

    list_filter = (
        'is_active',
        'title',
    )

    ordering = ('last_name', 'first_name')

    fieldsets = (
        ('Personal Information', {
            'fields': ('title', 'first_name', 'last_name', 'phone_number')
        }),
        ('Job Information', {
            'fields': ('job_title', 'is_active')
        }),
        ('Related User', {
            'fields': ('user',)
        }),
    )

    # **Raw ID Fields**: Use raw_id_field for user selection to improve performance
    raw_id_fields = ('user',)

    actions = ['activate_employees', 'deactivate_employees']

    def activate_employees(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected employees have been activated.")

    def deactivate_employees(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected employees have been deactivated.")

    activate_employees.short_description = "Activate selected employees"
    deactivate_employees.short_description = "Deactivate selected employees"

    readonly_fields = ('user',)

    list_per_page = 10
