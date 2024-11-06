from django.urls import path

from voya.common import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

]
