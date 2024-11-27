from django.urls import path, include

from voya.employees import views

urlpatterns = [
    path('create-employee', views.CreateEmployeeView.as_view(), name='create-employee'),
    path('<int:pk>/', include([
        path('', views.EmployeeDashboardView.as_view(), name='employee-dashboard'),
        path('profile/', views.EmployeeProfileDetailsView.as_view(), name='employee-profile'),
        path('edit-profile/', views.EditEmployeeProfileView.as_view(), name='employee-edit'),
        path('delete-profile/', views.EmployeeDeleteProfileView.as_view(), name='employee-delete')
    ])),
]
