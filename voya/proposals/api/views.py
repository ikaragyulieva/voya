"""
Copyright (C) 2025 DROMO SA

This file is part of VOYA.

VOYA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VOYA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from datetime import datetime

from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from voya.proposals.models import Proposal
from voya.proposals.api.serializers import ProposalSerializer, ItemSerializer, BudgetSerializer, \
    ProposalCreateUpdateSerializer
from voya.proposals.utils import save_proposal, update_proposal, REVERSE_SECTION_KEYS, \
    SECTION_MODEL_MAP, group_items_by_section, proposal_validations
from voya.requests.models import TripRequests

logger = logging.getLogger(__name__)


class ProposalItemsAPI(APIView):
    """
    Unified API endpoint to handle proposals, items, and budget.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Handles creating a new proposal."""
        data = request.data
        items = data.get('items', [])

        for item in items:
            label = item.get("section_name")
            item["section_name"] = REVERSE_SECTION_KEYS.get(label)

        # Validate Proposal
        proposal_serializer = ProposalSerializer(data=data.get('proposal'))
        if not proposal_serializer.is_valid():
            return Response({
                'error': _('Proposal validation failed'),
                'details': proposal_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate Items
        items_serializer = ItemSerializer(data=items, many=True)
        if not items_serializer.is_valid():
            return Response({
                'error': _('Item validation failed'),
                'details': items_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

        budget_serializer = BudgetSerializer(data=data.get('budget', []), many=True)
        if not budget_serializer.is_valid():
            return Response({
                'error': _('Budget validation failed'),
                'details': budget_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            proposal, created_items, created_budgets = save_proposal(data, request.user)

            # Return success response
            return JsonResponse({
                'success': _('Proposal, items, and budget saved successfully!'),
                'proposal_id': proposal.id,
                'item_ids': [item.id for item in created_items],
                'budget_ids': [budget.id for budget in created_budgets],
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProposalUpdateAPI(APIView):
    """
       API to handle updating an existing proposal, items, and budget.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        logger.warning("PUT request received")
        """Handles updating an existing proposal."""
        data = request.data
        items = data.get('items', [])
        trip_id = data.get('trip_id', '')

        for item in items:
            label = item.get('section_name')
            item["section_name"] = REVERSE_SECTION_KEYS.get(label)

        data['items'] = items

        try:
            proposal = Proposal.objects.get(pk=pk)
        except Proposal.DoesNotExist:
            return Response({'error': _('Proposal not found. Use Post to create a new one')},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            updated_proposal, created_items, created_budgets = update_proposal(proposal, data, request.user)
            return JsonResponse({
                'success': _('Proposal updated successfully!'),
                'proposal_id': updated_proposal.id,
                'item_ids': [item.id for item in created_items],
                'budget_ids': [budget.id for budget in created_budgets],
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DynamicServiceView(APIView):
    # model_map = {
    #     'Accommodations': 'Hotel',
    #     'Public Transport': 'PublicTransport',
    #     'Private Transport': 'PrivateTransport',
    #     'Transfers': 'Transfer',
    #     'Extra Activities': 'Ticket',
    #     'Activity': 'Ticket',
    #     'Local Guides': 'LocalGuide',
    #     'Tour Leader': 'Staff'
    #     # 'Other Services': 'Other',
    # }

    def get(self, request, section, city_id=None, *args, **kwargs):
        section_key = REVERSE_SECTION_KEYS.get(section)
        model_name = SECTION_MODEL_MAP.get(section_key)
        if not model_name or not section_key:
            return Response(
                {'error': _("Invalid section '%(section)s'") % {'section': section}},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            model = apps.get_model(app_label='services', model_name=model_name)
            queryset = model.objects.filter(is_active=True)

            # Determine the field to use for display (e.g., `name`, `guide_name`)
            if hasattr(model, 'name'):
                display_field = 'name'
            elif hasattr(model, 'type'):
                display_field = 'type'
            else:
                return Response(
                    {'error': _('Could not determine display field for %(model_name)s.') % {'model_name': model_name}},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if hasattr(model, 'price'):
                price = 'price'
            elif hasattr(model, 'high_season_price'):
                price = 'high_season_price'
            else:
                return Response(
                    {'error': _('Could not determine price field for %(model_name)s.') % {'model_name': model_name}},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = [
                {
                    'id': obj.id,
                    'display_field': getattr(obj, display_field),
                    'city': obj.city.city_name,
                    'city_id': obj.city.id,
                    'price': getattr(obj, price),
                } for obj in queryset
            ]

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SaveAndValidateProposalAPI(APIView):
    """
        API to handle the sase and validation of a proposal, items, and budget based on criteria.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        mode = data.get('data-mode')
        user = request.user
        proposal_data = data.get("proposal", {})
        proposal_id = proposal_data.get("id")

        # Handle creation or update of the proposal
        try:
            if mode == 'create' or not proposal_id:
                proposal, items, budget = save_proposal(data, user)
            elif mode == 'edit' and proposal_id:
                proposal = get_object_or_404(Proposal, pk=proposal_id)
                proposal, items, budget = update_proposal(proposal, data, user)
            else:
                return Response({"error": "Invalid mode."}, status=400)

            # Perform validations on the saved/updated proposal
            validation_summary = proposal_validations(proposal)

            return Response({
                "success": "Proposal saved and validated successfully.",
                "proposal_id": proposal.id,
                "item_ids": [i.id for i in items],
                "budget_ids": [b.id for b in budget],
                "validation_summary": validation_summary,
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        List all proposals.
        """
        if self.action in ["create", "update", "partial_update", ]:
            return ProposalCreateUpdateSerializer

        return ProposalSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new proposal along with items and budget
        """
        user = request.user
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            # proposal, items, budget = save_proposal(serializer.validated_data, user)
            proposal = serializer.save()
            return Response({
                'success': 'Proposal created successfully!',
                'proposal_id': proposal.id,
                # 'item_ids': [item.id for item in items],
                # 'budget_ids': [b.id for b in budget],
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
           Update an existing proposal, items, and budget
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = request.user

        try:
            # proposal, items, budget = update_proposal(instance, serializer.validated_data, user)
            proposal = serializer.save()
            return Response({
                'success': 'Proposal updated successfully.',
                'proposal_id': proposal.id,
                # 'item_ids': [item.id for item in items],
                # 'budget_ids': [b.id for b in budget],
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        """
            Run validations against a proposal
        """
        proposal = get_object_or_404(Proposal, pk=pk)

        try:
            results = proposal_validations(proposal)
            return Response({
                'success': 'Validation completed!',
                'validation_summary': results,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
