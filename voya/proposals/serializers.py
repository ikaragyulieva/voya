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
from django.utils.translation import gettext_lazy as _
from voya.proposals.choices import SectionChoices, StatusChoices
from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.requests import choices
from voya.services.models import Location


class ProposalSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=255,
        error_messages={
            'blank': _('The proposal title is required.'),
            'max_length': _('The title must not exceed 255 characters.'),
        }
    )

    status = serializers.ChoiceField(
        choices=StatusChoices,
        error_messages={
            'invalid_choice': _('Invalid status. Please select a valid status from the dropdown.'),
        }
    )

    internal_comments = serializers.CharField(allow_blank=True, max_length=None)

    class Meta:
        model = Proposal
        fields = ["title", "status", "internal_comments"]

    def create(self, validated_data):
        return Proposal.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ItemSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField()

    service_id = serializers.IntegerField(
        required=False,  # Allow missing service_id
        allow_null=True,  # Allow null value
        default=None,
        error_messages={'invalid': _('Invalid service ID.')}
    )

    quantity = serializers.IntegerField(
        min_value=1,
        error_messages={
            'min_value': _('Quantity must be at least 1.'),
            'invalid': _('Quantity must be a number.'),
        }
    )
    additional_notes = serializers.CharField(allow_blank=True)
    corresponding_trip_date = serializers.DateField(
        error_messages={
            'invalid': _('Invalid date format. Please use YYYY-MM-DD.'),
            'null': _('Trip date is required.'),
        }
    )
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    city = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        error_messages={
            'does_not_exist': _('Invalid city section.')
        }
    )

    order = serializers.IntegerField(required=False)

    class Meta:
        model = ProposalSectionItem
        fields = [
            "section_name",
            "service_id",
            "quantity",
            "additional_notes",
            "corresponding_trip_date",
            "price",
            "city",
            "order",
        ]

    def create(self, validated_data):
        return ProposalSectionItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BudgetSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = ProposalBudget
        fields = [
            "pax",
            "variable_cost",
            "fixed_cost",
            "free_of_charge",
            "free_of_charge_amount",
            "total_cost_per_person",
            "total_cost",
            "service_fee",
            "margin",
            "fina_price_per_person",
            "final_price",
        ]

    def create(self, validated_data):
        return ProposalBudget.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
