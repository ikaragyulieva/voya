from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField

from voya.clients.choices import TitleChoices
from voya.clients.models import ClientProfile
from voya.companies.models import CompanyProfile
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class SignUpClientForm(UserCreationForm):
    title = forms.ChoiceField(
        choices=TitleChoices,
    )

    first_name = forms.CharField(
        max_length=50,
    )

    last_name = forms.CharField(
        max_length=50,
    )

    job_title = forms.CharField(
        max_length=20,
    )

    phone_number = PhoneNumberField()

    tax_id = forms.CharField(
        max_length=20,
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
            'tax_id',
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

    def clean_tax_id(self):
        tax_id = self.cleaned_data.get('tax_id')
        try:
            # Validate if a company with the given tax_id exists
            company = CompanyProfile.objects.get(tax_id=tax_id)
            self.cleaned_data['company'] = company  # Store the company if found
        except CompanyProfile.DoesNotExist:
            raise ValidationError(_("No company with this Tax ID exists."))
        return tax_id

    def save(self, commit=True):
        with transaction.atomic():
            # Save the User instance adding role set up
            user = super().save(commit=False)
            user.role = 'client'
            user.is_active = False  # user is inactive until email confirm

            if commit:
                user.save()

            # Create a ClientProfile instance
            client = ClientProfile(
                title=self.cleaned_data.get('title'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                job_title=self.cleaned_data.get('job_title'),
                phone_number=self.cleaned_data.get('phone_number'),
                company=self.cleaned_data.get('company'),
                user=user,
            )

            if commit:
                client.save()

        return user


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['title', 'first_name', 'last_name', 'job_title', 'phone_number']
        labels = {
            'title': "",
            'first_name': "",
            'last_name': "",
            'job_title': "",
            'phone_number': "",
        }


class ClientLogInForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': _('Your email address')}),
        label=""

    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
        label=""
    )
