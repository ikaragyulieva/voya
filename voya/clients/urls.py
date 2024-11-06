from django.contrib import admin
from django.urls import path, include

from voya.clients import views

urlpatterns = [
    path('create-user/', views.CreateClientView.as_view(), name='create-client'),
    path('<int:pk>/', include([
        path('', views.ClientDashboardView.as_view(), name='client-dashboard'),
        path('edit-profile/', views.EditUserProfileView.as_view(), name='edit-client-profile'),
        path('profile-details', views.ProfileDetailsView.as_view(), name='profile-details'),
        path('deleteprofile/', views.DeleteClientProfileView.as_view(), name='delete-client-profile')
    ]))

]
