from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from voya.clients.choices import TitleChoices
from voya.common.models import TimestampedModel
from voya.users.models import CustomUser


class EmployeeProfile(TimestampedModel):

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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')

    def __str__(self):
        return f"Employee Profile for {self.user.email}"
