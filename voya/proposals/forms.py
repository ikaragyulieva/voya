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

from django import forms
from django.utils.translation import gettext_lazy as _
from voya.proposals.choices import StatusChoices, LogoChoices
from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.requests import choices
from voya.services.models import Location


class CreateProposalForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=StatusChoices,
        label="",
        # widget=forms.Select(attrs={'placeholder': 'Draft'}),
    )

    class Meta:
        model = Proposal
        fields = [
            'title',
            'status',
            'internal_comments'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Add Proposal Title')}),
        }

    def __init__(self, *args, **kwargs):
        trip_request = kwargs.pop("trip_request", None)
        super().__init__(*args, **kwargs)

        if trip_request:
            self.fields['title'].initial = trip_request.slug


class CreateItemForm(forms.ModelForm):
    corresponding_trip_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class': 'flatpickr',
                'placeholder': _('Select Date'),
            }
        )
    )

    city = forms.ModelChoiceField(
        queryset=Location.objects.all().order_by("city_name"),
        empty_label=_("Select city"),
        widget=forms.Select(
            attrs={
                'id': 'city-dropdown',
            }
        ),
    )

    additional_notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'description-field'
            }
        )
    )

    item_totals = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'readonly': 'readonly',
                'placeholder': '€ 0.00',
            }
        )
    )

    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': '0',
            }
        )
    )

    class Meta:
        model = ProposalSectionItem
        fields = [
            'corresponding_trip_date',
            'quantity',
            'city',
            'price',
            'additional_notes',
        ]


class CreateBudgetForm(forms.ModelForm):

    class Meta:
        model = ProposalBudget
        fields = [
            'variable_cost',
            'fixed_cost',
            'free_of_charge',
            'free_of_charge_amount',
            'total_cost_per_person',
            'total_cost',
            'pax',
            'fina_price_per_person',
            'final_price',
            'service_fee',
            'margin',
        ]


class PDFOptionsForm(forms.Form):
    logo_options = forms.ChoiceField(
        choices=LogoChoices,
        label="",
        # widget=forms.Select(attrs={'placeholder': 'Draft'}),
        initial='Dromo'
    )

    commission = forms.DecimalField(
        max_digits=10,
        label="",
        decimal_places=2,
        initial=0,
        # help_text='Commission should be added as percentage'
    )
