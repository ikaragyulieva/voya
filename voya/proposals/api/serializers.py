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
from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from voya.proposals.choices import SectionChoices, StatusChoices
from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.requests import choices
from voya.requests.models import TripRequests
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
    id = serializers.IntegerField(required=False)
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
    additional_notes = serializers.CharField(allow_blank=True, required=False, default='')
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
            "id",
            "section_name",
            "service_id",
            "quantity",
            "additional_notes",
            "corresponding_trip_date",
            "price",
            "city",
            "order",
        ]

    # def create(self, validated_data):
    #     return ProposalSectionItem.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class BudgetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
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
            "id",
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

    # def create(self, validated_data):
    #     return ProposalBudget.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class ProposalCreateUpdateSerializer(serializers.Serializer):
    trip_id = serializers.IntegerField()
    proposal = ProposalSerializer()
    items = ItemSerializer(many=True)
    budget = BudgetSerializer(many=True)

    class Meta:
        ref_name = "ProposalCreateUpdate"

    #     model = Proposal
    #     fields = ["title", "status", "internal_comments", "trip_id", "items", "budget"]

    def _apply_proposal_fields(self, instance: Proposal, data: dict):
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        trip = TripRequests.objects.get(id=validated_data['trip_id'])

        # Create proposal
        prop_data = validated_data["proposal"]
        proposal = Proposal.objects.create(
            trip_request=trip,
            user=user,
            **prop_data,
        )

        # items
        items_data = validated_data.get("items", [])
        for item in items_data:
            ProposalSectionItem.objects.create(proposal=proposal, **item)

        # budget
        budgets_data = validated_data.get("budget", [])
        for b in budgets_data:
            ProposalBudget.objects.create(proposal=proposal, **b)

        return proposal

    @transaction.atomic
    def update(self, instance: Proposal, validated_data):
        user = self.context["request"].user

        # update proposal fields
        self._apply_proposal_fields(instance, validated_data["proposal"])

        # --- Upsert ITEMS by id ---
        existing_items = {i.id: i for i in instance.items.all()}
        seen_items_id = set()
        for item_data in validated_data.get("items", []):
            item_id = item_data.pop("id", None)

            if item_id and item_id in existing_items:
                # update existing
                item = existing_items[item_id]
                for k, v in item_data.items():
                    setattr(item, k, v)
                item.save()
                seen_items_id.add(item_id)
            else:
                new_item = ProposalSectionItem.objects.create(proposal=instance, **item_data)
                seen_items_id.add(new_item.id)

        # delete removed items
        to_delete = [obj for _id, obj in existing_items.items() if _id not in seen_items_id]
        for obj in to_delete:
            obj.delete()

        # --- Upsert BUDGET by id ---
        existing_budgets = {b.id: b for b in instance.budget.all()}
        seen_budget_ids = set()
        for b_data in validated_data.get("budget", []):
            b_id = b_data.pop("id", None)
            if b_id and b_id in existing_budgets:
                b = existing_budgets[b_id]
                for k, v in b_data.items():
                    setattr(b, k, v)
                b.save()
                seen_budget_ids.add(b_id)
            else:
                new_b = ProposalBudget.objects.create(proposal=instance, **b_data)
                seen_budget_ids.add(new_b.id)

        # delete removed budgets
        for _id, b in list(existing_budgets.items()):
            if _id not in seen_budget_ids:
                b.delete()

        return instance
