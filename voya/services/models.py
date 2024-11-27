from django.db import models

from voya.common.models import TimestampedModel, ServiceBaseModel
from voya.proposals.choices import TransferTypeChoices
from voya.requests import choices
from voya.users.models import CustomUser


# Create your models here.


class Hotels(ServiceBaseModel):
    category = models.CharField(
        max_length=30,
        choices=choices.AccommodationsType,
        blank=False,
        null=False,
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


class Transfers(ServiceBaseModel):
    transfer_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    type = models.CharField(
        max_length=50,
        choices=TransferTypeChoices
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )


class LocalGuides(ServiceBaseModel):
    guide_name = models.CharField(
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

    tour_duration = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )


class Tickets(ServiceBaseModel):
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

    description = models.TextField(
        blank=True,
        null=True,
    )


class Currency(TimestampedModel):
    currency_from = models.CharField(
        max_length=10,
        choices=choices.CurrencyChoices,
        blank=False,
        null=False,
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
        choices=choices.TransportationType,
        blank=False,
        null=False,
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )


class PrivateTransport(ServiceBaseModel):
    type = models.CharField(
        max_length=30,
        choices=choices.TransportationType,
        blank=False,
        null=False,
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
