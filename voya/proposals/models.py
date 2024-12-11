from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from voya.common.models import TimestampedModel
from voya.proposals.choices import SectionChoices
from voya.requests import choices
from voya.requests.models import TripRequests
from voya.services.models import Currency

# Create your models here.

User = get_user_model()


class Proposal(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_proposal",
    )

    trip_request = models.OneToOneField(
        TripRequests,
        on_delete=models.CASCADE,
        related_name='request_proposal'
    )

    title = models.CharField(
        max_length=255,
    )

    is_draft = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.title} - {self.trip_request.created_by_company.commercial_name}'


class ProposalSectionItem(models.Model):
    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        related_name='items',
        blank=False,
        null=False,
    )

    section_name = models.CharField(
        max_length=50,
        choices=SectionChoices,
        blank=False,
        null=False,
    )

    service_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    quantity = models.PositiveIntegerField(
        # default=1,
        blank=False,
        null=False,
    )

    additional_notes = models.TextField(
        blank=True,
        null=True,
    )

    corresponding_trip_date = models.DateField(
        blank=False,
        null=False,
    )

    city = models.CharField(
        max_length=50,
        choices=choices.CityChoices,
        blank=False,
        null=False,
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    def __str__(self):
        return f'{self.proposal.title} - {self.section_name}'


class ProposalBudget(models.Model):
    pax = models.PositiveIntegerField(
        blank=False,
        null=False,
    )

    variable_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )

    fixed_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )

    total_cost_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )

    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )

    service_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        default=500.00,
    )

    margin = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=10,
    )

    fina_price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )

    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )

    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        related_name='budget',
    )
