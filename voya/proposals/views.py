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
from datetime import timedelta, datetime
from itertools import chain
from operator import attrgetter

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
from django.utils.translation import gettext_lazy as _
from django.utils.formats import date_format
from django.utils.text import capfirst
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
from voya.proposals.choices import StatusChoices, MealChoices
from voya.proposals.forms import CreateProposalForm, CreateItemForm, CreateBudgetForm, PDFOptionsForm
from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.proposals.serializers import ProposalSerializer, ItemSerializer, BudgetSerializer
from voya.proposals.utils import save_proposal, update_proposal, get_section_context, REVERSE_SECTION_KEYS, \
    SECTION_MODEL_MAP, SECTION_KEYS, group_items_by_section
from voya.requests.choices import CityChoices
from voya.requests.models import TripRequests
from voya.services.models import Location
from voya.utils import get_user_obj, get_dashboard_multiple_search

logger = logging.getLogger(__name__)


class CreateProposalView(mixins.LoginRequiredMixin, TemplateView):
    template_name = "proposals/create-proposal-page.html"

    proposal_form_class = CreateProposalForm
    create_item_form_class = CreateItemForm
    create_budget_form_class = CreateBudgetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_id = self.kwargs.get('trip_id')
        current_request = get_object_or_404(TripRequests, pk=trip_id)

        proposal = self.proposal_form_class(trip_request=current_request)
        item_form = self.create_item_form_class()
        budget_form = self.create_budget_form_class()
        context['trip_id'] = trip_id
        context['profile'] = get_user_obj(self.request)
        context['current_request'] = current_request
        context['proposal'] = proposal
        context['item_form'] = item_form
        context['budget_form'] = budget_form
        context['meal_options'] = MealChoices

        context.update(get_section_context())

        return context


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


@login_required
def proposal_detail(request, pk):
    proposal = get_object_or_404(Proposal, id=pk)
    items = ProposalSectionItem.objects.filter(proposal=proposal).order_by('order')
    section_items_map = group_items_by_section(items)

    budget = ProposalBudget.objects.filter(proposal=proposal).order_by("pax")
    foc_pax = [budget_option.free_of_charge for budget_option in budget]

    user_profile = get_user_obj(request)
    current_request = TripRequests.objects.get(id=proposal.trip_request.id)

    if user_profile.user.role == 'employee':
        context = {
            'proposal': proposal,
            'profile': user_profile,
            'items': items,
            'accommodation_items': section_items_map['Accommodations'],
            'public_transport_items': section_items_map["Public Transport"],
            'private_transport_items': section_items_map["Private Transport"],
            'activity_items': section_items_map["Activity"] + section_items_map["Extra Activities"],
            'guides_items': section_items_map["Local Guides"],
            'tour_leader_items': section_items_map["Tour Leader"],
            'transfer_items': section_items_map["Transfers"],
            'other_variable_items': section_items_map["Other Services - Variable"] + section_items_map["Other Services"],
            'other_fixed_items': section_items_map["Other Services - Fixed"],
            'meal_items': section_items_map["Meals"],
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
            'accommodation_items': section_items_map['Accommodations'],
            'public_transport_items': section_items_map["Public Transport"],
            'private_transport_items': section_items_map["Private Transport"],
            'activity_items': section_items_map["Activity"] + section_items_map["Extra Activities"],
            'guides_items': section_items_map["Local Guides"],
            'tour_leader_items': section_items_map["Tour Leader"],
            'transfer_items': section_items_map["Transfers"],
            'other_variable_items': section_items_map["Other Services - Variable"] + section_items_map["Other Services"],
            'other_fixed_items': section_items_map["Other Services - Fixed"],
            'meal_items': section_items_map["Meals"],
            'budget': budget,
            'current_request': current_request
        }
        return render(request, 'proposals/client-proposal-details-page.html', context)
    else:

        return render(request, 'common/home-page.html')


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


