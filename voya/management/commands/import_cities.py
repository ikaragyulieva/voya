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

from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

from voya.services.models import Location


class Command(BaseCommand):
    help = 'Import predefined cities into the Location model'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        admin_user = User.objects.filter(is_superuser=True).first()  # Assign to the first admin user

        cities = [
            {"city": "Amsterdam", "country": "NL"},
            {"city": "Athens", "country": "GR"},
            {"city": "Ávila", "country": "ES"},
            {"city": "Barcelona", "country": "ES"},
            {"city": "Belgrade", "country": "RS"},
            {"city": "Berlin", "country": "DE"},
            {"city": "Bologna", "country": "IT"},
            {"city": "Bordeaux", "country": "FR"},
            {"city": "Bourges", "country": "FR"},
            {"city": "Bruges", "country": "BE"},
            {"city": "Brussels", "country": "BE"},
            {"city": "Budapest", "country": "HU"},
            {"city": "Cappadocia", "country": "TR"},
            {"city": "Capri", "country": "IT"},
            {"city": "Chamonix", "country": "FR"},
            {"city": "Cinque Terre", "country": "IT"},
            {"city": "Coira/Chur", "country": "CH"},
            {"city": "Colmar", "country": "FR"},
            {"city": "Como", "country": "IT"},
            {"city": "Copenhagen", "country": "DK"},
            {"city": "Cracow", "country": "PL"},
            {"city": "Dublin", "country": "IE"},
            {"city": "Dubrovnik", "country": "HR"},
            {"city": "Edinburgh", "country": "GB"},
            {"city": "Fátima", "country": "PT"},
            {"city": "Florence", "country": "IT"},
            {"city": "Frankfurt", "country": "DE"},
            {"city": "Garbagnate Milanese", "country": "IT"},
            {"city": "Geneva", "country": "CH"},
            {"city": "Ghent", "country": "BE"},
            {"city": "Glasgow", "country": "GB"},
            {"city": "Gothenburg", "country": "SE"},
            {"city": "Harrogate", "country": "GB"},
            {"city": "Helsinki", "country": "FI"},
            {"city": "Highlands", "country": "GB"},
            {"city": "Hvar", "country": "HR"},
            {"city": "Ibiza", "country": "ES"},
            {"city": "Istanbul", "country": "TR"},
            {"city": "Lisbon", "country": "PT"},
            {"city": "Lisieux", "country": "FR"},
            {"city": "Liverpool", "country": "GB"},
            {"city": "Loire", "country": "FR"},
            {"city": "London", "country": "GB"},
            {"city": "Lourdes", "country": "FR"},
            {"city": "Lucerne", "country": "CH"},
            {"city": "Lyon", "country": "FR"},
            {"city": "Madrid", "country": "ES"},
            {"city": "Milan", "country": "IT"},
            {"city": "Montecatini Terme", "country": "IT"},
            {"city": "Montserrat", "country": "ES"},
            {"city": "Moscow", "country": "RU"},
            {"city": "Munich", "country": "DE"},
            {"city": "Mykonos", "country": "GR"},
            {"city": "Naples", "country": "IT"},
            {"city": "Nuremberg", "country": "DE"},
            {"city": "Nice", "country": "FR"},
            {"city": "Oporto", "country": "PT"},
            {"city": "Oslo", "country": "NO"},
            {"city": "Pamplona", "country": "ES"},
            {"city": "Paris", "country": "FR"},
            {"city": "Prague", "country": "CZ"},
            {"city": "Pisa", "country": "IT"},
            {"city": "Reykjavik", "country": "IS"},
            {"city": "Rome", "country": "IT"},
            {"city": "Salzburg", "country": "AT"},
            {"city": "Santiago de Compostela", "country": "ES"},
            {"city": "Santorini", "country": "GR"},
            {"city": "Seville", "country": "ES"},
            {"city": "Sofia", "country": "BG"},
            {"city": "Split", "country": "HR"},
            {"city": "Stockholm", "country": "SE"},
            {"city": "Varna", "country": "BG"},
            {"city": "Venice", "country": "IT"},
            {"city": "Vienna", "country": "AT"},
            {"city": "Vinci", "country": "IT"},
            {"city": "Warsaw", "country": "PL"},
            {"city": "Zagreb", "country": "HR"},
            {"city": "Zaragoza", "country": "ES"},
            {"city": "Zurich", "country": "CH"},
            {"city": "Grenoble", "country": "FR"},
            {"city": "Jerez de la Frontera", "country": "ES"},
            {"city": "Chefchaouen", "country": "MAR"},
            {"city": "FEZ", "country": "MAR"},
            {"city": "Rabat", "country": "MAR"},
            {"city": "Reims", "country": "FR"},
            {"city": "Tanger", "country": "MAR"},
            {"city": "Tarragona", "country": "ES"},
            {"city": "Dudley", "country": "GB"},
            {"city": "Leicester", "country": "GB"},
            {"city": "Generic", "country": "ES"},

        ]

        existing_cities = set(Location.objects.values_list("city_name", flat=True))

        new_cities = [
            Location(city_name=city_data["city"], country=city_data["country"], created_by_user=admin_user)
            for city_data in cities if city_data["city"] not in existing_cities
        ]

        if new_cities:
            Location.objects.bulk_create(new_cities)
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(new_cities)} cities'))
        else:
            self.stdout.write(self.style.WARNING("No new cities to import"))
