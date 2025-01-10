from django import forms
from django.contrib import messages
from django.contrib.auth import mixins
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from django.apps import apps

from voya.common.forms import SearchForm
from voya.common.mixins import PlaceholderMixin
from voya.services.models import LocalGuides, Hotels
from voya.utils import get_user_obj


# Create your views here.


class ServiceDashboardView(mixins.LoginRequiredMixin, ListView):
    template_name = 'services/services-dashboard-page.html'

    def get_model(self):
        model_name = self.kwargs['model_name']
        try:
            return apps.get_model(app_label='services', model_name=model_name)
        except LookupError:
            raise Http404(f'Model {model_name} does not exist')

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all().order_by('-is_active', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_form = SearchForm(self.request.GET)

        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')
            if search_query:
                model_fields = [field.name for field in self.get_queryset().model._meta.fields if
                                field.name not in ['id', 'created_at', 'created_by_user']]
                query = Q()

                # Build a Q object using the field__icontains lookup to search for the query.
                # Use the | operator to combine the Q objects into a single query.
                for field in model_fields:
                    query |= Q(**{f'{field}__icontains': search_query})

                context['service_list'] = self.get_queryset().filter(query)
            else:
                context['service_list'] = self.get_queryset()

        context['search_form'] = search_form
        context['service_queryset'] = self.get_queryset()
        context['model_name'] = self.kwargs['model_name']
        context['profile'] = get_user_obj(self.request)

        return context


class CreateServiceView(mixins.LoginRequiredMixin, CreateView):
    template_name = 'services/create-service.html'

    def get_model(self):
        model_name = self.kwargs['model_name']
        try:
            return apps.get_model(app_label='services', model_name=model_name)
        except LookupError:
            raise Http404(f'Model {model_name} does not exist')

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

    def get_form_class(self):
        class DynamicModelForm(PlaceholderMixin, forms.ModelForm):
            class Meta:
                model = self.get_model()
                # fields = "__all__"
                exclude = ['is_active', 'created_by_user']

        return DynamicModelForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by_user = self.request.user
        instance.save()

        messages.success(self.request, "Service was successfully created")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.kwargs['model_name']
        context['profile'] = get_user_obj(self.request)

        return context

    def get_success_url(self):
        return reverse_lazy('service-dashboard', kwargs={
            'model_name': self.get_model()._meta.model_name
        })


class ServiceEditView(UpdateView):
    template_name = 'services/edit-service-page.html'

    def get_model(self):
        model_name = self.kwargs['model_name']
        try:
            return apps.get_model(app_label='services', model_name=model_name)
        except LookupError:
            raise Http404(f'Model {model_name} does not exist')

    def get_queryset(self):
        model = self.get_model()
        return model.objects.all()

    def get_form_class(self):
        class DynamicModelForm(PlaceholderMixin, forms.ModelForm):
            class Meta:
                model = self.get_model()
                # fields = "__all__"
                exclude = ['is_active', 'created_by_user']

        return DynamicModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['model_name'] = self.kwargs['model_name']
        context['profile'] = get_user_obj(self.request)

        return context

    def get_success_url(self):
        return reverse_lazy('service-dashboard', kwargs={
            'model_name': self.get_model()._meta.model_name
        })


class DeleteServiceView(DeleteView):

    def get_model(self):
        model_name = self.kwargs['model_name']
        try:
            return apps.get_model(app_label='services', model_name=model_name)
        except LookupError:
            raise Http404(f'Model {model_name} does not exist')

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


def service_detail_view(request, model_name, pk):
    try:
        model = apps.get_model(app_label='services', model_name=model_name)
    except LookupError:
        raise Http404(f'Model {model_name} does not exist')

    service = get_object_or_404(model, pk=pk)

    context = {
        'model_name': model_name,
        'service': service,
        'profile': get_user_obj(request),
    }
    return render(request, 'services/service-details-page.html', context)
