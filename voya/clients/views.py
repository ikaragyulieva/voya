from django.contrib.auth import logout, login
from django.contrib.auth import mixins
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from voya.clients import forms
from voya.clients.models import ClientProfile
from voya.common.forms import SearchForm
from voya.requests.models import TripRequests
from voya.utils import get_user_obj


class CreateClientView(CreateView):
    model = ClientProfile
    form_class = forms.SignUpClientForm
    template_name = 'clients/client-create-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, form.instance)
        return result


class EditUserProfileView(mixins.LoginRequiredMixin, UpdateView):
    model = ClientProfile
    form_class = forms.ClientEditForm
    template_name = 'clients/client-edit-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return ClientProfile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.get_object().pk
            }
        )


class DeleteClientProfileView(mixins.LoginRequiredMixin, DeleteView):
    model = ClientProfile
    template_name = 'clients/client-delete-page.html'
    context_object_name = "profile"
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return ClientProfile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'profile': self.get_object()})

    def post(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user_credentials = user_profile.user
        user_profile.is_active = False
        user_credentials.is_active = False
        user_profile.save()
        user_credentials.save()

        logout(self.request)

        return redirect(self.success_url)


class ProfileDetailsView(mixins.LoginRequiredMixin, DetailView):
    model = ClientProfile
    template_name = 'clients/client-profile-details-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return ClientProfile.objects.get(user=self.request.user)


class ClientDashboardView(mixins.LoginRequiredMixin, ListView):
    model = TripRequests
    template_name = 'common/dashboard-page.html'

    def get_object(self, queryset=None):
        return ClientProfile.objects.get(user=self.request.user)

    def get_context_data(self, queryset=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = SearchForm(self.request.GET)
        queryset = TripRequests.objects.filter(created_by_company=self.get_object().company).order_by('-is_active',
                                                                                                      '-created_at')
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')

            if search_query:
                model_fields = [field.name for field in queryset.model._meta.fields
                                if field.name not in ['id', 'created_at', 'created_by_company_id', 'created_by_user_id']
                                and field.get_internal_type() not in ['ForeignKey', 'OneToOneField']]
                query = Q()

                # Build a Q object using the field__icontains lookup to search for the query.
                # Use the | operator to combine the Q objects into a single query.
                for field in model_fields:
                    query |= Q(**{f'{field}__icontains': search_query})

                context['triprequests_list'] = queryset.filter(query)
            else:
                context['triprequests_list'] = queryset

        context['profile'] = self.get_object()
        context['all_requests'] = queryset
        context['search_form'] = search_form

        return context
