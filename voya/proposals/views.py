import json
import logging

from django.apps import apps
from django.contrib.auth import mixins
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from voya.proposals.forms import CreateProposalForm, CreateItemForm, CreateBudgetForm
from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.proposals.serializers import ProposalSerializer, ItemSerializer, BudgetSerializer
from voya.requests.models import TripRequests
from voya.utils import get_user_obj


# Create your views here.

# @extend_schema(
#     summary="Create Proposal Endpoint",
#     description="Create a new proposal",
#     request=ProposalSerializer,
#     responses={
#         201: ProposalSerializer,
#         400: "Invalid request data",
#     }
# )
class CreateProposalView(mixins.LoginRequiredMixin, TemplateView):
    template_name = "proposals/create-proposal-page.html"

    proposal_form_class = CreateProposalForm
    create_item_form_class = CreateItemForm
    create_budget_form_class = CreateBudgetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_id = self.kwargs.get('trip_id')
        current_request = get_object_or_404(TripRequests, pk=trip_id)

        proposal = self.proposal_form_class()
        item_form = self.create_item_form_class()
        budget_form = self.create_budget_form_class
        context['trip_id'] = trip_id
        context['profile'] = get_user_obj(self.request)
        context['current_request'] = current_request
        context['proposal'] = proposal
        context['item_form'] = item_form
        context['budget_form'] = budget_form

        return context


