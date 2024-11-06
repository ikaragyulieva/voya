from django.urls import path, include

from voya.requests import views

urlpatterns = [
    path('new-request', views.NewRequestView.as_view(), name='new-request'),
    path('<str:username>/request/<slug:request_slug>/', include([
        path('', views.RequestDetailsView.as_view(), name='request-details'),
        path('edit/', views.EditRequestView.as_view(), name='edit-request'),
        path('delete', views.DeleteRequestView.as_view(), name='delete-request'),
    ]))
]
