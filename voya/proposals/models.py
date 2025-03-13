"""
Copyright (C) 2025 DROMO SA

This file is part of VOYA.

VOYA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[Project Name] is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from simple_history.models import HistoricalRecords

from voya.common.models import TimestampedModel
from voya.proposals.choices import SectionChoices, StatusChoices
from voya.requests import choices
from voya.requests.models import TripRequests
from voya.services.models import Currency


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

    status = models.CharField(
        max_length=50,
        choices=StatusChoices,
        blank=False,
        null=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    internal_comments = models.TextField(
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.title} - {self.trip_request.created_by_company.commercial_name}'


class ProposalSectionItem(TimestampedModel):
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

    # city = models.CharField(
    #     max_length=50,
    #     choices=choices.CityChoices,
    #     blank=False,
    #     null=False,
    # )

    city = models.ForeignKey(
        'services.Location',
        on_delete=models.RESTRICT,
        blank=False,
        null=False,
        related_name='item_city',
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.proposal.title} - {self.section_name}'


class ProposalBudget(TimestampedModel):
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

    free_of_charge = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
    )

    free_of_charge_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
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

    history = HistoricalRecords()
