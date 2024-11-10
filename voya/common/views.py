from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from voya.clients.models import ClientProfile
from voya.common import forms
from voya.common.forms import SearchForm
from voya.employees.models import EmployeeProfile


# Create your views here.


def home_view(request):
    context = {}

    if request.user.is_authenticated and request.user.is_active:

        try:
            client_profile = ClientProfile.objects.get(user=request.user, is_active=True)

            context['profile'] = client_profile
        except ClientProfile.DoesNotExist:
            pass

        try:
            employee_profile = EmployeeProfile.objects.get(user=request.user, is_active=True)

            context['profile'] = employee_profile

        except EmployeeProfile.DoesNotExist:
            pass

    # all_request = Pet.objects.all()  # Fetch all the pets
    # search_form = SearchForm(request.GET)
    # if search_form.is_valid():
    #     all_request = all_request.filter(
    #         tagged_pet__name__icontains=search_form.cleaned_data['pet_name']
    #     )

    return render(request, template_name='common/home-page.html', context=context)


class LogInView(LoginView):
    form_class = forms.LogInForm
    template_name = 'common/login-page.html'
    redirect_authenticated_user = True

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL
        client_profile = ClientProfile.objects.filter(user=self.request.user).first()
        if client_profile:
            return client_profile

        employee_profile = EmployeeProfile.objects.filter(user=self.request.user).first()
        if employee_profile:
            return employee_profile

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


