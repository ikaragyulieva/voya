from django.core.exceptions import ValidationError
from django.db import models

from voya.common.models import TimestampedModel, ServiceBaseModel
from voya.proposals.choices import TransferTypeChoices
from voya.requests import choices
from voya.users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Hotel(ServiceBaseModel):
    category = models.CharField(
        max_length=30,
        choices=choices.HotelType,
        blank=False,
        null=False,
        default='',
    )

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    high_season_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    low_season_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    street_address = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

    zone = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    zone_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )


class Transfer(ServiceBaseModel):
    transfer_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    type = models.CharField(
        max_length=50,
        choices=TransferTypeChoices,
        default='',
        blank=False,
        null=False,
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )


class LocalGuide(ServiceBaseModel):
    name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    price_includes = models.CharField(
        max_length=200,
        blank=False,
        null=False,
    )

    tour_description = models.TextField(
        blank=False,
        null=False,
    )

    label = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )


class Staff(ServiceBaseModel):
    name = models.CharField(
        max_length=80,
        blank=False,
        null=False,
    )

    mansion = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    price_includes = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    tour_description = models.TextField(
        blank=True,
        null=True,
    )

    label = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )


class Ticket(ServiceBaseModel):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    type = models.CharField(
        max_length=20,
        choices=choices.ActivityTypeChoices,
        blank=False,
        null=False,
        default='choice',
    )


class Currency(TimestampedModel):
    currency_from = models.CharField(
        max_length=10,
        choices=choices.CurrencyChoices,
        blank=False,
        null=False,
        default='',
    )

    currency_to = models.CharField(
        max_length=10,
        choices=choices.CurrencyChoices,
        default=choices.CurrencyChoices.EUR,
        blank=False,
        null=False,
    )

    exchange_rate = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=False,
        null=False,
    )

    is_active = models.BooleanField(
        default=True
    )

    created_by_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='currency_created_by',
    )


class PublicTransport(ServiceBaseModel):
    type = models.CharField(
        max_length=30,
        choices=choices.PublicTransportationType,
        blank=False,
        null=False,
        default="",
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )


class PrivateTransport(ServiceBaseModel):
    type = models.CharField(
        max_length=30,
        choices=choices.PrivateTransportationType,
        blank=False,
        null=False,
        default="",
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )
