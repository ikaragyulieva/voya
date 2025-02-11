from django import forms

from voya.common.mixins import PlaceholderMixin, StyledFormMixin
from voya.companies.models import CompanyProfile, Address, PhoneNumber
from cloudinary.forms import CloudinaryFileField

from voya.companies.validators import FileSizeValidator


class CompanyProfileForm(forms.ModelForm):
    logo = CloudinaryFileField(
        options={
            'folder': 'uploads/',
            'tags': ['company-logo'],
            'resource_type': 'auto',
            'editable': True,
        },
        help_text="Please upload your logo here",
        validators=[
            FileSizeValidator(5),
        ]

    )

    class Meta:
        model = CompanyProfile
        exclude = ['notes']
        # widgets = {
        #     'commercial_name': forms.TextInput(attrs={'placeholder': 'Commercial name'}),
        #     'legal_name': forms.TextInput(attrs={'placeholder': 'Legal name'}),
        #     'tax_id': forms.TextInput(attrs={'placeholder': 'VAT/Tax ID'}),
        #     'billing_email': forms.TextInput(attrs={'placeholder': 'Billing email'}),
        #
        # }
        # labels = {
        #     'commercial_name': "",
        #     'legal_name': "",
        #     'tax_id': "",
        #     'billing_email': "",
        #     'logo': "",
        # }


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['country', 'street_address', 'city', 'state', 'postal_code',]
        # widgets = {
        #     'street_address': forms.TextInput(attrs={'placeholder': 'Street'}),
        #     'city': forms.TextInput(attrs={'placeholder': 'City'}),
        #     'state': forms.TextInput(attrs={'placeholder': 'State'}),
        #     'postal_code': forms.TextInput(attrs={'placeholder': 'Postal code'}),
        # }
        # labels = {
        #     'country': "",
        #     'street_address': "",
        #     'city': "",
        #     'state': "",
        #     'postal_code': "",
        # }


class PhoneNumberForm(forms.ModelForm):

    class Meta:
        model = PhoneNumber
        fields = ['number']
        # widgets = {
        #     'number': forms.TextInput(attrs={'placeholder': 'Whatsapp number in format: +1234567890'}),
        # }
        # labels = {
        #     'number': "",
        # }
        help_texts = {
            'number': "",
        }
