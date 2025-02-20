from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView, PasswordChangeView, \
    PasswordChangeDoneView, PasswordResetDoneView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from voya.common import forms

from voya.utils import get_user_obj, send_activation_email, send_custom_email
from voya.common.tokens import account_activation_token


# Create your views here.


def home_view(request):
    context = {'profile': get_user_obj(request)}

    # return render(request, template_name='common/home-page.html', context=context)
    return render(request, template_name='common/home-page.html', context=context)


class LogInView(LoginView):
    form_class = forms.LogInForm
    template_name = 'common/login-page.html'
    redirect_authenticated_user = True

    def get_object(self, queryset=None):
        return get_user_obj(self.request)

    def get_success_url(self):
        if self.get_object().user.role == 'client':
            return reverse_lazy(
                'client-dashboard',
                kwargs={
                    'pk': self.get_object().pk
                }
            )
        if self.get_object().user.role == 'employee':
            return reverse_lazy(
                'employee-dashboard',
                kwargs={
                    'pk': self.get_object().pk
                }
            )


def activate_account(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    context = {
        'user': user,
        'profile': get_user_obj(request),
    }

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Your account has been confirmed successfully. You can now log in.')
        return render(request, template_name='common/successful-account-activation.html', context=context)
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return render(request, template_name='common/unsuccessful-account-activation.html', context=context)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'common/password_reset_form.html'
    subject_template_name = 'emails/password-reset-subject.txt'
    email_template_name = 'emails/password-reset-email.txt'
    html_email_template_name = 'emails/forgot-password.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        response = super().form_valid(form)
        self.request.session['reset_email'] = email

        return response


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'common/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.get('reset_email', '')

        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Send an extra email to the user when their password is successfully changed."""

    template_name = 'common/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = form.save()

        send_custom_email(
            user=user,
            template_name='emails/new-password-confirmation.html',
            activation_link=None,
            email_subject='Your Voya password has been changed successfully',
            send_to=[user.email, ]
        )

        return render(self.request, 'common/password_reset_complete.html')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'common/password-change-form.html'
    success_url = reverse_lazy('password_change_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = get_user_obj(self.request)

        return context


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'common/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = get_user_obj(self.request)

        return context


def test_email_layout(request):
    UserModel = get_user_model()
    user = UserModel.objects.get(email='ivelina.karagulieva@gmail.com')

    send_activation_email(request, user)
    return HttpResponse(f'Sent test email to {user.email}')


def logout_view(request):
    logout(request)
    return redirect('home')
