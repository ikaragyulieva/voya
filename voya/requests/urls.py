from django.urls import path, include

from voya.requests import views

urlpatterns = [
    path('new-request/', views.NewRequestView.as_view(), name='new-request'),
    path('<int:pk>/', include([
        path('', views.RequestDetailsView.as_view(), name='request-details'),
        path('edit/', views.EditRequestView.as_view(), name='edit-request'),
        path('clone/', views.CloneRequestView.as_view(), name='clone-request'),
        path('delete/', views.DeleteRequestView.as_view(), name='delete-request'),
    ]))
]
