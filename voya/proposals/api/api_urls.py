"""
Copyright (C) 2025 DROMO SA

This file is part of VOYA.

VOYA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VOYA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
from django.urls import path

from voya.proposals.api import views

urlpatterns = [
    path('services/<str:section>/', views.DynamicServiceView.as_view(), name='dynamic-services'),
    # path('create/<int:trip_id>/', views.ProposalItemsAPI.as_view(), name='proposal-create-api'),
    # path('edit/<int:pk>/', views.ProposalUpdateAPI.as_view(), name='proposal-edit-api'),
    path('save-and-validate/', views.SaveAndValidateProposalAPI.as_view(), name='save-validate-api')
]
