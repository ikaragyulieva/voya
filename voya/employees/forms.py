from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from voya.clients.choices import TitleChoices
from voya.clients.models import ClientProfile
from voya.companies.models import CompanyProfile
from voya.employees.models import EmployeeProfile

UserModel = get_user_model()


class EmployeeSignUpForm(UserCreationForm):
    title = forms.ChoiceField(
        choices=TitleChoices,
        label="",
        widget=forms.Select(attrs={'placeholder': _('Title')}),
    )

    first_name = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={'placeholder': _('First name')}),
    )

    last_name = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={'placeholder': _('Last name')}),
    )

    job_title = forms.CharField(
        max_length=20,
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Job title')}),
    )

    phone_number = PhoneNumberField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': _('Whatsapp number in format: +1234567890')}),
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': _('Email address')}),
        label="",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
        label="",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password')}),
        label="",
        help_text="",
    )

    class Meta:
        model = UserModel
        fields = [
            'title',
            'first_name',
            'last_name',
            'job_title',
            'phone_number',
            'email',
            'password1',
            'password2',]
        labels = {
            'email': "",
        }

    def save(self, commit=True):
        with transaction.atomic():
            # Save the User instance adding role set up
            user = super().save(commit=False)
            user.is_active = False
            user.role = 'employee'

            if commit:
                user.save()

            # Create a ClientProfile instance
            employee = EmployeeProfile(
                title=self.cleaned_data.get('title'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                job_title=self.cleaned_data.get('job_title'),
                phone_number=self.cleaned_data.get('phone_number'),
                preferred_language='en',
                user=user,
            )

            if commit:
                employee.save()

        return user


class EmployeeEditForm(forms.ModelForm):
    preferred_language = forms.ChoiceField(
        choices=settings.LANGUAGES,
        required=True,
    )


    class Meta:
        model = EmployeeProfile
        fields = ['title', 'first_name', 'last_name', 'job_title', 'phone_number', 'preferred_language']
        labels = {
            'title': "",
            'first_name': "",
            'last_name': "",
            'job_title': "",
            'phone_number': "",
            'preferred_language': "",
        }
