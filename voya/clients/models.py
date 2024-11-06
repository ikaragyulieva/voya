from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from voya.clients.choices import TitleChoices
from voya.common.models import TimestampedModel
from voya.companies.models import CompanyProfile
from voya.users.models import CustomUser


class ClientProfile(TimestampedModel):
    title = models.CharField(
        max_length=10,
        choices=TitleChoices.choices,
    )

    first_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(2),

        ]

    )

    last_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(2),

        ]

    )

    job_title = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(2),

        ]
    )

    phone_number = PhoneNumberField(
        blank=False,
        null=False,

    )

    is_active = models.BooleanField(
        default=True,
    )

    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name='agent',
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='client_profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
