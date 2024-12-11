from django.urls import path

from voya.proposals import views

urlpatterns = [
    path('create/<int:trip_id>/', views.CreateProposalView.as_view(), name='create-proposal'),
    path('details/<int:proposal_id>/', views.proposal_detail, name='proposal-detail'),
    path('proposal_details/<int:proposal_id>/', views.client_proposal_detail, name='client-proposal-detail'),
    path('api/services/<str:section>/', views.DynamicServiceView.as_view(), name='dynamic-services'),
    path('api/create/<int:trip_id>/', views.ProposalItemsAPI.as_view(), name='proposal-create-api'),

]
