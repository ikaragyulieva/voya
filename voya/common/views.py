from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from voya.clients.models import ClientProfile
from voya.common import forms
from voya.common.forms import SearchForm
from voya.employees.models import EmployeeProfile
from voya.utils import get_user_obj


# Create your views here.


def home_view(request):
    context = {'profile': get_user_obj(request)}

    return render(request, template_name='common/home-page.html', context=context)


class LogInView(LoginView):
    form_class = forms.LogInForm
    template_name = 'common/login-page.html'
    redirect_authenticated_user = True

    def get_object(self, queryset=None):
        return get_user_obj(self.request)

    def get_success_url(self):
        if self.get_object().user.role == 'client':
            return reverse_lazy(
                'client-dashboard',
                kwargs={
                    'pk': self.get_object().pk
                }
            )
        if self.get_object().user.role == 'employee':
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': self.get_object().pk
                }
            )


def logout_view(request):
    logout(request)
    return redirect('home')
