from django.urls import path, include

from voya.employees import views

urlpatterns = [
    path('create-employee', views.CreateEmployeeView.as_view(), name='create-employee'),
    path('<int:pk>/', include([
        path('', views.EmployeeDashboardView.as_view(), name='employee-dashboard'),
    ])),
]
