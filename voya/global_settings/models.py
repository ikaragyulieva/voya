from django.db import models

from voya.common.models import TimestampedModel
from voya.services.models import Location


# Create your models here.


class BankAccounts(TimestampedModel):
    iban = models.CharField(
        max_length=34,
        unique=True,
        blank=False,
        null=False,
        verbose_name="IBAN",
    )

    swift = models.CharField(
        max_length=11,
        blank=False,
        null=False,
        verbose_name="SWIFT/BIC Code"
    )

    beneficiary = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Beneficiary Name"
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='bank_location',
    )

    street = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Street"
    )

    postal_code = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name="Postal Code (CP)"
    )

    class Meta:
        verbose_name = "Bank Accounts"
        verbose_name_plural = "Bank Accounts"
        ordering = ["beneficiary"]

    def __str__(self):
        return f"{self.beneficiary} - {self.iban}"


class PaymentConditions(TimestampedModel):
    pass


class CancellationTerms(TimestampedModel):
    pass
