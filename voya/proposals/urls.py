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

from django.urls import path, include

from voya.proposals import views

urlpatterns = [
    path('create/<int:trip_id>/', views.CreateProposalView.as_view(), name='create-proposal'),
    path('dashboard/', views.ProposalDashboardView.as_view(), name='proposal-dashboard'),
    path('<int:pk>/', include([
        path('details/', views.proposal_detail, name='proposal-detail'),
        path('proposal_details/', views.proposal_detail, name='client-proposal-detail'),
        path('edit/', views.EditProposalView.as_view(), name='edit-proposal'),
        path('history/', views.HistoryLogView.as_view(), name='proposal-history'),
        path('download/', views.proposal_pdf_view, name='proposal_download'),

    ])),



]
