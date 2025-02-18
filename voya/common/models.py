from django.apps import apps
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from voya.providers.models import Providers
from voya.requests import choices
from voya.users.models import CustomUser


# Create your models here.


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServiceBaseModel(TimestampedModel):
    country = models.CharField(
        max_length=100,
        choices=choices.CountryChoices,
        blank=False,
        null=False,
        default='cc',
    )

    city = models.CharField(
        max_length=50,
        choices=choices.CityChoices,
        blank=False,
        null=False,
        default="Select city",
    )

    capacity = models.PositiveIntegerField(
        default=1,
        blank=False,
        null=False,
    )

    telephone_number = PhoneNumberField(
        blank=True,
        null=True,
        help_text="Enter phone number in international format. Example: +123456789"
    )

    email = models.EmailField(
        blank=True,
        null=True,
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

    provider = models.ForeignKey(
        Providers,
        on_delete=models.CASCADE,
        related_name='%(class)s_provider',
    )

    created_by_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='%(class)s_created_by',
    )

    class Meta:
        abstract = True
