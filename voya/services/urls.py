from django.urls import path, include

from voya.services import views

urlpatterns = [
    path('<str:model_name>/', include([
        path('', views.ServiceDashboardView.as_view(), name='service-dashboard'),
        path('create/', views.CreateServiceView.as_view(), name='create-service'),
        path('<int:pk>/', include([
            path('', views.service_detail_view, name='service-details'),
            path('edit/', views.ServiceEditView.as_view(), name='edit-service'),
            path('desactivate/', views.DeleteServiceView.as_view(), name='delete-service'),
        ]))
    ]))
]
