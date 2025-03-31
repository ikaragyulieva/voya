from django.contrib.auth import mixins
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from voya.clients.models import ClientProfile
from voya.employees.models import EmployeeProfile
from voya.proposals.models import Proposal
from voya.proposals.utils import clone_proposal_data
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
        if self.request.user.role == 'employee':
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
        elif self.request.user.role == 'client':
            return reverse_lazy(
                'client-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )


class CloneRequestView(NewRequestView):
    def get_initial(self):
        original_request = get_object_or_404(models.TripRequests, pk=self.kwargs['pk'])
        initial_data = super().get_initial()
        for field in self.form_class.Meta.fields:
            initial_data[field] = getattr(original_request, field)

        initial_data['field_to_clear_or_update'] = None
        return initial_data

    def form_valid(self, form):
        # Get original request before it is overwritten, to use it for cloning proposal
        original_request = get_object_or_404(models.TripRequests, pk=self.kwargs['pk'])

        # Prevent updating the original request
        form.instance.pk = None
        # Save the new trip request
        response = super().form_valid(form)

        # Clone proposal if it exists
        if hasattr(original_request, 'request_proposal'):
            try:
                original_proposal = original_request.request_proposal
                clone_proposal_data(original_proposal, self.object, self.request.user)
            except Proposal.DoesNotExist:
                pass

        return response


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
        if self.request.user.role == 'employee':
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
        elif self.request.user.role == 'client':
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
        if self.request.user.role == 'employee':
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
        elif self.request.user.role == 'client':
            return reverse_lazy(
                'client-dashboard',
                kwargs={
                    'pk': profile.pk
                }
            )
