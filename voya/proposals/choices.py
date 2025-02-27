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


class SectionChoices(models.TextChoices):
    ACCOMMODATIONS = 'Accommodations', 'Accommodations'
    PUBLIC_TRANSPORT = 'Public Transport', 'Public Transport'
    PRIVATE_TRANSPORT = 'Private Transport', 'Private Transport'
    TRANSFERS = 'Transfers', 'Transfers'
    ACTIVITY = 'Activity', 'Activity'
    LOCAL_GUIDES = 'Local Guides', 'Local Guides'
    TOUR_LEADERS = 'Tour Leader', 'Tour Leader'
    OTHER_SERVICES = 'Other Services', 'Other Services'


class TransferTypeChoices(models.TextChoices):
    CHOOSE_TRANSFER = '', 'Select an option'
    CAR_AROUND_CITY = 'City car', 'Car around the city'
    CAR_TO_AIRPORT = 'Airport car', 'Car to the airport'
    BUS_AROUND_CITY = 'City bus', 'Bus around the city'
    BUS_TO_AIRPORT = 'Airport bus', 'Bus to the airport'
    PRIVATE_BOAT = 'private boat', 'Private boat'
    LUXURY_CAR = 'luxury car (4pax)', 'Luxury car (4 pax)'
    LUXURY_VAN = 'luxury van (7pax)', 'Luxury van (7 pax)'
    LUXURY_BUS = 'luxury bus (8+pax)', 'Luxury bus (8+ pax)'


class StatusChoices(models.TextChoices):
    SELECT_CHOICE = '', 'Select an option'
    DRAFT = 'Draft', 'Draft'
    DONE = 'Done', 'Done'
    IN_PROGRESS = 'In progress', 'In progress'


class LogoChoices(models.TextChoices):
    NONE = "None", "None"
    VOYA_LOGO = "Voya logo", "Voya logo"
    COMPANY_LOGO = "My company's logo", "My company's logo"
