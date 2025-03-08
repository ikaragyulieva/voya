from django.contrib.auth import mixins
from django.db import models
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from voya.common.forms import SearchForm
from voya.employees.models import EmployeeProfile
from voya.providers.forms import ProviderCreateForm
from voya.providers.models import Providers
from voya.utils import get_user_obj


# Create your views here.

class ProviderCreateView(mixins.LoginRequiredMixin, CreateView):
    model = Providers
    form_class = ProviderCreateForm
    template_name = 'providers/create-provider.html'
    success_url = reverse_lazy('providers-dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)

        return context


class ProviderEditView(mixins.LoginRequiredMixin, UpdateView):
    model = Providers
    form_class = ProviderCreateForm
    template_name = 'providers/edit-provider.html'
    success_url = reverse_lazy('providers-dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)

        return context


class ProvidersDashboardView(mixins.LoginRequiredMixin, ListView):
    model = Providers
    template_name = 'providers/providers-dashboard.html'
    paginate_by = 10

    def get_object(self, queryset=None):
        return EmployeeProfile.objects.get(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        search_form = SearchForm(self.request.GET)
        providers_query = Providers.objects.all().order_by('-is_active', '-created_at')

        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')
            if search_query:
                model_fields = [field for field in self.get_queryset().model._meta.fields if
                                field.name not in ['id', 'created_at'] and field.get_internal_type() not in [
                                    'OneToOneField']]

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
                        if hasattr(related_model, 'city_name'):
                            query |= Q(**{f'{field.name}__city_name__icontains': search_query})
                    else:
                        query |= Q(**{f'{field.name}__icontains': search_query})

                context['providers_list'] = self.get_queryset().filter(query)
            else:
                context['providers_list'] = self.get_queryset()

        context['profile'] = self.get_object()
        context['all_providers'] = providers_query
        context["search_form"] = search_form

        return context


class ProviderDetailsView(mixins.LoginRequiredMixin, DetailView):
    model = Providers
    template_name = 'providers/provider-details-page.html'
    context_object_name = 'provider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)

        return context


class DeleteProviderView(mixins.LoginRequiredMixin, DeleteView):
    model = Providers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_user_obj(self.request)

        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        provider = self.get_object()

        provider.is_active = not provider.is_active
        provider.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('providers-dashboard')
