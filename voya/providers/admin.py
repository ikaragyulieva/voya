from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from voya.providers.models import Providers


# Register your models here.

@admin.register(Providers)
class ProvidersAdmin(admin.ModelAdmin):
    list_display = (
        'commercial_name',
        'services',
        'country',
        'city',
        'is_active',
        'updated_at',
    )

    search_fields = (
        'commercial_name',
        'services',
        'country',
    )

    list_filter = (
        'services',
        'is_active',
        'commercial_name',
        'country',
    )

    ordering = ('commercial_name',)

    fieldsets = (
        (_('General Information'), {
            'fields': (
                'commercial_name',
                'services',
                'description',
            )
        }),
        (_('Contact Information'), {
            'fields': (
                'country',
                'city',
                'telephone_number',
                'email',
                'website',
            )
        }),
        (_('Status'), {
            'fields': (
                'is_active',
                'created_at',
                'updated_at',
                'created_by_user',
            )
        }),
    )

    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected providers have been marked as active."))
    mark_active.short_description = _("Mark selected providers as active")

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected providers have been marked as inactive."))
    mark_inactive.short_description = _("Mark selected providers as inactive")
