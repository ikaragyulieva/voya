from django.urls import path, include

from voya.companies import views

urlpatterns = [
    path('create-company/', views.CompanyCreateView.as_view(), name='create-company'),
    path('dashboard/', views.CompaniesDashboardView.as_view(), name='companies-dashboard'),
    path('<int:pk>/', include([
        path('details/', views.CompanyDetailsView.as_view(), name='company-details'),
        path('edit/', views.CompanyEditView.as_view(), name='company-edit'),
        path('delete/', views.CompanyDeleteView.as_view(), name='company-delete'),

    ])),
]
