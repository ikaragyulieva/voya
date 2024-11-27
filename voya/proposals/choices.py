from django.db import models


class SectionChoices(models.TextChoices):
    ACCOMMODATIONS = 'Accommodations', 'Accommodations'
    PUBLIC_TRANSPORT = 'Public Transport', 'Public Transport'
    PRIVATE_TRANSPORT = 'Private Transport', 'Private Transport'
    TRANSFERS = 'Transfers', 'Transfers'
    ACTIVITY = 'Activity', 'Activity'
    GUIDES = 'Guides', 'Guides'


class TransferTypeChoices(models.TextChoices):
    CAR_AROUND_CITY = 'City car', 'Car around the city'
    CAR_TO_AIRPORT = 'Airport car', 'Car to the airport'
    BUS_AROUND_CITY = 'City bus', 'Bus around the city'
    BUS_TO_AIRPORT = 'Airport bus', 'Bus to the airport'

