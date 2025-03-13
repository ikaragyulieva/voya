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

from rest_framework import serializers

from voya.proposals.choices import SectionChoices, StatusChoices
from voya.requests import choices
from voya.services.models import Location


class ProposalSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255,
        error_messages={
            'blank': 'The proposal title is required.',
            'max_length': 'The title must not exceed 255 characters.',
        }
    )

    status = serializers.ChoiceField(
        choices=StatusChoices,
        error_messages={
            'invalid_choice': 'Invalid status. Please select a valid status from the dropdown.',
        }
    )

    internal_comments = serializers.CharField(allow_blank=True)


class ItemSerializer(serializers.Serializer):
    section_name = serializers.ChoiceField(
        choices=SectionChoices,
        error_messages={
            'invalid_choice': 'Invalid section name. Please select a valid section.',
        }
    )

    service_id = serializers.IntegerField(
        required=False,  # Allow missing service_id
        allow_null=True,  # Allow null value
        default=None,
        error_messages={'invalid': 'Invalid service ID.'}
    )

    quantity = serializers.IntegerField(
        min_value=1,
        error_messages={
            'min_value': 'Quantity must be at least 1.',
            'invalid': 'Quantity must be a number.',
        }
    )
    additional_notes = serializers.CharField(allow_blank=True)
    corresponding_trip_date = serializers.DateField(
        error_messages={
            'invalid': 'Invalid date format. Please use YYYY-MM-DD.',
            'null': 'Trip date is required.',
        }
    )
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    city = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        error_messages={
            'does_not_exist': 'Invalid city section.'
        }
    )


class BudgetSerializer(serializers.Serializer):
    pax = serializers.IntegerField()
    variable_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    fixed_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    free_of_charge = serializers.IntegerField()
    free_of_charge_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cost_per_person = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    service_fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    margin = serializers.IntegerField()
    fina_price_per_person = serializers.DecimalField(max_digits=10, decimal_places=2)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2)
