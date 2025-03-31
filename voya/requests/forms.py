from django import forms

from voya.companies.models import CompanyProfile
from voya.requests import choices
from voya.requests.models import TripRequests


class CreateRequestForm(forms.ModelForm):

    country_destinations = forms.MultipleChoiceField(
        choices=choices.CountryChoices,
        widget=forms.SelectMultiple(attrs={'class': 'multi-select', 'placeholder': 'Select Destinations'}),
        label="Country Destinations",
    )

    trip_start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'flatpickr'}))
    trip_end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'flatpickr'}))

    transportation_type = forms.MultipleChoiceField(
        choices=choices.TransportationType,
        widget=forms.SelectMultiple(attrs={
            'class': 'multi-select',
            'placeholder': 'Select an option'
        })
        )

    created_by_company = forms.ModelChoiceField(
        queryset=CompanyProfile.objects.filter(is_active=True),
        required=False,  # Optional, if it should only be set by employees
        label="Company",
        widget=forms.Select(attrs={'placeholder': 'Select Company'}),
        initial='Select Company',
    )

    currency = forms.ChoiceField(
        choices=[('', 'Select an option')] + list(choices.CurrencyChoices.choices),
        widget=forms.Select(),
    )

    accommodations = forms.ChoiceField(
        choices=[('', 'Select an option')] + list(choices.AccommodationsType.choices),
        widget=forms.Select(),
    )

    meals = forms.ChoiceField(
        choices=[('', 'Select an option')] + list(choices.MealsType.choices),
        widget=forms.Select(),
    )

    staff = forms.ChoiceField(
        choices=[('', 'Select an option')] + list(choices.StaffChoices.choices),
        widget=forms.Select(),
    )

    kind_of_group = forms.ChoiceField(
        choices=[('', 'Select an option')] + list(choices.GroupChoice.choices),
        widget=forms.Select(),
    )

    class Meta:
        model = TripRequests
        fields = [
            'country_origin',
            'nationality',
            'age_range',
            'min_participants',
            'max_participants',
            'country_destinations',
            'other_destinations',
            'budget',
            'currency',
            'trip_duration',
            'trip_start_date',
            'trip_end_date',
            'transportation_type',
            'transportation_details',
            'accommodations',
            'accommodations_details',
            'meals',
            'meals_details',
            'staff',
            'kind_of_group',
            'type_of_trip',
            'additional_observations',
            'created_by_company',
        ]
        widgets = {
            'age_range': forms.TextInput(attrs={'placeholder': 'Average travelers age'}),
            'other_destinations': forms.TextInput(attrs={'placeholder': 'Tell us more about the places you wish to visit.'}),
            'transportation_details': forms.TextInput(attrs={'placeholder': 'Share any transport details here.'}),
            'accommodations_details': forms.TextInput(attrs={'placeholder': 'Share any accommodations details here.'}),
            'meals_details': forms.TextInput(attrs={'placeholder': 'Any meals details we need to have into account?'}),
            'type_of_trip': forms.TextInput(attrs={'placeholder': 'E.g. family trip, company trip, religious trip'}),
            'additional_observations': forms.TextInput(attrs={'placeholder': 'Share any details you consider important here'}),

        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If the user is not an employee, remove the field from the form
        if not hasattr(self.user, 'employee_profile'):
            self.fields.pop('created_by_company')

    def clean_country_destinations(self):
        selected_countries = self.cleaned_data.get('country_destinations', [])
        return ', '.join(selected_countries)

    def clean_city_destinations(self):
        cities = self.cleaned_data.get('city_destinations', [])
        return ', '.join(cities)

    def save(self, commit=True):
        trip_request = super().save(commit=False)

        trip_request.created_by_user = self.user

        if hasattr(self.user, 'employee_profile'):
            trip_request.created_by_company = self.cleaned_data.get('created_by_company')
        else:
            trip_request.created_by_company = self.user.client_profile.company

        if commit:
            trip_request.save()

        return trip_request


