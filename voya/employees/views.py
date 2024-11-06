from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from voya.employees import forms
from voya.employees.models import EmployeeProfile


# Create your views here.
class CreateEmployeeView(CreateView):
    model = EmployeeProfile
    form_class = forms.EmployeeSignUpForm
    template_name = 'employees/create-new-employee-page.html'
    success_url = reverse_lazy('home')


class EmployeeDashboardView(DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee-dashboard-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return EmployeeProfile.objects.get(user=self.request.user)
