from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField
from voya.common.models import TimestampedModel


# Create your models here.


class Request(TimestampedModel):
    country_origin = CountryField(
        blank_label='Select your country of origin',
        null=False,
        blank=False,
    )

    nationality = CountryField(
        blank_label='Select your nationality',
        null=False,
        blank=False,
    )

    destinations = models.TextField(
        null=False,
        blank=False,
    )

    budget = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    trip_duration = models.IntegerField()

    # trip_start_date = models.DateField(
    #     null=False,
    #     blank=False,)
    #
    # trip_end_date = models.DateField(
    #     null=False,
    #     blank=False,
    # )

    age_range = models.IntegerField(
        null=False,
        blank=False,
    )




    def clean(self):
        if self.trip_end_date <= self.trip_start_date:
            raise ValidationError("End date must be after the start date.")

