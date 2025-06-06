from django.core.validators import MinLengthValidator
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField

from voya.common.models import TimestampedModel
from voya.companies.validators import FileSizeValidator
from django.utils.translation import gettext_lazy as _


class CompanyProfile(TimestampedModel):
    commercial_name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(2),
        ]
    )

    legal_name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(2),
        ]
    )

    tax_id = models.CharField(
        max_length=15,
        unique=True,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(5),
        ]
    )

    billing_email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )

    logo = CloudinaryField(
        "company_logos",
        null=False,
        blank=False,
        # validators=[
        #     FileSizeValidator(5),
        # ]
    )

    notes = models.TextField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.commercial_name


class Address(TimestampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name='addresses',
    )

    street_address = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    city = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(4),
        ]
    )

    country = CountryField(
        blank_label=_("Select country"),
        blank=False,
        null=False,
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.street_address}, {self.city}"


class PhoneNumber(TimestampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name='phone_numbers',
    )
    number = PhoneNumberField(
        blank=False,
        null=False,
        help_text=_("Enter phone number in international format. Example: +123456789")
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"Phone: {self.number}"
