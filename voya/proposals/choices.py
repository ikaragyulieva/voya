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

from django.db import models
from django.utils.translation import gettext_lazy as _


class SectionChoices(models.TextChoices):
    ACCOMMODATIONS = 'Accommodations', _('Accommodations')
    PUBLIC_TRANSPORT = 'Public Transport', _('Public Transport')
    PRIVATE_TRANSPORT = 'Private Transport', _('Private Transport')
    TRANSFERS = 'Transfers', _('Transfers')
    ACTIVITY = 'Activity', _('Activity')
    LOCAL_GUIDES = 'Local Guides', _('Local Guides')
    TOUR_LEADERS = 'Tour Leader', _('Tour Leader')
    MEALS = 'Meals', _('Meals')
    OTHER_SERVICES = 'Other Services - Variable', _('Other Services - Variable')
    OTHER_SERVICES_FIXED = 'Other Services - Fixed', _('Other Services - Fixed')


class TransferTypeChoices(models.TextChoices):
    CHOOSE_TRANSFER = '', _('Select an option')
    CAR_AROUND_CITY = 'City car', _('Car around the city')
    CAR_TO_AIRPORT = 'Airport car', _('Car to the airport')
    BUS_AROUND_CITY = 'City bus', _('Bus around the city')
    BUS_TO_AIRPORT = 'Airport bus', _('Bus to the airport')
    PRIVATE_BOAT = 'Private boat', _('Private boat')
    LUXURY_CAR = 'Luxury car (4pax)', _('Luxury car (4 pax)')
    LUXURY_VAN = 'Luxury van (7pax)', _('Luxury van (7 pax)')
    LUXURY_BUS = 'Luxury bus (8+pax)', _('Luxury bus (8+ pax)')


class StatusChoices(models.TextChoices):
    SELECT_CHOICE = '', _('Select an option')
    DRAFT = 'Not finished', _('Not finished')
    IN_PROGRESS = 'Ready for review', _('Ready for review')
    DONE = 'Send to client', _('Send to client')
    APPROVED = 'Approved by client', _('Approved by client')
    REJECTED = 'Rejected by client', _('Rejected by client')


class LogoChoices(models.TextChoices):
    NONE = "None", _("None")
    DROMO_LOGO = "Dromo", _("Dromo")
    COMPANY_LOGO = "My company's logo", _("My company's logo")


class MealChoices(models.TextChoices):
    BREAKFAST = "Breakfast", _("Breakfast")
    LUNCH = "Lunch", _("Lunch")
    DINNER = "Dinner", _("Dinner")
    OTHER = "Other", _("Other")
