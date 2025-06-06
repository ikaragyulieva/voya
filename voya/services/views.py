from django import forms
from django.contrib import messages
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.apps import apps

from voya.common.forms import SearchForm
from voya.common.mixins import PlaceholderMixin
from voya.providers.models import Providers
from voya.services.models import LocalGuide, Hotel, Location
from voya.utils import get_user_obj


MODEL_TITLES = {
    'hotel': _('hotels'),
    'publictransport': _('public transport'),
    'privatetransport': _('private transport'),
    'ticket': _('activities'),
    'transfer': _('transfers'),
    'localguide': _('local guides'),
    'staff': _('tour leaders'),
    'currency':  _('currencies'),
    'location': _('location'),
}


class ServiceDashboardView(mixins.LoginRequiredMixin, ListView):
    template_name = 'services/services-dashboard-page.html'
    ALLOWED_MODELS = [
        'hotel',
        'publictransport',
        'privatetransport',
        'activity',
        'ticket',
        'transfer',
        'localguide',
        'staff',
        'currency',
        'location',
        'other']

    def get_model(self):
        model_name = self.kwargs['model_name']
        if model_name not in self.ALLOWED_MODELS:
            raise Http404(_('Model %(model_name)s does not exist or is not allowed.') % {'model_name': model_name})
        try:
            return apps.get_model(app_label='services', model_name=model_name)
        except LookupError:
            raise Http404(_('Model %m(model_name)s does not exist') % {'model_name': model_name})

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all().order_by('-is_active', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model = self.kwargs['model_name']
        model_title = MODEL_TITLES.get(model, model)

        search_form = SearchForm(self.request.GET)

        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')
            if search_query:
                model_fields = [field.name for field in self.get_queryset().model._meta.fields if
                                field.name not in ['id', 'created_at', 'created_by_user', 'website']]
                query = Q()

                # Build a Q object using the field__icontains lookup to search for the query.
                # Use the | operator to combine the Q objects into a single query.
                for field in model_fields:
                    field_type = self.get_queryset().model._meta.get_field(field)

                    if isinstance(field_type, models.ForeignKey):
                        if field == 'city':
                            query |= Q(city__city_name__icontains=search_query)
                        elif field == 'provider':
                            query |= Q(provider__commercial_name__icontains=search_query)
                        elif field == 'country':
                            query |= Q(country__name__icontains=search_query)
                        # elif field == 'country':

                    else:
                        query |= Q(**{f'{field}__icontains': search_query})

                print(f"Final search query: {query}")

                context['service_list'] = self.get_queryset().filter(query)
            else:
                context['service_list'] = self.get_queryset()

        context['search_form'] = search_form
        context['service_queryset'] = self.get_queryset()
        context['model_name'] = model
        context['model_title'] = model_title
        context['profile'] = get_user_obj(self.request)

        return context


class CreateServiceView(mixins.LoginRequiredMixin, CreateView):
    template_name = 'services/create-service.html'

    def get_model(self):
        model_name = self.kwargs['model_name']
        try:
            return apps.get_model(app_label='services', model_name=model_name)
        except LookupError:
            raise Http404(_('Model %(model_name)s does not exist') % {'model_name': model_name})

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

    def get_form_class(self):
        service_name = self.kwargs['model_name']

        if service_name == 'hotel':
            service_name = 'accommodation'
        elif service_name == 'publictransport':
            service_name = 'public transport'
        elif service_name == 'privatetransport':
            service_name = 'private transport'
        elif service_name == 'ticket':
            service_name = 'activity'
        elif service_name == 'transfer':
            service_name = 'transfers'
        elif service_name == 'localguide':
            service_name = 'local guides'
        elif service_name == 'staff':
            service_name = 'tour leaders'

        eligible_providers = Providers.objects.filter(services__icontains=service_name) | Providers.objects.filter(
            services__icontains='other')
        cities = Location.objects.all().order_by('city_name')

        class DynamicModelForm(PlaceholderMixin, forms.ModelForm):
            class Meta:
                model = self.get_model()
                # fields = "__all__"
                exclude = ['is_active', 'created_by_user']
                # widgets = {
                #     'city_name': forms.Select(),
                # }

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if 'provider' in self.fields:
                    self.fields['provider'].queryset = eligible_providers
                    self.fields['provider'].empty_label = _("Select an option")
                if 'city' in self.fields:
                    self.fields['city'].queryset = cities
                    self.fields['city'].empty_label = _("Select a city")

        return DynamicModelForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by_user = self.request.user
        instance.save()

        messages.success(self.request, _("Service was successfully created"))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model = self.kwargs['model_name']
        model_title = MODEL_TITLES.get(model, model)

        context['model_name'] = model
        context['profile'] = get_user_obj(self.request)
        context['model_title'] = model_title

        return context

    def get_success_url(self):
        return reverse_lazy('service-dashboard', kwargs={
            'model_name': self.get_model()._meta.model_name
        })


class ServiceEditView(mixins.LoginRequiredMixin, UpdateView):
    template_name = 'services/edit-service-page.html'

    def get_model(self):
        model_name = self.kwargs['model_name']
        try:
            return apps.get_model(app_label='services', model_name=model_name)
        except LookupError:
            raise Http404(_('Model %(model_name)s does not exist') % {'model_name': model_name})

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

    def get_form_class(self):

        service_name = self.kwargs['model_name']

        if service_name == 'hotel':
            service_name = 'accommodation'
        elif service_name == 'publictransport':
            service_name = 'public transport'
        elif service_name == 'privatetransport':
            service_name = 'private transport'
        elif service_name == 'ticket':
            service_name = 'activity'
        elif service_name == 'transfer':
            service_name = 'transfers'
        elif service_name == 'localguide':
            service_name = 'local guides'
        elif service_name == 'staff':
            service_name = 'tour leaders'

        eligible_providers = Providers.objects.filter(services__icontains=service_name) | Providers.objects.filter(
            services__icontains='other')
        cities = Location.objects.all().order_by('city_name')

        class DynamicModelForm(PlaceholderMixin, forms.ModelForm):
            class Meta:
                model = self.get_model()
                # fields = "__all__"
                exclude = ['is_active', 'created_by_user']

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if 'provider' in self.fields:
                    self.fields['provider'].queryset = eligible_providers
                    self.fields['provider'].empty_label = _("Select an option")
                    self.fields['city'].queryset = cities
                    self.fields['city'].empty_label = _("Select an option")

        return DynamicModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model = self.kwargs['model_name']
        model_title = MODEL_TITLES.get(model, model)

        context['model_name'] = model
        context['model_title'] = model_title
        context['profile'] = get_user_obj(self.request)

        return context

    def get_success_url(self):
        return reverse_lazy('service-dashboard', kwargs={
            'model_name': self.get_model()._meta.model_name
        })


class DeleteServiceView(mixins.LoginRequiredMixin, DeleteView):

    def get_model(self):
        model_name = self.kwargs['model_name']
        try:
            return apps.get_model(app_label='services', model_name=model_name)
        except LookupError:
            raise Http404(_('Model %(model_name)s does not exist') % {'model_name': model_name})

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.kwargs['model_name']
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
        return reverse_lazy('service-dashboard', kwargs={
            'model_name': self.get_model()._meta.model_name
        })


@login_required
def service_detail_view(request, model_name, pk):
    try:
        model = apps.get_model(app_label='services', model_name=model_name)
    except LookupError:
        raise Http404(_('Model %(model_name) does not exist') % {'model_name': model_name})

    service = get_object_or_404(model, pk=pk)

    context = {
        'model_name': model_name,
        'service': service,
        'profile': get_user_obj(request),
    }
    return render(request, 'services/service-details-page.html', context)
