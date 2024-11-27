from django.contrib import admin
from .models import CompanyProfile, Address, PhoneNumber


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('commercial_name', 'legal_name', 'tax_id', 'is_active')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('company', 'street_address', 'city', 'state', 'postal_code', 'country', 'is_active')


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('company', 'number', 'is_active')
