from django.core.validators import MinLengthValidator
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from voya.common.models import TimestampedModel
from voya.companies.validators import FileSizeValidator


class CompanyProfile(TimestampedModel):
    commercial_name = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(2),
        ]
    )

    legal_name = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(2),
        ]
    )

    tax_id = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(5),
        ]
    )

    billing_email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )

    logo = models.ImageField(
        upload_to="company_logos/",
        null=False,
        blank=False,
        validators=[
            FileSizeValidator(5),
        ]
    )

    notes = models.TextField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True
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
    )

    city = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    postal_code = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(4),
        ]
    )

    country = CountryField(
        blank_label="Select your country",
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
        help_text="Enter phone number in international format. Example: +123456789"
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"Phone: {self.number}"
