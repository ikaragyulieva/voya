from django.contrib import admin
from .models import CompanyProfile, Address, PhoneNumber
from django.utils.translation import gettext_lazy as _


class AddressInline(admin.TabularInline):  # Define AddressInline
    model = Address
    extra = 1  # Number of empty forms displayed in the inline


class PhoneNumberInline(admin.TabularInline):  # Define PhoneNumberInline
    model = PhoneNumber
    extra = 1  # Number of empty forms displayed in the inline


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = (
        'commercial_name',
        'legal_name',
        'tax_id',
        'billing_email',
        'is_active',
    )

    search_fields = (
        'commercial_name',
        'legal_name',
        'tax_id',
        'billing_email',
    )

    list_filter = (
        'is_active',
    )

    ordering = ('commercial_name',)

    fieldsets = (
        (_('Company Information'), {
            'fields': (
                'commercial_name',
                'legal_name',
                'tax_id',
                'billing_email',
                'logo',
            )
        }),
        (_('Additional Details'), {
            'fields': (
                'notes',
                'is_active',
            )
        }),
    )
    # **Inline Editing**: Allow editing related addresses and phone numbers inline
    inlines = [AddressInline, PhoneNumberInline]

    actions = ['activate_companies', 'deactivate_companies']

    def activate_companies(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected companies have been activated."))

    def deactivate_companies(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected companies have been deactivated."))

    activate_companies.short_description = _("Activate selected companies")
    deactivate_companies.short_description = _("Deactivate selected companies")

    readonly_fields = ('logo',)

    list_per_page = 10


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'city',
        'country',
        'is_active',
    )

    search_fields = (
        'is_active',
        'company__commercial_name',
        'city',
        'country',
    )

    list_filter = (
        'country',
        'is_active',
    )

    ordering = ('company', 'country', 'city')

    fieldsets = (
        (_('Address Details'), {
            'fields': (
                'company',
                'street_address',
                'city',
                'state',
                'postal_code',
                'country',
            )
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

    # **Raw ID Fields**: Use raw_id_field for better performance
    raw_id_fields = ('company',)

    actions = ['activate_addresses', 'deactivate_addresses']

    def activate_addresses(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected addresses have been activated."))

    def deactivate_addresses(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected addresses have been deactivated."))

    activate_addresses.short_description = _("Activate selected addresses")
    deactivate_addresses.short_description = _("Deactivate selected addresses")

    list_per_page = 10


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'number',
        'is_active',
    )

    search_fields = (
        'number',
        'company__commercial_name',
    )

    list_filter = (
        'is_active',
    )

    ordering = ('company', 'number')

    raw_id_fields = ('company',)

    actions = ['activate_numbers', 'deactivate_numbers']

    def activate_numbers(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected phone numbers have been activated."))

    def deactivate_numbers(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected phone numbers have been deactivated."))

    activate_numbers.short_description = _("Activate selected phone numbers")
    deactivate_numbers.short_description = _("Deactivate selected phone numbers")

    list_per_page = 10
