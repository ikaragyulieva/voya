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
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal
from weasyprint import HTML

from voya.common.forms import SearchForm
from voya.employees.models import EmployeeProfile
from voya.proposals.choices import StatusChoices
from voya.proposals.forms import CreateProposalForm, CreateItemForm, CreateBudgetForm, PDFOptionsForm
from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.proposals.serializers import ProposalSerializer, ItemSerializer, BudgetSerializer
from voya.proposals.utils import save_proposal, update_proposal
from voya.requests.choices import CityChoices
from voya.requests.models import TripRequests
from voya.services.models import Location
from voya.utils import get_user_obj, get_dashboard_multiple_search


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
        budget_form = self.create_budget_form_class()
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
        """Handles creating a new proposal."""
        data = request.data

        # Validate Proposal
        proposal_serializer = ProposalSerializer(data=data.get('proposal'))
        if not proposal_serializer.is_valid():
            return Response({
                'error': 'Proposal validation failed',
                'details': proposal_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

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

        try:
            proposal, created_items, created_budgets = save_proposal(data, request.user)

            # Return success response
            return JsonResponse({
                'success': 'Proposal, items, and budget saved successfully!',
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

    def put(self, request, *args, **kwargs):
        """Handles updating an existing proposal."""
        data = request.data
        trip_id = data.get('trip_id', '')

        try:
            proposal = Proposal.objects.get(trip_request_id=trip_id, user=request.user)
        except Proposal.DoesNotExist:
            return Response({'error': 'Proposal not found. Use Post to create a new one'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            proposal, created_items, created_budgets = update_proposal(proposal, data)
            return JsonResponse({
                'success': 'Proposal updated successfully!',
                'proposal_id': proposal.id,
                'item_ids': [item.id for item in created_items],
                'budget_ids': [budget.id for budget in created_budgets],
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
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
            'foc_pax': foc_pax[0] if foc_pax else 0,
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


@login_required
def proposal_pdf_view(request, pk):
    # Get user's profile
    user_profile = get_user_obj(request)

    if request.method == 'POST':
        form = PDFOptionsForm(request.POST)

        # Get Proposal data
        proposal = get_object_or_404(Proposal, id=pk)

        # Get proposal's items
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

        # Get proposal's budget
        budget = ProposalBudget.objects.filter(proposal=proposal)
        foc_pax = [budget_option.free_of_charge for budget_option in budget]


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
                    budget_final_price_per_person = budget_option.fina_price_per_person * Decimal(
                        1 + (commission / 100))
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
                'public_transport_items': public_transport_items,
                'private_transport_items': private_transport_items,
                'activity_items': activity_items,
                'guides_items': guides_items,
                'transfer_items': transfer_items,
                'tour_leader_items': tour_leader_items,
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
    else:
        form = PDFOptionsForm()

    return render(request, 'proposals/pdf-proposal-form.html', {'form': form, 'profile': user_profile})


class ProposalDashboardView(mixins.LoginRequiredMixin, ListView):
    model = Proposal
    template_name = 'proposals/proposal-dashboard.html'
    paginate_by = 10

    def get_queryset(self):
        return Proposal.objects.all().order_by('-is_draft', '-created_at')

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return EmployeeProfile.objects.get(user=self.request.user)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        all_proposals_query = self.get_queryset()
        proposals_list = get_dashboard_multiple_search(self.request, all_proposals_query)

        context['profile'] = self.get_object()
        context["search_form"] = SearchForm(self.request.GET)
        context['all_proposals'] = all_proposals_query
        context['proposals_list'] = proposals_list

        return context


class EditProposalView(mixins.LoginRequiredMixin, UpdateView):
    model = Proposal
    template_name = 'proposals/edit-proposal-page.html'
    success_url = reverse_lazy('proposal-dashboard')

    form_class = CreateProposalForm
    create_item_form_class = CreateItemForm
    create_budget_form_class = CreateBudgetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        proposal = self.get_object()
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
        current_request = TripRequests.objects.get(id=proposal.trip_request.id)

        current_proposal = self.get_object()
        trip_id = current_proposal.trip_request.id
        proposal_form = self.form_class
        item_form = self.create_item_form_class()
        budget_form = self.create_budget_form_class()

        context['trip_id'] = trip_id
        context['item_form'] = item_form
        context['budget_form'] = budget_form
        context['profile'] = get_user_obj(self.request)
        context['current_request'] = current_request
        context['proposal'] = proposal
        context['items'] = items
        context['accommodation_items'] = accommodation_items
        context['public_transport_items'] = public_transport_items
        context['private_transport_items'] = private_transport_items
        context['activity_items'] = activity_items
        context['guides_items'] = guides_items
        context['tour_leader_items'] = tour_leader_items
        context['transfer_items'] = transfer_items
        context['other_items'] = other_items
        context['budget'] = budget
        context['current_request'] = current_request
        context['foc_pax'] = foc_pax[0] if foc_pax else 0
        context['city_choices'] = Location.objects.all()
        context['status_choices'] = StatusChoices.choices

        return context
