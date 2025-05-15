from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Search ...')
            }
        ),
    )


class LogInForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': _('Your email address')}),
        label=""

    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
        label=""
    )
