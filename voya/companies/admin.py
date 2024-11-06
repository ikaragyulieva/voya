from django.contrib import admin
from .models import CompanyProfile, Address, PhoneNumber


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('commercial_name', 'tax_id', 'country')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('company', 'street_address', 'city', 'state', 'postal_code', 'country')


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('company', 'number', 'label')
