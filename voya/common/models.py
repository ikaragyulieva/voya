from django.db import models

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

    capacity = models.IntegerField(
        default=1,
        blank=False,
        null=False,
    )

    is_active = models.BooleanField(
        default=True
    )

    created_by_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='%(class)s_created_by',
    )

    class Meta:
        abstract = True
