from django.core.validators import MinLengthValidator
from django.db import models
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField

from voya.requests.choices import CountryChoices, CityChoices
from voya.users.models import CustomUser

from voya.providers import choices


class Providers(models.Model):
    commercial_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(2),
        ]
    )
    services = MultiSelectField(
        max_length=100,
        blank=False,
        null=False,
        choices=choices.ServiceChoices,
        help_text='Select a service',
    )

    country = CountryField(
        blank=False,
        null=False,
        blank_label="Select country",
    )

    city = models.ForeignKey(
        'services.Location',
        on_delete=models.RESTRICT,
        blank=False,
        null=False,
        related_name='provider_city',
    )

    # city = models.CharField(
    #     max_length=50,
    #     choices=CityChoices,
    #     blank=False,
    #     null=False,
    #     default="Select city",
    # )

    telephone_number = PhoneNumberField(
        blank=False,
        null=False,
        help_text="Enter phone number in international format. Example: +123456789"
    )

    email = models.EmailField(
        blank=False,
        null=False,
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='provider_created_by',
    )

    def __str__(self):
        return self.commercial_name
