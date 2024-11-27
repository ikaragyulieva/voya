from django.urls import path

from voya.proposals import views

urlpatterns = [
    path('create/<int:trip_id>/', views.CreateProposalView.as_view(), name='create-proposal'),
    path('api/services/<str:section>/', views.DynamicServiceView.as_view(), name='dynamic-services'),
]
