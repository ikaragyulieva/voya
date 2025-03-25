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
import logging

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from simple_history.utils import update_change_reason

from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.proposals.serializers import ProposalSerializer, ItemSerializer, BudgetSerializer
from voya.requests.models import TripRequests
from voya.services.models import Location

logger = logging.getLogger(__name__)


def save_proposal(data, user):
    """Creates a new proposal along with its items and budget."""

    with transaction.atomic():
        trip = TripRequests.objects.get(id=data.get('trip_id'))

        # Create Proposal
        proposal = Proposal.objects.create(
            trip_request=trip,
            user=user,
            title=data['proposal'].get('title'),
            status=data['proposal'].get('status'),
            internal_comments=data['proposal'].get('internal_comments'),
        )

        proposal.history_user = user
        update_change_reason(
            proposal,
            "Proposal created via API"
        )

        # Save items and budget
        created_items = save_items(proposal, data.get('items', []))
        created_budgets = save_budget(proposal, data.get('budget', []))

        return proposal, created_items, created_budgets


def update_proposal(proposal, data, user):
    """Updates an existing proposal along with its items and budget."""

    logger.warning(f"update_proposal() called for proposal {proposal.id}")
    with transaction.atomic():
        proposal_serializer = ProposalSerializer(proposal, data=data['proposal'], partial=True)
        proposal_serializer.is_valid(raise_exception=True)

        if has_changes(proposal, proposal_serializer.validated_data):
            proposal = proposal_serializer.save()

            update_change_reason(proposal, "Proposal updated via API")
            proposal.history_user = user
            logger.warning(f"✅ Proposal updated")
        else:
            logger.warning("⚪ No changes for Proposal")


        # Update or recreate proposal items
        existing_items = ProposalSectionItem.objects.filter(proposal=proposal)
        existing_items_map = {str(item.id): item for item in existing_items}
        received_items_ids = set()

        created_or_updated_items = []

        for item_data in data.get('items', []):
            raw_id = item_data.get("id")
            item_id = str(raw_id) if raw_id is not None else None
            # item_id = str(item_data.get('id', ''))  # ID from the frontend, if exists

            instance = existing_items_map.get(item_id) if item_id else None
            if instance:
                #  Update existing item
                serializer = ItemSerializer(instance, data=item_data, partial=True)
                action = "updated"
            else:
                #  Create new item if it doesn't exist
                serializer = ItemSerializer(data=item_data)
                action = "created"
                logger.warning("🟢 Creating new item")

            serializer.is_valid(raise_exception=True)

            if instance and not has_changes(instance, serializer.validated_data):
                item = serializer.instance  # just use existing one
                logger.warning(f"⚪ No changes for Item ID: {item.id}")
            else:
                item = serializer.save(proposal=proposal)

            if item:
                item.history_user = user
                update_change_reason(
                    item,
                    f"Item {action}: {item.section_name} - “{item.additional_notes or 'No notes'}” – €{item.price} x {item.quantity} on {item.corresponding_trip_date} in {item.city}")
                # item.save()
                logger.warning(f"✅ Item {action}: ID {item.id}")

                created_or_updated_items.append(item)

            received_items_ids.add(item.id)

        # delete removed items
        to_delete_items = ProposalSectionItem.objects.filter(proposal=proposal).exclude(id__in=received_items_ids)
        for item in to_delete_items:
            item.history_user = user
            update_change_reason(
                item,
                f"Item deleted: {item.section_name} – “{item.additional_notes or 'No notes'}” – €{item.price} x {item.quantity} on {item.corresponding_trip_date} in {item.city}"
            )

        logger.warning(f"🗑️ Deleting {to_delete_items.count()} items: {[i.id for i in to_delete_items]}")
        to_delete_items.delete()

        # Update or create proposal budgets
        existing_budgets = ProposalBudget.objects.filter(proposal=proposal)
        existing_budgets_map = {str(b.id): b for b in existing_budgets}
        received_budget_ids = set()

        created_or_updated_budgets = []

        for budget_data in data.get('budget', []):
            raw_id = budget_data.get("id")
            budget_id = str(raw_id) if raw_id is not None else None

            instance = existing_budgets_map.get(budget_id) if budget_id else None

            if instance:
                # Update existing budget

                serializer = BudgetSerializer(instance, data=budget_data, partial=True)
                action = "updated"
            else:
                # Create new budget if it doesn’t exist
                serializer = BudgetSerializer(data=budget_data)
                action = "created"
                logger.warning("🟢 Creating new budget")

            serializer.is_valid(raise_exception=True)

            if instance and not has_changes(instance, serializer.validated_data):
                budget = serializer.instance
                logger.warning(f"⚪ No changes for Budget: {budget.id}")
            else:
                budget = serializer.save(proposal=proposal)
                if budget:
                    budget.history_user = user
                    update_change_reason(budget, f"Budget {action} via API")
                    # budget.save()
                    logger.warning(f"✅ Budget {action}: ID {budget.id}")

                    created_or_updated_budgets.append(budget)

            received_budget_ids.add(budget.id)

        # Remove budgets not in received data (handle deleted budgets)
        to_delete_budgets = ProposalBudget.objects.filter(proposal=proposal).exclude(id__in=received_budget_ids)
        logger.warning(f"🗑️ Deleting {to_delete_budgets.count()} items: {[i.id for i in to_delete_budgets]}")
        to_delete_budgets.delete()

        return proposal, created_or_updated_items, created_or_updated_budgets


