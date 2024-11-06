from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from voya.clients import forms
from voya.clients.models import ClientProfile


class CreateClientView(CreateView):
    model = ClientProfile
    form_class = forms.SignUpClientForm
    template_name = 'clients/create-user.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, form.instance)

        return result


# class ClientLogIn(LoginView):
#     form_class = forms.ClientLogInForm
#     template_name = 'clients/../../templates/common/login-page.html'
#
#     def get_object(self, queryset=None):
#         # Fetch the ClientProfile based on the URL pk
#         return ClientProfile.objects.get(user=self.request.user)
#
#     def get_success_url(self):
#         return reverse_lazy(
#             'dashboard',
#             kwargs={
#                 'pk': self.get_object().pk
#             }
#         )
#
#     redirect_authenticated_user = True


# def logout_view(request):
#     logout(request)
#     return redirect('home')


class EditUserProfileView(UpdateView):
    model = ClientProfile
    form_class = forms.ClientEditForm
    template_name = 'clients/client-profile-edit.html'
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


class DeleteClientProfileView(DeleteView):
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


class ProfileDetailsView(DetailView):
    model = ClientProfile
    template_name = 'clients/client-profile-details.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return ClientProfile.objects.get(user=self.request.user)


class ClientDashboardView(DetailView):
    model = ClientProfile
    template_name = 'clients/client-dashboard.html'
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Fetch the ClientProfile based on the URL pk
        return ClientProfile.objects.get(user=self.request.user)
