"""
Copyright (C) 2025 DROMO SA

This file is part of VOYA.

VOYA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[Project Name] is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
from django.urls import path, include

from voya.providers import views

urlpatterns = [
    path('create-provider/', views.ProviderCreateView.as_view(), name='create-provider'),
    path('provider-dashboard/', views.ProvidersDashboardView.as_view(), name='providers-dashboard'),
    path('<int:pk>/', include([
        path('details/', views.ProviderDetailsView.as_view(), name='provider-details'),
        path('edit/', views.ProviderEditView.as_view(), name='edit-provider'),
        path('delete/', views.DeleteProviderView.as_view(), name='delete-provider'),

    ])),
]
