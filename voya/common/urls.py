from django.urls import path, reverse_lazy

from voya.common import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Home, login, logout
    path('', views.home_view, name='home'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Activate user account / Confirm email when account is created
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),

    # Reset Password
    path(
        'password-reset/',
        views.CustomPasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password-reset/done',
        views.CustomPasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='common/password_reset_complete.html'),
        name='password_reset_complete'
    ),

    path('test-email/', views.test_email_layout, name='test-email'),

    # Change password
    path(
        'password-change/',
        views.CustomPasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password-change/done/',
        views.CustomPasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
]
