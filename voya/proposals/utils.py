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
from rest_framework import status
from rest_framework.response import Response

from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.requests.models import TripRequests
from voya.services.models import Location


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

        # Save items and budget
        created_items = save_items(proposal, data.get('items', []))
        created_budgets = save_budget(proposal, data.get('budget', []))

        return proposal, created_items, created_budgets


def update_proposal(proposal, data):
    """Updates an existing proposal along with its items and budget."""
    with transaction.atomic():
        proposal.title = data['proposal'].get('title', proposal.title)
        proposal.status = data['proposal'].get('status', proposal.status)
        proposal.internal_comments = data['proposal'].get('internal_comments', proposal.internal_comments)
        proposal.save()

        # Update or recreate proposal items
        existing_items_ids = set(ProposalSectionItem.objects.filter(proposal=proposal).values_list('id', flat=True))
        received_items_ids = set()

        for item_data in data.get('items', []):
            item_id = item_data.get('id')  # ID from the frontend, if exists
            city_id = item_data.get('city')

            try:
                city = Location.objects.get(id=city_id)

            except Location.DoesNotExist:
                return Response({'error': 'Invalid city ID'}, status=status.HTTP_400_BAD_REQUEST)

            if item_id and item_id in existing_items_ids:
                #  Update existing item
                item = ProposalSectionItem.objects.get(id=item_id)
                item.section_name = item_data.get('section_name', item.section_name)
                item.service_id = item_data.get('service_id', item.service_id)
                item.quantity = item_data.get('quantity', item.quantity)
                item.additional_notes = item_data.get('additional_notes', item.additional_notes)
                item.corresponding_trip_date = item_data.get('corresponding_trip_date', item.corresponding_trip_date)
                item.price = item_data.get('price', item.price)
                item.city = city
                item.save()
            else:
                #  Create new item if it doesn't exist
                item = ProposalSectionItem.objects.create(
                    proposal=proposal,
                    section_name=item_data.get('section_name'),
                    service_id=item_data.get('service_id'),
                    quantity=item_data.get('quantity'),
                    additional_notes=item_data.get('additional_notes', ''),
                    corresponding_trip_date=item_data.get('corresponding_trip_date'),
                    price=item_data.get('price'),
                    city=city,
                )

            received_items_ids.add(item.id)

        # Removes item not in received data (handle deleted items)
        ProposalSectionItem.objects.filter(proposal=proposal).exclude(id__in=received_items_ids).delete()

        # Update or create proposal budgets
        existing_budget_ids = set(ProposalBudget.objects.filter(proposal=proposal).values_list('id', flat=True))
        received_budget_ids = set()

        for budget_entry in data.get('budget', []):
            budget_id = budget_entry.get('id')

            if budget_id and budget_id in existing_budget_ids:
                # Update existing budget
                budget = ProposalBudget.objects.get(id=budget_id)
                budget.pax = budget_entry.get('pax', budget.pax)
                budget.variable_cost = budget_entry.get('variable_cost', budget.variable_cost)
                budget.fixed_cost = budget_entry.get('fixed_cost', budget.fixed_cost)
                budget.free_of_charge = budget_entry.get('free_of_charge', budget.free_of_charge)
                budget.free_of_charge_amount = budget_entry.get('free_of_charge_amount', budget.free_of_charge_amount)
                budget.total_cost_per_person = budget_entry.get('total_cost_per_person', budget.total_cost_per_person)
                budget.total_cost = budget_entry.get('total_cost', budget.total_cost)
                budget.service_fee = budget_entry.get('service_fee', budget.service_fee)
                budget.margin = budget_entry.get('margin', budget.margin)
                budget.fina_price_per_person = budget_entry.get('fina_price_per_person', budget.fina_price_per_person)
                budget.final_price = budget_entry.get('final_price', budget.final_price)
                budget.save()
            else:
                # Create new budget if it doesn’t exist
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

            received_budget_ids.add(budget.id)

            # Remove budgets not in received data (handle deleted budgets)
            ProposalBudget.objects.filter(proposal=proposal).exclude(id__in=received_budget_ids).delete()

            updated_items = ProposalSectionItem.objects.filter(proposal=proposal)
            updated_budget = ProposalBudget.objects.filter(proposal=proposal)

        return proposal, updated_items, updated_budget


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
        created_budgets.append(budget)
    return created_budgets