def save_items(proposal, items_data):
    """Creates and saves proposal items."""
    created_items = []
    for item_data in items_data:
        # Fetch linked services
        city_id = item_data.get('city') if isinstance(item_data.get('city'), int) else None

        if city_id:
            try:
                city = Location.objects.get(id=city_id)
            except Location.DoesNotExist:
                return Response({'error': 'Invalid city ID'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'City ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the item
        new_item = ProposalSectionItem.objects.create(
            proposal=proposal,
            section_name=item_data.get('section_name'),
            service_id=item_data.get('service_id', None),
            quantity=item_data.get('quantity'),
            additional_notes=item_data.get('additional_notes', ''),
            corresponding_trip_date=item_data.get('corresponding_trip_date'),
            price=item_data.get('price'),
            city=city,
        )

        new_item.history_user = proposal.user
        update_change_reason(
            new_item,
            f"Item created: {new_item.section_name} – “{new_item.additional_notes or 'No notes'}” – €{new_item.price} x {new_item.quantity} on {new_item.corresponding_trip_date} in {new_item.city}"
        )
        new_item.save()
        created_items.append(new_item)

    return created_items


def save_budget(proposal, budget_data):
    """Creates and saves proposal budgets."""
    created_budgets = []
    for budget_entry in budget_data:
        budget = ProposalBudget.objects.create(
            proposal=proposal,
            pax=budget_entry.get('pax'),
            variable_cost=budget_entry.get('variable_cost'),
            fixed_cost=budget_entry.get('fixed_cost'),
            free_of_charge=budget_entry.get('free_of_charge'),
            free_of_charge_amount=budget_entry.get('free_of_charge_amount'),
            total_cost_per_person=budget_entry.get('total_cost_per_person'),
            total_cost=budget_entry.get('total_cost'),
            service_fee=budget_entry.get('service_fee'),
            margin=budget_entry.get('margin'),
            fina_price_per_person=budget_entry.get('fina_price_per_person'),
            final_price=budget_entry.get('final_price'),
        )

        budget.bistory_user = proposal.user
        update_change_reason(
            budget,
            f"Budget created: {budget.pax} pax – Total: €{budget.total_cost} – Price/pp: €{budget.fina_price_per_person} – Margin: {budget.margin}%"
        )
        budget.save()
        created_budgets.append(budget)
    return created_budgets


def has_changes(instance, validated_data):
    for field, new_value in validated_data.items():
        old_value = getattr(instance, field)
        if old_value != new_value:
            return True
    return False
