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
from voya.proposals.choices import StatusChoices
from voya.proposals.models import Proposal, ProposalSectionItem, ProposalBudget
from voya.requests import choices


class CreateProposalForm(forms.ModelForm):
    is_draft = forms.ChoiceField(
        choices=StatusChoices,
        label="",
        widget=forms.Select(attrs={'placeholder': 'Draft'}),
    )

    class Meta:
        model = Proposal
        fields = [
            'title',
            'is_draft',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Add Proposal Title'}),
        }


class CreateItemForm(forms.ModelForm):
    corresponding_trip_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class': 'flatpickr',
                'placeholder': 'Select Date',
            }
        )
    )

    city = forms.ChoiceField(
        choices=choices.CityChoices,
        label="City",
        widget=forms.Select(
            attrs={
                'placeholder': 'Select City',
                'id': 'city-dropdown',
            }
        ),
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

    # def __int__(self, *args, section=None, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     section_model_map = {
    #         'Accommodations': 'Hotels',
    #         'Public Transport': 'Public Transport',
    #         'Private Transport': 'Private Transport',
    #         'Transfers': 'Transfers',
    #         'Activity': 'Tickets',
    #         'Guides': 'LocalGuides',
    #     }
    #
    #     if section and section in section_model_map:
    #         self.fields['service'].queryset = section_model_map[section].objects.filter(is_active=True)
    #     else:
    #         self.fields['service'].queryset = None


class CreateBudgetForm(forms.ModelForm):

    class Meta:
        model = ProposalBudget
        fields = [
            'variable_cost',
            'fixed_cost',
            'total_cost_per_person',
            'total_cost',
            'pax',
            'fina_price_per_person',
            'final_price',
            'service_fee',
            'margin',
        ]