@login_required
def proposal_pdf_view(request, pk):
    # Get user's profile
    user_profile = get_user_obj(request)

    if request.method == 'POST':
        form = PDFOptionsForm(request.POST)

        # Get Proposal data
        proposal = get_object_or_404(Proposal, id=pk)
        trip_start_date = TripRequests.objects.get(request_proposal=proposal).trip_start_date

        # Get proposal's items
        items = ProposalSectionItem.objects.filter(proposal=proposal).order_by("order")
        model_map = {
            'Accommodations': 'Hotel',
            'Public Transport': 'PublicTransport',
            'Private Transport': 'PrivateTransport',
            'Transfers': 'Transfer',
            'Extra Activities': 'Ticket',
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
        meal_items = []

        for item in items:
            if item.section_name == 'Other Services - Fixed' or item.section_name == 'Other Services - Variable' or item.section_name == 'Other Services' or item.section_name == 'Meals':
                pass
            else:
                model_name = model_map.get(item.section_name)

                service_object = apps.get_model('services', model_name=model_name).objects.get(id=item.service_id)
                if hasattr(service_object, 'name'):
                    item.service_name = service_object.name
                elif hasattr(service_object, 'type'):
                    item.service_name = service_object.type
                elif hasattr(service_object, 'object.get_type_display'):
                    item.service_name = service_object.get_type_display()

                if hasattr(service_object, 'category'):
                    item.category = service_object.get_category_display()

                if hasattr(service_object, 'label'):
                    item.label = service_object.label

            if item.section_name == 'Accommodations':
                accommodation_items.append(item)
            elif item.section_name == 'Public Transport':
                public_transport_items.append(item)
            elif item.section_name == 'Private Transport':
                private_transport_items.append(item)
            elif item.section_name == 'Extra Activities':
                activity_items.append(item)
            elif item.section_name == 'Activity':
                activity_items.append(item)
            elif item.section_name == 'Local Guides':
                guides_items.append(item)
            elif item.section_name == 'Transfers':
                transfer_items.append(item)
            elif item.section_name == 'Tour Leader':
                tour_leader_items.append(item)
            elif (item.section_name == 'Other Services - Variable'
                  or item.section_name == 'Other Services'):
                other_items.append(item)
            elif item.section_name == 'Other Services - Fixed':
                other_items.append(item)
            elif item.section_name == 'Meals':
                meal_items.append(item)

        # Get proposal's budget
        budget = ProposalBudget.objects.filter(proposal=proposal).order_by('pax')
        foc_pax = [budget_option.free_of_charge for budget_option in budget][0]
        foc_amount = [budget_option.free_of_charge_amount for budget_option in budget][0]

        if foc_pax > 0:
            item = {
                'proposal': proposal,
                'section_name': _('Other Services - Variable'),
                'quantity': foc_pax,
                'additional_notes': _('Gratuidad'),
                'corresponding_trip_date': trip_start_date,
                'city': '-',
                'price': foc_amount,

            }
            other_items.append(item)

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
            elif logo_option == 'Dromo':
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
            previous_paxs = []

            # Calculate final price if a commission is added

            for budget_option in budget:
                if budget_option.pax in previous_paxs:
                    continue

                if commission > 0.00:
                    budget_final_price = budget_option.final_price * Decimal(1 + (commission / 100))
                    budget_final_price_per_person = budget_option.fina_price_per_person * Decimal(
                        1 + (commission / 100))
                else:
                    budget_final_price = budget_option.final_price
                    budget_final_price_per_person = budget_option.fina_price_per_person

                deposit = budget_final_price * Decimal(0.30)
                final_payment = budget_final_price * Decimal(0.40)

                proposal_budget.append({
                    'id': budget_option.id,
                    'pax': budget_option.pax,
                    'final_price': budget_final_price,
                    'final_price_per_person': budget_final_price_per_person,
                    'deposit': deposit,
                    'final_payment': final_payment,
                })

                previous_paxs.append(budget_option.pax)

            current_date = timezone.now()
            deposit_due_date = current_date + timedelta(days=7)
            second_due_date = trip_start_date - timedelta(days=90)
            final_due_date = trip_start_date - timedelta(days=31)

            payment_terms = {
                'deposit_due_date': deposit_due_date,
                'second_due_date': second_due_date,
                'final_due_date': final_due_date,

            }

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
                'meal_items': meal_items,
                'budget': budget,
                'current_date': current_date,
                'payment_terms': payment_terms,
                'company_name': company_name,
                'company_address': company_address,
                'company_address_2': company_address_2,
                'company_email': company_email,
            })

            file_name = f"DromoProposal-{proposal.trip_request.slug}-{current_date:%Y-%m-%d}.pdf"

            # 3. Convert the HTML to PDF
            pdf_file = HTML(string=html_string).write_pdf()

            # 4. Return as a download
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
            # return HttpResponse(html_string)
    else:
        form = PDFOptionsForm()

    return render(request, 'proposals/pdf-proposal-form.html', {'form': form, 'profile': user_profile})


