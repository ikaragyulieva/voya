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
        fields = "__all__"


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['country', 'street_address', 'city', 'state', 'postal_code',]


class PhoneNumberForm(forms.ModelForm):

    class Meta:
        model = PhoneNumber
        fields = ['number']
        help_texts = {
            'number': "",
        }
