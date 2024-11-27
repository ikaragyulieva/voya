from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from voya.proposals.forms import CreateProposalForm, CreateItemForm
from voya.proposals.models import Proposal, ProposalSectionItem
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
class CreateProposalView(CreateView):
    model = Proposal
    template_name = "proposals/create-proposal-page.html"
    form_class = CreateProposalForm
    context_object_name = 'proposal'

    create_item_form_class = CreateItemForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_id = self.kwargs.get('trip_id')
        current_request = get_object_or_404(TripRequests, pk=trip_id)

        item_form = self.create_item_form_class()
        context['profile'] = get_user_obj(self.request)
        context['current_request'] = current_request
        context['item_form'] = item_form

        return context


class DynamicServiceView(APIView):
    model_map = {
        'Accommodations': 'Hotels',
        'Public Transport': 'Public Transport',
        'Private Transport': 'Private Transport',
        'Transfers': 'Transfers',
        'Activity': 'Tickets',
        'Guides': 'LocalGuides',
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

