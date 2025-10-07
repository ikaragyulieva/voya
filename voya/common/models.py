from django.apps import apps
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from voya.providers.models import Providers
from voya.requests import choices
from voya.users.models import CustomUser

from django.utils.translation import gettext_lazy as _


# Create your models here.


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServiceBaseModel(TimestampedModel):
    country = CountryField(
        blank_label=_('Select country'),
        null=False,
        blank=False,
    )

    city = models.ForeignKey(
        'Location',
        on_delete=models.RESTRICT,
        blank=False,
        null=False,
        related_name='%(class)s_city',
    )

    capacity = models.PositiveIntegerField(
        default=1,
        blank=False,
        null=False,
    )

    telephone_number = PhoneNumberField(
        blank=True,
        null=True,
        help_text=_("Enter phone number in international format. Example: +123456789")
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

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

