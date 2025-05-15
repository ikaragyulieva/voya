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
from django.utils.translation import gettext_lazy as _


class ServiceChoices(models.TextChoices):
    SELECT = '', _('Select an option')
    TRANSFERS = 'transfers', _('Transfers')
    ACTIVITY = 'activity', _('Activity')
    ACCOMMODATION = 'accommodation', _('Accommodation')
    FOOD_AND_BEVERAGE = 'food and beverage', _('Food & Beverage')
    LOCAL_GUIDES = 'local guides', _('Local guides')
    TOUR_LEADERS = 'tour leaders', _('Tour leaders')
    PUBLIC_TRANSPORT = 'public transport', _('Public Transport')
    PRIVATE_TRANSPORT = 'private transport', _('Private Transport')
    OTHER = 'other', _('Other')