class ProposalDashboardView(mixins.LoginRequiredMixin, ListView):
    model = Proposal
    template_name = 'proposals/proposal-dashboard.html'
    paginate_by = 10

    def get_queryset(self):
        return Proposal.objects.all().order_by('-is_active', '-created_at')

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
        items = ProposalSectionItem.objects.filter(proposal=proposal).order_by("order")
        section_items_map = group_items_by_section(items)

        budget = ProposalBudget.objects.filter(proposal=proposal).order_by("pax")
        budget_id_min, budget_id_max = [b.id for b in budget]
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
        context['accommodation_items'] = section_items_map['Accommodations']
        context['public_transport_items'] = section_items_map["Public Transport"]
        context['private_transport_items'] = section_items_map["Private Transport"]
        context['activity_items'] = section_items_map["Activity"] + section_items_map["Extra Activities"]
        context['guides_items'] = section_items_map["Local Guides"]
        context['tour_leader_items'] = section_items_map["Tour Leader"]
        context['transfer_items'] = section_items_map["Transfers"]
        context['other_variable_items'] = section_items_map["Other Services - Variable"] + section_items_map["Other Services"]
        context['other_fixed_items'] = section_items_map["Other Services - Fixed"]
        context['meal_items'] = section_items_map["Meals"]
        context['budget'] = budget
        context['current_request'] = current_request
        context['foc_pax'] = foc_pax[0] if foc_pax else 0
        context['city_choices'] = Location.objects.all().order_by("city_name")
        context['status_choices'] = StatusChoices.choices
        context['meal_options'] = MealChoices
        context['budget_id_min'] = budget_id_min
        context['budget_id_max'] = budget_id_max

        context.update(get_section_context())

        return context


class HistoryLogView(ListView):
    template_name = "proposals/history-log.html"
    context_object_name = "history_entries"

    # paginate_by = 50

    def get_queryset(self):
        proposal_id = self.kwargs.get("pk")
        proposal = get_object_or_404(Proposal, pk=proposal_id)

        proposal_history = Proposal.history.filter(id=proposal_id)
        items_history = ProposalSectionItem.history.filter(proposal=proposal)
        budget_history = ProposalBudget.history.filter(proposal=proposal)

        model_map = {
            'Accommodations': 'Hotel',
            'Public Transport': 'PublicTransport',
            'Private Transport': 'PrivateTransport',
            'Transfers': 'Transfer',
            'Extra Activities': 'Ticket',
            'Activity': 'Ticket',
            'Local Guides': 'LocalGuide',
            'Tour Leader': 'Staff',
        }

        combined_history = list(chain(
            proposal_history,
            items_history,
            budget_history,
        ))

        combined_history.sort(key=attrgetter("history_date"), reverse=True)

        enriched_history = []

        for entry in combined_history:
            prev_record = entry.prev_record
            changes = []

            if prev_record and type(prev_record) is type(entry):
                delta = entry.diff_against(prev_record)
                print(f"[DEBUG] Entry ID: {entry.id} | Changes: {delta.changes}")
                for change in delta.changes:
                    if str(change.old).strip() != str(change.new).strip():
                        changes.append({
                            "field": change.field,
                            "old": change.old,
                            "new": change.new,
                        })

            service_name = None
            model_name = entry._meta.model_name
            # Try ro resolve service name if it is Proposal Section Item
            if model_name == "Proposal Section Item":
                section = getattr(entry, "section_name", "")
                service_id = getattr(entry, "service_id", None)

                model_key = model_map.get(section)
                if service_id and model_key:
                    try:
                        model_class = apps.get_model("services", model_key)
                        service_obj = model_class.objects.filter(id=service_id).first()
                        if service_obj:
                            service_name = service_obj.name

                    except LookupError:
                        service_name = "Unknown model"

            enriched_history.append({
                "entry": entry,
                "changes": changes,
                "model_name": entry.instance._meta.verbose_name.title(),
                "service_name": service_name,
                "timestamp": entry.history_date.astimezone(timezone.get_current_timezone()),  # Localized datetime
            })

        return enriched_history

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_user_obj(self.request)
        context["proposal"] = get_object_or_404(Proposal, pk=self.kwargs.get("pk"))
        return context
