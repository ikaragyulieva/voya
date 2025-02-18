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
from django.apps import apps
from django.db import models


class ServiceChoices(models.TextChoices):
    SELECT = '', 'Select an option'
    TRANSFERS = 'transfers', 'Transfers'
    ACTIVITY = 'activity', 'Activity'
    ACCOMMODATION = 'accommodation', 'Accommodation'
    LOCAL_GUIDES = 'local guides', 'Local guides'
    TOUR_LEADERS = 'tour leaders', 'Tour leaders'
    PUBLIC_TRANSPORT = 'public transport', 'Public Transport'
    PRIVATE_TRANSPORT = 'private transport', 'Private Transport'
    OTHER = 'other', 'Other'

