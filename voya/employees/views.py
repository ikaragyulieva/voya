from django.contrib.auth import mixins
from django.db import models
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from voya.common.forms import SearchForm
from voya.companies.models import CompanyProfile
from voya.employees import forms
from voya.employees.models import EmployeeProfile
from voya.requests.models import TripRequests
from voya.users.models import CustomUser
from voya.utils import get_user_obj


# Create your views here.
class CreateEmployeeView(CreateView):
    model = EmployeeProfile
    form_class = forms.EmployeeSignUpForm
    template_name = 'employees/employee-create-page.html'
    success_url = reverse_lazy('home')


class EmployeeDashboardView(mixins.LoginRequiredMixin, ListView):
    model = TripRequests
    template_name = 'common/dashboard-page.html'

    def get_queryset(self):
        return TripRequests.objects.all().order_by('-is_active', '-created_at')

    def get_object(self, queryset=None):
        return EmployeeProfile.objects.get(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        search_form = SearchForm(self.request.GET)

        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')
            if search_query:
                model_fields = [field for field in self.get_queryset().model._meta.fields if field.name not in ['id', 'created_at'] and field.get_internal_type() not in ['OneToOneField']]

                query = Q()

                # Build a Q object using the field__icontains lookup to search for the query.
                # Use the | operator to combine the Q objects into a single query.
                for field in model_fields:
                    if isinstance(field, models.ForeignKey):
                        related_model = field.related_model
                        if hasattr(related_model, 'commercial_name'):
                            query |= Q(**{f'{field.name}__commercial_name__icontains': search_query})
                        if hasattr(related_model, 'email'):
                            query |= Q(**{f'{field.name}__email__icontains': search_query})
                    else:
                        query |= Q(**{f'{field.name}__icontains': search_query})

                context['triprequests_list'] = self.get_queryset().filter(query)
            else:
                context['triprequests_list'] = self.get_queryset()

        context['profile'] = self.get_object()

        context["search_form"] = search_form
        context['all_requests'] = self.get_queryset()

        return context


class EmployeeProfileDetailsView(mixins.LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'employees/employee-profile-details-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return EmployeeProfile.objects.get(user=self.request.user)


class EditEmployeeProfileView(mixins.LoginRequiredMixin, UpdateView):
    model = EmployeeProfile
    form_class = forms.EmployeeEditForm
    template_name = 'employees/employee-edit-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
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