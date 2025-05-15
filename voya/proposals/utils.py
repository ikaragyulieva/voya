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

from django.apps import apps
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from simple_history.utils import update_change_reason

from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.proposals.serializers import ProposalSerializer, ItemSerializer, BudgetSerializer
from voya.requests.models import TripRequests
from voya.services.models import Location

logger = logging.getLogger(__name__)

# SECTION KEYS (internal identifiers)
SECTION_KEYS = {
    "Accommodations": _("Accommodations"),
    "Public Transport": _("Public Transport"),
    "Private Transport": _("Private Transport"),
    "Transfers": _("Transfers"),
    "Extra Activities": _("Extra Activities"),
    "Activity": _("Activity"),
    "Local Guides": _("Local Guides"),
    "Tour Leader": _("Tour Leader"),
    "Meals": _("Meals"),
    "Other Services - Variable": _("Other Services - Variable"),
    "Other Services": _("Other Services"),
    "Other Services - Fixed": _("Other Services - Fixed"),

}

# Reverse translated label to key
REVERSE_SECTION_KEYS = {str(v): k for k, v in SECTION_KEYS.items()}

# MODEL MAP based on SECTION KEY
SECTION_MODEL_MAP = {
    "Accommodations": "Hotel",
    "Public Transport": "PublicTransport",
    "Private Transport": "PrivateTransport",
    "Transfers": "Transfer",
    "Extra Activities": "Ticket",
    "Activity": "Ticket",
    "Local Guides": "LocalGuide",
    "Tour Leader": "Staff",
    # MEALS / OTHER_FIXED / OTHER_VARIABLE don't map to services directly
}


# JS Injection helper (in context processors and views)
def get_section_context():
    return {
        "section_keys": SECTION_KEYS,
        "reverse_section_keys": REVERSE_SECTION_KEYS,
        "section_model_map": SECTION_MODEL_MAP,
    }


def group_items_by_section(items):
    section_items_map = {key: [] for key in SECTION_KEYS.keys()}

    for item in items:
        section_key = item.section_name

        # Handel model lookup only for service-related sections
        if section_key in SECTION_MODEL_MAP:
            model_name = SECTION_MODEL_MAP[section_key]
            try:
                service_model = apps.get_model("services", model_name)
                service_object = service_model.objects.get(id=item.service_id)

                # Fetch the name based on the service label
                item.service_name = getattr(service_object, "name", None) or getattr(service_object, "type", None)
            except Exception:
                item.section_name = None

        # Append item to its appropriate group
        if section_key in section_items_map:
            section_items_map[section_key].append(item)

    return section_items_map


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
            _("Proposal created via API")
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

            update_change_reason(proposal, _("Proposal updated via API"))
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
                action = _("updated")
            else:
                #  Create new item if it doesn't exist
                serializer = ItemSerializer(data=item_data)
                action = _("created")
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
                    _("Item %(action)s: %(section_name)s - “%(additional_notes)s” – €%(price)s x %(quantity)s on %(corresponding_trip_date)s in %(city)s") % {
                        'action': action,
                        'section_name': item.section_name,
                        'additional_notes': item.additional_notes or _('No notes'),
                        'price': item.price,
                        'quantity': item.quantity,
                        'corresponding_trip_date': item.corresponding_trip_date,
                        'city': item.city,
                    }
                )
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
                _("Item deleted: %(section_name)s – “%(additional_notes)s” – €%(price)s x %(quantity)s on %(corresponding_trip_date)s in %(city)s") % {
                    'section_name': item.section_name,
                    'additional_notes': item.additional_notes or _('No notes'),
                    'price': item.price,
                    'quantity': item.quantity,
                    'corresponding_trip_date': item.corresponding_trip_date,
                    'city': item.city,
                }
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
                action = _("updated")
            else:
                # Create new budget if it doesn’t exist
                serializer = BudgetSerializer(data=budget_data)
                action = _("created")
                logger.warning("🟢 Creating new budget")

            serializer.is_valid(raise_exception=True)

            if instance and not has_changes(instance, serializer.validated_data):
                budget = serializer.instance
                logger.warning(f"⚪ No changes for Budget: {budget.id}")
            else:
                budget = serializer.save(proposal=proposal)
                if budget:
                    budget.history_user = user
                    update_change_reason(budget, _("Budget %(action)s via API") % {'action': action})
                    # budget.save()
                    logger.warning(f"✅ Budget {action}: ID {budget.id}")

                    created_or_updated_budgets.append(budget)

            received_budget_ids.add(budget.id)

        # Remove budgets not in received data (handle deleted budgets)
        to_delete_budgets = ProposalBudget.objects.filter(proposal=proposal).exclude(id__in=received_budget_ids)
        logger.warning(f"🗑️ Deleting {to_delete_budgets.count()} items: {[i.id for i in to_delete_budgets]}")
        to_delete_budgets.delete()

        return proposal, created_or_updated_items, created_or_updated_budgets


def clone_proposal_data(original_proposal, new_request, user):
    """Clones an existing proposal along with its items and budget."""

    items_data = []
    for item in original_proposal.items.all():
        items_data.append({
            'section_name': item.section_name,
            'service_id': item.service_id,
            'quantity': item.quantity,
            'additional_notes': item.additional_notes,
            'corresponding_trip_date': item.corresponding_trip_date,
            'price': item.price,
            'city': item.city_id,
        })

    budget_data = []
    for budget in original_proposal.budget.all():
        budget_data.append({
            'pax': budget.pax,
            'variable_cost': budget.variable_cost,
            'fixed_cost': budget.fixed_cost,
            'free_of_charge': budget.free_of_charge,
            'free_of_charge_amount': budget.free_of_charge_amount,
            'total_cost_per_person': budget.total_cost_per_person,
            'total_cost': budget.total_cost,
            'service_fee': budget.service_fee,
            'margin': budget.margin,
            'fina_price_per_person': budget.fina_price_per_person,
            'final_price': budget.final_price,
        })

    # Construct the payload and call proposal, items and budget save functions
    payload = {
        'trip_id': new_request.id,
        'proposal': {
            'title': f"{new_request.slug}",
            'status': 'Not finished',
            'internal_comments': original_proposal.internal_comments or "",
        },
        'items': items_data,
        'budget': budget_data,
    }

    save_proposal(payload, user)


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
                return Response({'error': _('Invalid city ID')}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': _('City ID is required')}, status=status.HTTP_400_BAD_REQUEST)

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
            _("Item created: %(section_name)s – “%(additional_notes)s” – €%(price)s x %(quantity)s on %(corresponding_trip_date)s in %(city)s") % {
                'section_name': new_item.section_name,
                'additional_notes': new_item.additional_notes or _('No notes'),
                'price': new_item.price,
                'quantity': new_item.quantity,
                'corresponding_trip_date': new_item.corresponding_trip_date,
                'city': new_item.city,
            }
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

        budget.history_user = proposal.user
        update_change_reason(
            budget,
            _("Budget created: %(pax)s pax – Total: €%(total_cost)s – Price/pp: €%(fina_price_per_person)s – Margin: %(margin)s%%") % {
                'pax': budget.pax,
                'total_cost': budget.total_cost,
                'fina_price_per_person': budget.fina_price_per_person,
                'margin': budget.margin,
            }
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
