from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField

from voya.clients.choices import TitleChoices
from voya.clients.models import ClientProfile
from voya.companies.models import CompanyProfile

UserModel = get_user_model()


class SignUpClientForm(UserCreationForm):
    title = forms.ChoiceField(
        choices=TitleChoices,
        label="",
        widget=forms.Select(attrs={'placeholder': 'Title'}),
    )

    first_name = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'First name'}),
    )

    last_name = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}),
    )

    job_title = forms.CharField(
        max_length=20,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Job title?'}),
    )

    phone_number = PhoneNumberField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Whatsapp number in format: +1234567890'}),
    )
    tax_id = forms.CharField(
        max_length=20,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Company VAT/Tax ID'}),

    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email address'}),
        label="",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
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
        # widgets = {
        #     'email': forms.TextInput(attrs={'placeholder': 'Your Email Address'}),
        #     'password1': forms.PasswordInput(attrs={'placeholder': 'Your Password'}),
        #     'password2': forms.PasswordInput(attrs={'placeholder': 'Please Confirm Your Password'}),
        # }
        # help_texts = {
        #     'password2': "",
        # }

    def clean_tax_id(self):
        tax_id = self.cleaned_data.get('tax_id')
        try:
            # Validate if a company with the given tax_id exists
            company = CompanyProfile.objects.get(tax_id=tax_id)
            self.cleaned_data['company'] = company  # Store the company if found
        except CompanyProfile.DoesNotExist:
            raise ValidationError("No company with this Tax ID exists.")
        return tax_id

    def save(self, commit=True):
        with transaction.atomic():
            # Save the User instance adding role set up
            user = super().save(commit=False)
            user.role = 'client'

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
        widget=forms.TextInput(attrs={'placeholder': 'Your email address'}),
        label=""

    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label=""
    )
