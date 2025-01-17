from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField
from voya.common.models import TimestampedModel
from voya.companies.models import CompanyProfile
from voya.requests import choices
from voya.users.models import CustomUser


# Create your models here.


class TripRequests(TimestampedModel):

    country_origin = CountryField(
        blank_label='Select country',
        null=False,
        blank=False,
    )

    nationality = CountryField(
        blank_label='Select nationality',
        null=False,
        blank=False,
    )

    country_destinations = MultiSelectField(
        max_length=100,
        choices=choices.CountryChoices,
        help_text='Choose the countries you would like to visit',
    )

    city_destinations = MultiSelectField(
        choices=choices.CityChoices,
    )

    other_destinations = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    budget = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    trip_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    trip_start_date = models.DateField(
        null=False,
        blank=False,
    )

    trip_end_date = models.DateField(
        null=False,
        blank=False,
    )

    age_range = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    min_participants = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    max_participants = models.PositiveIntegerField(
        null=False,
        blank=False,
    )

    currency = models.CharField(
        max_length=20,
        choices=choices.CurrencyChoices.choices,
        null=False,
        blank=False,
        default='currency',

    )

    transportation_type = models.CharField(
        max_length=100,
        choices=choices.TransportationType,
        blank=False,
        null=False,
        default='transport',
    )

    transportation_details = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    accommodations = models.CharField(
        max_length=100,
        choices=choices.AccommodationsType,
        blank=False,
        null=False,
        default='acc',
    )

    accommodations_details = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    meals = models.CharField(
        max_length=50,
        choices=choices.MealsType,
        null=True,
        blank=True,
        default='meal',
    )

    meals_details = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    staff = models.CharField(
        max_length=50,
        choices=choices.StaffChoices,
        null=True,
        blank=True,
        default='staff',
    )

    kind_of_group = models.CharField(
        max_length=100,
        choices=choices.GroupChoice,
        null=True,
        blank=True,
        default='group',
    )

    type_of_trip = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    additional_observations = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True
    )

    created_by_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='request_user',
    )

    created_by_company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name='request_company'
    )

    slug = models.SlugField(
        # unique=True,
        null=False,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.slug} - {self.created_by_company.commercial_name}"

    def clean(self):

        if self.trip_start_date and self.trip_end_date:
            if self.trip_end_date <= self.trip_start_date:
                raise ValidationError("End date must be after the start date.")

            today = timezone.now().date()
            if self.trip_start_date <= today:
                raise ValidationError("Start date must be in the future.")

        else:
            raise ValidationError("Both start and end dates must be specified.")

    def save(self, *args, **kwargs):

        date_part = self.trip_start_date.strftime('%y.%m')

        destinations_part = '_'.join([country.upper() for country in self.country_destinations])

        company_part = ''.join([word[0].upper() for word in self.created_by_company.commercial_name.split()])

        self.slug = f"{date_part}-{destinations_part}-{company_part}-{self.pk}"

        super().save(*args, **kwargs)
