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
from datetime import timedelta

from django.apps import apps
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal
from weasyprint import HTML

from voya.proposals.forms import CreateProposalForm, CreateItemForm, CreateBudgetForm, PDFOptionsForm
from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.proposals.serializers import ProposalSerializer, ItemSerializer, BudgetSerializer
from voya.requests.models import TripRequests
from voya.utils import get_user_obj


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
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        data = request.data

        # Validate Proposal
        proposal_serializer = ProposalSerializer(data=data.get('proposal'))
        if not proposal_serializer.is_valid():
            return Response({
                'error': 'Proposal validation failed',
                'details': proposal_serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)

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
                        service_id=item_data.get('service_id', None),
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

                # Return success response
                return Response({
                    'success': 'Proposal, items, and budget saved successfully!',
                    'proposal_id': proposal.id,
                    'item_ids': [item.id for item in created_items],
                    'budget_ids': [budget.id for budget in created_budgets],
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def proposal_detail(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    items = ProposalSectionItem.objects.filter(proposal=proposal)
    model_map = {
        'Accommodations': 'Hotel',
        'Public Transport': 'PublicTransport',
        'Private Transport': 'PrivateTransport',
        'Transfers': 'Transfer',
        'Activity': 'Ticket',
        'Local Guides': 'LocalGuide',
        'Tour Leader': 'Staff',
        # 'Other Services': 'Other',
    }

    accommodation_items = []
    public_transport_items = []
    private_transport_items = []
    activity_items = []
    transfer_items = []
    guides_items = []
    tour_leader_items = []
    other_items = []

    for item in items:
        if item.section_name == 'Other Services':
            pass
        else:
            model_name = model_map.get(item.section_name)

            service_object = apps.get_model('services', model_name=model_name).objects.get(id=item.service_id)
            if hasattr(service_object, 'name'):
                item.service_name = service_object.name
            elif hasattr(service_object, 'type'):
                item.service_name = service_object.type

        if item.section_name == 'Accommodations':
            accommodation_items.append(item)
        elif item.section_name == 'Public Transport':
            public_transport_items.append(item)
        elif item.section_name == 'Private Transport':
            private_transport_items.append(item)
        elif item.section_name == 'Activity':
            activity_items.append(item)
        elif item.section_name == 'Local Guides':
            guides_items.append(item)
        elif item.section_name == 'Transfers':
            transfer_items.append(item)
        elif item.section_name == 'Tour Leader':
            tour_leader_items.append(item)
        elif item.section_name == 'Other Services':
            other_items.append(item)

    budget = ProposalBudget.objects.filter(proposal=proposal)
    foc_pax = [budget_option.free_of_charge for budget_option in budget]

    user_profile = get_user_obj(request)
    current_request = TripRequests.objects.get(id=proposal.trip_request.id)

    if user_profile.user.role == 'employee':
        context = {
            'proposal': proposal,
            'profile': user_profile,
            'items': items,
            'accommodation_items': accommodation_items,
            'public_transport_items': public_transport_items,
            'private_transport_items': private_transport_items,
            'activity_items': activity_items,
            'guides_items': guides_items,
            'tour_leader_items': tour_leader_items,
            'transfer_items': transfer_items,
            'other_items': other_items,
            'budget': budget,
            'current_request': current_request,
            'foc_pax': foc_pax[0],
        }
        return render(request, 'proposals/proposal-detail-page.html', context)

    elif user_profile.user.role == 'client':

        context = {
            'proposal': proposal,
            'profile': user_profile,
            'items': items,
            'accommodation_items': accommodation_items,
            'public_transport_items': public_transport_items,
            'private_transport_items': private_transport_items,
            'activity_items': activity_items,
            'guides_items': guides_items,
            'tour_leader_items': tour_leader_items,
            'transfer_items': transfer_items,
            'other_items': other_items,
            'budget': budget,
            'current_request': current_request
        }
        return render(request, 'proposals/client-proposal-details-page.html', context)
    else:

        return render(request, 'common/home-page.html')

# @login_required
# def client_proposal_detail(request, proposal_id):
#     proposal = get_object_or_404(Proposal, id=proposal_id)
#     items = ProposalSectionItem.objects.filter(proposal=proposal)
#     model_map = {
#         'Accommodations': 'Hotel',
#         'Public Transport': 'Public Transport',
#         'Private Transport': 'Private Transport',
#         'Transfers': 'Transfer',
#         'Activity': 'Ticket',
#         'Guides': 'LocalGuide',
#         # 'Other Services': 'Other',
#     }
#     accommodation_items = []
#     transport_items = []
#     activity_items = []
#     transfer_items = []
#     guides_items = []
#     other_items = []
#
#     for item in items:
#         model_name = model_map.get(item.section_name)
#
#         service_object = apps.get_model('services', model_name=model_name).objects.get(id=item.service_id)
#         if hasattr(service_object, 'name'):
#             item.service_name = service_object.name
#         elif hasattr(service_object, 'guide_name'):
#             item.service_name = service_object.guide_name
#         elif hasattr(service_object, 'type'):
#             item.service_name = service_object.type
#
#         if item.section_name == 'Accommodations':
#             accommodation_items.append(item)
#         elif item.section_name == 'Transport':
#             transport_items.append(item)
#         elif item.section_name == 'Activity':
#             activity_items.append(item)
#         elif item.section_name == 'Guides':
#             guides_items.append(item)
#         elif item.section_name == 'Transfers':
#             transfer_items.append(item)
#         elif item.section_name == 'Other Services':
#             other_items.append(item)
#
#     budget = ProposalBudget.objects.filter(proposal=proposal)
#     user_profile = get_user_obj(request)
#     current_request = TripRequests.objects.get(id=proposal.trip_request.id)
#     context = {
#         'proposal': proposal,
#         'profile': user_profile,
#         'items': items,
#         'accommodation_items': accommodation_items,
#         'transport_items': transport_items,
#         'activity_items': activity_items,
#         'guides_items': guides_items,
#         'transfer_items': transfer_items,
#         'other_items': other_items,
#         'budget': budget,
#         'current_request': current_request
#     }
#     return render(request, 'proposals/client-proposal-details-page.html', context)


class DynamicServiceView(APIView):
    model_map = {
        'Accommodations': 'Hotel',
        'Public Transport': 'PublicTransport',
        'Private Transport': 'PrivateTransport',
        'Transfers': 'Transfer',
        'Activity': 'Ticket',
        'Local Guides': 'LocalGuide',
        'Tour Leader': 'Staff'
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


@login_required
def proposal_pdf_view(request, proposal_id):
    # Get user's profile
    user_profile = get_user_obj(request)

    if request.method == 'POST':
        form = PDFOptionsForm(request.POST)

        # Get Proposal data
        proposal = get_object_or_404(Proposal, id=proposal_id)

        # Get proposal's items
        items = ProposalSectionItem.objects.filter(proposal=proposal)
        model_map = {
            'Accommodations': 'Hotel',
            'Public Transport': 'Public Transport',
            'Private Transport': 'Private Transport',
            'Transfers': 'Transfer',
            'Activity': 'Ticket',
            'Guides': 'LocalGuide',
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

        # Get proposal's budget
        budget = ProposalBudget.objects.filter(proposal=proposal)

        if form.is_valid():
            logo_option = form.cleaned_data['logo_options']
            commission = form.cleaned_data['commission']

            company_name = 'Dromo S.A.'
            company_address = 'Rue de Madame de Stael 5'
            company_address_2 = '1201, Genève, Suisse'
            company_email = 'info@dromo.travel'

            # Set logo
            if logo_option == 'None':
                logo = None
            elif logo_option == 'Voya logo':
                logo = 'https://dromo.travel/wp-content/uploads/128px_Logo_Dromo.png'
            elif logo_option == "My company's logo":
                logo = proposal.trip_request.created_by_company.logo.url
                company_name = proposal.trip_request.created_by_company.commercial_name
                company_address = proposal.trip_request.created_by_company.addresses.first().street_address
                company_address_2 = (f'{proposal.trip_request.created_by_company.addresses.first().postal_code}, '
                                     f'{proposal.trip_request.created_by_company.addresses.first().city}, '
                                     f'{proposal.trip_request.created_by_company.addresses.first().country}')
                company_email = proposal.trip_request.created_by_company.billing_email

            proposal_budget = []

            # Calculate final price if a commission is added

            for budget_option in budget:
                if commission > 0.00:
                    budget_final_price = budget_option.final_price * Decimal(1 + (commission / 100))
                    budget_final_price_per_person = budget_option.fina_price_per_person * Decimal(1 + (commission / 100))
                else:
                    budget_final_price = budget_option.final_price
                    budget_final_price_per_person = budget_option.fina_price_per_person

                pre_payment = budget_final_price * Decimal(0.20)

                proposal_budget.append({
                    'id': budget_option.id,
                    'pax': budget_option.pax,
                    'final_price': budget_final_price,
                    'final_price_per_person': budget_final_price_per_person,
                    'pre_payment': pre_payment,
                })

            current_date = timezone.now()
            due_date = current_date + timedelta(days=7)
            # Render template to HTML with the user's choices
            html_string = render_to_string('proposals/pdf-proposal.html', {
                'logo_option': logo_option,
                'logo': logo,
                'commission': commission,
                'proposal_budget': proposal_budget,
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
                'current_date': current_date,
                'due_date': due_date,
                'company_name': company_name,
                'company_address': company_address,
                'company_address_2': company_address_2,
                'company_email': company_email,
            })

            # 3. Convert the HTML to PDF
            pdf_file = HTML(string=html_string).write_pdf()

            # 4. Return as a download
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="proposal.pdf"'
            return response
            # return render(request, 'proposals/pdf-proposal.html', context={'logo_option': logo_option,
            #                                                                'logo': logo,
            #                                                                'commission': commission,
            #
            #                                                                'proposal_budget': proposal_budget,
            #                                                                'proposal': proposal,
            #                                                                'profile': user_profile,
            #                                                                'items': items,
            #                                                                'accommodation_items': accommodation_items,
            #                                                                'transport_items': transport_items,
            #                                                                'activity_items': activity_items,
            #                                                                'guides_items': guides_items,
            #                                                                'transfer_items': transfer_items,
            #                                                                'other_items': other_items,
            #                                                                'budget': budget,
            #                                                                'current_date': current_date,
            #                                                                'due_date': due_date,
            #                                                                'company_name': company_name,
            #                                                                'company_address': company_address,
            #                                                                'company_address_2': company_address_2,
            #                                                                'company_email': company_email,
            #                                                                },)

    else:
        form = PDFOptionsForm()

    return render(request, 'proposals/pdf-proposal-form.html', {'form': form, 'profile': user_profile})
