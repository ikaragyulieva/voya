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
from attr.filters import exclude
from django import forms

from voya.providers import choices
from voya.providers.models import Providers


class ProviderCreateForm(forms.ModelForm):
    services = forms.MultipleChoiceField(
        choices=choices.ServiceChoices,
        widget=forms.SelectMultiple(attrs={'class': 'multi-select', 'placeholder': 'Select an option'}),
        label="Select an option",
    )

    city = forms.Select()

    class Meta:
        model = Providers
        fields = [
            'commercial_name',
            'services',
            'country',
            'city',
            'telephone_number',
            'email',
            'website',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        provider = super().save(commit=False)

        provider.created_by_user = self.user

        if commit:
            provider.save()

        return provider
