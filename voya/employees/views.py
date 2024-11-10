from django.contrib.auth import mixins
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from voya.employees import forms
from voya.employees.models import EmployeeProfile


# Create your views here.
class CreateEmployeeView(CreateView):
    model = EmployeeProfile
    form_class = forms.EmployeeSignUpForm
    template_name = 'employees/employee-create-page.html'
    success_url = reverse_lazy('home')


class EmployeeDashboardView(mixins.LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee-dashboard-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return EmployeeProfile.objects.get(user=self.request.user)


class EmployeeProfileDetailsView(mixins.LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee-profile-details-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return EmployeeProfile.objects.get(user=self.request.user)


class EditEmployeeProfileView(mixins.LoginRequiredMixin, UpdateView):
    model = EmployeeProfile
    form_class = forms.EmployeeEditForm
    template_name = 'employees/employee-edit-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return EmployeeProfile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'employee-profile',
            kwargs={
                'pk': self.get_object().pk
            }
        )


class EmployeeDeleteProfileView(mixins.LoginRequiredMixin, DeleteView):
    model = EmployeeProfile
    template_name = 'employees/employee-delete-page.html'
    context_object_name = "profile"
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return EmployeeProfile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'profile': self.get_object()})

    def post(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user_credentials = user_profile.user

        if user_profile.is_active and user_credentials.is_active:
            user_profile.is_active = False
            user_credentials.is_active = False
        else:
            user_profile.is_active = True
            user_credentials.is_active = True

        user_profile.save()
        user_credentials.save()

        return redirect(self.success_url)