class ProposalItemsAPI(APIView):
    """
    Unified API endpoint to handle proposals, items, and budget.
    """

    def post(self, request, *args, **kwargs):

        data = request.data

        # Validate Proposal
        proposal_serializer = ProposalSerializer(data=data.get('proposal'))
        if not proposal_serializer.is_valid():
            return Response({
                'error': 'Proposal validation failed',
                'details': proposal_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

        # Validate Items
        items_serializer = ItemSerializer(data=data.get('items', []), many=True)
        if not items_serializer.is_valid():
            return Response({
                'error': 'Item validation failed',
                'details': items_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

        budget_serializer = BudgetSerializer(data=data.get('budget', []), many=True)
        if not budget_serializer.is_valid():
            return Response({
                'error': 'Budget validation failed',
                'details': budget_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

        # Extract proposal, items, and budget data
        proposal_data = data.get('proposal', {})
        items_data = data.get('items', [])
        budget_data = data.get('budget', [])
        trip_id = data.get('trip_id', '')
        trip = TripRequests.objects.get(id=trip_id)

        try:
            with transaction.atomic():

                # 1. Save the proposal
                proposal = Proposal.objects.create(
                    trip_request=trip,
                    user=request.user,
                    title=proposal_data.get('title'),
                    is_draft=proposal_data.get('is_draft', True)
                )

                # 2. Saves the item
                created_items = []
                for item_data in items_data:
                    # Fetch linked services

                    # Create the item
                    new_item = ProposalSectionItem.objects.create(
                        proposal=proposal,
                        section_name=item_data.get('section_name'),
                        service_id=item_data.get('service_id'),
                        quantity=item_data.get('quantity'),
                        additional_notes=item_data.get('additional_notes', ''),
                        corresponding_trip_date=item_data.get('corresponding_trip_date'),
                        price=item_data.get('price'),
                        city=item_data.get('city'),
                    )
                    created_items.append(new_item)

                # 3. Save the budget
                created_budgets = []
                for budget_entry in budget_data:
                    budget = ProposalBudget.objects.create(
                        proposal=proposal,
                        pax=budget_entry.get('pax'),
                        variable_cost=budget_entry.get('variable_cost'),
                        fixed_cost=budget_entry.get('fixed_cost'),
                        total_cost_per_person=budget_entry.get('total_cost_per_person'),
                        total_cost=budget_entry.get('total_cost'),
                        service_fee=budget_entry.get('service_fee'),
                        margin=budget_entry.get('margin'),
                        fina_price_per_person=budget_entry.get('fina_price_per_person'),
                        final_price=budget_entry.get('final_price'),
                    )
                    created_budgets.append(budget)

                # Return success response
                return Response({
                    'success': 'Proposal, items, and budget saved successfully!',
                    'proposal_id': proposal.id,
                    'item_ids': [item.id for item in created_items],
                    'budget_ids': [budget.id for budget in created_budgets],
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def proposal_detail(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    items = ProposalSectionItem.objects.filter(proposal=proposal)
    model_map = {
        'Accommodations': 'Hotels',
        'Public Transport': 'Public Transport',
        'Private Transport': 'Private Transport',
        'Transfers': 'Transfers',
        'Activity': 'Tickets',
        'Guides': 'LocalGuides',
        # 'Other Services': 'Other',
    }
    accommodation_items = []
    transport_items = []
    activity_items = []
    transfer_items = []
    guides_items = []
    other_items = []

    for item in items:
        model_name = model_map.get(item.section_name)

        service_object = apps.get_model('services', model_name=model_name).objects.get(id=item.service_id)
        if hasattr(service_object, 'name'):
            item.service_name = service_object.name
        elif hasattr(service_object, 'guide_name'):
            item.service_name = service_object.guide_name
        elif hasattr(service_object, 'type'):
            item.service_name = service_object.type

        if item.section_name == 'Accommodations':
            accommodation_items.append(item)
        elif item.section_name == 'Transport':
            transport_items.append(item)
        elif item.section_name == 'Activity':
            activity_items.append(item)
        elif item.section_name == 'Guides':
            guides_items.append(item)
        elif item.section_name == 'Transfers':
            transfer_items.append(item)
        elif item.section_name == 'Other Services':
            other_items.append(item)

    budget = ProposalBudget.objects.filter(proposal=proposal)
    user_profile = get_user_obj(request)
    current_request = TripRequests.objects.get(id=proposal.trip_request.id)
    context = {
        'proposal': proposal,
        'profile': user_profile,
        'items': items,
        'accommodation_items': accommodation_items,
        'transport_items': transport_items,
        'activity_items': activity_items,
        'guides_items': guides_items,
        'transfer_items': transfer_items,
        'other_items': other_items,
        'budget': budget,
        'current_request': current_request
    }
    return render(request, 'proposals/proposal-detail-page.html', context)

def client_proposal_detail(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    items = ProposalSectionItem.objects.filter(proposal=proposal)
    model_map = {
        'Accommodations': 'Hotels',
        'Public Transport': 'Public Transport',
        'Private Transport': 'Private Transport',
        'Transfers': 'Transfers',
        'Activity': 'Tickets',
        'Guides': 'LocalGuides',
        # 'Other Services': 'Other',
    }
    accommodation_items = []
    transport_items = []
    activity_items = []
    transfer_items = []
    guides_items = []
    other_items = []

    for item in items:
        model_name = model_map.get(item.section_name)

        service_object = apps.get_model('services', model_name=model_name).objects.get(id=item.service_id)
        if hasattr(service_object, 'name'):
            item.service_name = service_object.name
        elif hasattr(service_object, 'guide_name'):
            item.service_name = service_object.guide_name
        elif hasattr(service_object, 'type'):
            item.service_name = service_object.type

        if item.section_name == 'Accommodations':
            accommodation_items.append(item)
        elif item.section_name == 'Transport':
            transport_items.append(item)
        elif item.section_name == 'Activity':
            activity_items.append(item)
        elif item.section_name == 'Guides':
            guides_items.append(item)
        elif item.section_name == 'Transfers':
            transfer_items.append(item)
        elif item.section_name == 'Other Services':
            other_items.append(item)

    budget = ProposalBudget.objects.filter(proposal=proposal)
    user_profile = get_user_obj(request)
    current_request = TripRequests.objects.get(id=proposal.trip_request.id)
    context = {
        'proposal': proposal,
        'profile': user_profile,
        'items': items,
        'accommodation_items': accommodation_items,
        'transport_items': transport_items,
        'activity_items': activity_items,
        'guides_items': guides_items,
        'transfer_items': transfer_items,
        'other_items': other_items,
        'budget': budget,
        'current_request': current_request
    }
    return render(request, 'proposals/client-proposal-details-page.html', context)

class DynamicServiceView(APIView):
    model_map = {
        'Accommodations': 'Hotels',
        'Public Transport': 'Public Transport',
        'Private Transport': 'Private Transport',
        'Transfers': 'Transfers',
        'Activity': 'Tickets',
        'Guides': 'LocalGuides',
        # 'Other Services': 'Other',
    }

    def get(self, request, section, *args, **kwargs):
        model_name = self.model_map.get(section)
        if not model_name:
            return Response(
                {'error': f"Invalid section '{section}'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            model = apps.get_model(app_label='services', model_name=model_name)
            queryset = model.objects.filter(is_active=True)

            # Determine the field to use for display (e.g., `name`, `guide_name`)
            if hasattr(model, 'name'):
                display_field = 'name'
            elif hasattr(model, 'guide_name'):
                display_field = 'guide_name'
            elif hasattr(model, 'type'):
                display_field = 'type'
            else:
                return Response(
                    {'error': f'Could not determine display field for {model_name}.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if hasattr(model, 'price'):
                price = 'price'
            elif hasattr(model, 'high_season_price'):
                price = 'high_season_price'
            else:
                return Response(
                    {'error': f'Could not determine price field for {model_name}.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = [
                {
                    'id': obj.id,
                    'display_field': getattr(obj, display_field),
                    'city': obj.city,
                    'price': getattr(obj, price),
                } for obj in queryset
            ]

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
