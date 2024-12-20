from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search ...'
            }
        ),
    )


class LogInForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Your email address'}),
        label=""

    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label=""
    )