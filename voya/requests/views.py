from django.contrib.auth import mixins
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from voya.clients.models import ClientProfile
from voya.employees.models import EmployeeProfile
from voya.requests import models, forms
from voya.utils import get_user_obj


# Create your views here.

class RequestDetailsView(mixins.LoginRequiredMixin, DetailView):
    model = models.TripRequests
    template_name = 'requests/request-details-page.html'
    context_object_name = 'trip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)

        return context


class NewRequestView(mixins.LoginRequiredMixin, CreateView):
    model = models.TripRequests
    form_class = forms.CreateRequestForm
    template_name = 'requests/create-new-request-page.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)

        return context

    def get_success_url(self):
        profile = get_user_obj(self.request)

        if profile is None or profile.pk is None:
            # Log an error or redirect to a default fallback
            return reverse_lazy('home')

        if hasattr(self.request.user, 'employee_profile'):
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
        elif hasattr(self.request.user, 'client-profile'):
            return reverse_lazy(
                'client-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )


class CloneRequestView(NewRequestView):
    template_name = 'requests/duplicate-request-page.html'

    def get_initial(self):
        original_request = get_object_or_404(models.TripRequests, pk=self.kwargs['pk'])
        initial_data = super().get_initial()
        for field in self.form_class.Meta.fields:
            initial_data[field] = getattr(original_request, field)

        initial_data['field_to_clear_or_update'] = None
        return initial_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)
        context['trip_request'] = get_object_or_404(models.TripRequests, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.pk = None
        return super().form_valid(form)

    def get_success_url(self):
        profile = get_user_obj(self.request)

        if profile is None or profile.pk is None:
            # Log an error or redirect to a default fallback
            return reverse_lazy('home')

        if hasattr(self.request.user, 'employee_profile'):
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
        elif hasattr(self.request.user, 'client-profile'):
            return reverse_lazy(
                'client-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )


class EditRequestView(mixins.LoginRequiredMixin, UpdateView):
    model = models.TripRequests
    form_class = forms.CreateRequestForm
    template_name = 'requests/edit-request-page.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)

        return context

    def get_success_url(self):
        profile = get_user_obj(self.request)
        if hasattr(self.request.user, 'employee_profile'):
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
        elif hasattr(self.request.user, 'client-profile'):
            return reverse_lazy(
                'client-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )


class DeleteRequestView(mixins.LoginRequiredMixin, DeleteView):
    model = models.TripRequests

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)

        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        trip = self.get_object()

        trip.is_active = not trip.is_active
        trip.save()

        return redirect(self.get_success_url())

    def get_success_url(self):

        profile = get_user_obj(self.request)
        if hasattr(self.request.user, 'employee_profile'):
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
        elif hasattr(self.request.user, 'client-profile'):
            return reverse_lazy(
                'client-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
