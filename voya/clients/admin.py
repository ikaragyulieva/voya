from django.contrib import admin

from voya.clients.models import ClientProfile


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'job_title',
        'phone_number',
        'company',
        'is_active',
    )

    search_fields = (
        'first_name',
        'last_name',
        'job_title',
        'phone_number',
        'company__commercial_name',
    )

    list_filter = (
        'is_active',
        'company',
        'job_title',
    )

    ordering = ('is_active', 'last_name', 'first_name')

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'title',
                ('first_name', 'last_name'),
                'job_title',
                'phone_number',
            )
        }),
        ('Company Information', {
            'fields': ('company',)
        }),
        ('Account Information', {
            'fields': ('user', 'is_active')
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected profiles have been marked as active.")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected profiles have been marked as inactive.")

    mark_active.short_description = "Mark selected profiles as active"
    mark_inactive.short_description = "Mark selected profiles as inactive"

    readonly_fields = ('user',)

    list_per_page = 10
