from django.urls import path

from voya.companies.views import CompanyCreateView

urlpatterns = [
    path('create-company/', CompanyCreateView.as_view(), name='create-company')
]
