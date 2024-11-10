from django.contrib.auth import logout, login
from django.contrib.auth import mixins
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from voya.clients import forms
from voya.clients.models import ClientProfile


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


class ClientDashboardView(mixins.LoginRequiredMixin, DetailView):
    model = ClientProfile
    template_name = 'clients/client-dashboard-page.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return ClientProfile.objects.get(user=self.request.user)
