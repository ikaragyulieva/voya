from django.db import models


class CityChoices(models.TextChoices):
    SELECT_CITY = 'Select city', 'Select city'
    AMSTERDAM = 'Amsterdam', 'Amsterdam'
    ATHENS = 'Athens', 'Athens'
    BARCELONA = 'Barcelona', 'Barcelona'
    BELGRADE = 'Belgrade', 'Belgrade'
    BERLIN = 'Berlin', 'Berlin'
    BRUGES = 'Bruges', 'Bruges'
    BRUSSELS = 'Brussels', 'Brussels'
    BUDAPEST = 'Budapest', 'Budapest'
    COPENHAGEN = 'Copenhagen', 'Copenhagen'
    DUBLIN = 'Dublin', 'Dublin'
    EDINBURGH = 'Edinburgh', 'Edinburgh'
    FLORENCE = 'Florence', 'Florence'
    GENEVA = 'Geneva', 'Geneva'
    HELSINKI = 'Helsinki', 'Helsinki'
    ISTANBUL = 'Istanbul', 'Istanbul'
    LISBON = 'Lisbon', 'Lisbon'
    LONDON = 'London', 'London'
    LUCERNE = 'Lucerne', 'Lucerne'
    MADRID = 'Madrid', 'Madrid'
    MILAN = 'Milan', 'Milan'
    MOSCOW = 'Moscow', 'Moscow'
    MUNICH = 'Munich', 'Munich'
    NAPLES = 'Naples', 'Naples'
    NICE = 'Nice', 'Nice'
    OSLO = 'Oslo', 'Oslo'
    PARIS = 'Paris', 'Paris'
    PRAGUE = 'Prague', 'Prague'
    PISA = 'Pisa', 'Pisa'
    REYKJAVIK = 'Reykjavik', 'Reykjavik'
    ROME = 'Rome', 'Rome'
    SALZBURG = 'Salzburg', 'Salzburg'
    SANTORINI = 'Santorini', 'Santorini'
    SEVILLE = 'Seville', 'Seville'
    SOFIA = 'Sofia', 'Sofia'
    SPLIT = 'Split', 'Split'
    STOCKHOLM = 'Stockholm', 'Stockholm'
    VARNA = 'Varna', 'Varna'
    VENICE = 'Venice', 'Venice'
    VIENNA = 'Vienna', 'Vienna'
    WARSAW = 'Warsaw', 'Warsaw'
    ZAGREB = 'Zagreb', 'Zagreb'
    ZURICH = 'Zurich', 'Zurich'


# CITIES_BY_COUNTRY = {
#     'Austria': [('Vienna', 'Vienna'), ('Salzburg', 'Salzburg')],
#     'Belgium': [('Bruges', 'Bruges'), ('Brussels', 'Brussels')],
#     'Croatia': [('Split', 'Split'), ('Zagreb', 'Zagreb')],
#     'Czech Republic': [('Prague', 'Prague')],
#     'Denmark': [('Copenhagen', 'Copenhagen')],
#     'Finland': [('Helsinki', 'Helsinki')],
#     'France': [('Paris', 'Paris'), ('Nice', 'Nice')],
#     'Germany': [('Berlin', 'Berlin'), ('Munich', 'Munich')],
#     'Greece': [('Athens', 'Athens'), ('Santorini', 'Santorini')],
#     'Hungary': [('Budapest', 'Budapest')],
#     'Iceland': [('Reykjavik', 'Reykjavik')],
#     'Ireland': [('Dublin', 'Dublin')],
#     'Italy': [('Rome', 'Rome'), ('Florence', 'Florence'), ('Milan', 'Milan'), ('Venice', 'Venice'), ('Naples', 'Naples')],
#     'Netherlands': [('Amsterdam', 'Amsterdam')],
#     'Norway': [('Oslo', 'Oslo')],
#     'Poland': [('Warsaw', 'Warsaw')],
#     'Portugal': [('Lisbon', 'Lisbon')],
#     'Russia': [('Moscow', 'Moscow')],
#     'Spain': [('Madrid', 'Madrid'), ('Barcelona', 'Barcelona'), ('Seville', 'Seville')],
#     'Sweden': [('Stockholm', 'Stockholm')],
#     'Switzerland': [('Zurich', 'Zurich'), ('Lucerne', 'Lucerne')],
#     'Turkey': [('Istanbul', 'Istanbul')],
#     'United Kingdom': [('London', 'London'), ('Edinburgh', 'Edinburgh')],
# }

class CountryChoices(models.TextChoices):
    # European countries
    ALBANIA = "AL", "Albania"
    ANDORRA = "AD", "Andorra"
    ARMENIA = "AM", "Armenia"
    AUSTRIA = "AT", "Austria"
    AZERBAIJAN = "AZ", "Azerbaijan"
    BELARUS = "BY", "Belarus"
    BELGIUM = "BE", "Belgium"
    BOSNIA_AND_HERZEGOVINA = "BA", "Bosnia and Herzegovina"
    BULGARIA = "BG", "Bulgaria"
    CROATIA = "HR", "Croatia"
    CYPRUS = "CY", "Cyprus"
    CZECH_REPUBLIC = "CZ", "Czech Republic"
    DENMARK = "DK", "Denmark"
    ESTONIA = "EE", "Estonia"
    FINLAND = "FI", "Finland"
    FRANCE = "FR", "France"
    GEORGIA = "GE", "Georgia"
    GERMANY = "DE", "Germany"
    GREECE = "GR", "Greece"
    HUNGARY = "HU", "Hungary"
    ICELAND = "IS", "Iceland"
    IRELAND = "IE", "Ireland"
    ITALY = "IT", "Italy"
    KOSOVO = "XK", "Kosovo"
    LATVIA = "LV", "Latvia"
    LIECHTENSTEIN = "LI", "Liechtenstein"
    LITHUANIA = "LT", "Lithuania"
    LUXEMBOURG = "LU", "Luxembourg"
    MALTA = "MT", "Malta"
    MOLDOVA = "MD", "Moldova"
    MONACO = "MC", "Monaco"
    MONTENEGRO = "ME", "Montenegro"
    NETHERLANDS = "NL", "Netherlands"
    NORTH_MACEDONIA = "MK", "North Macedonia"
    NORWAY = "NO", "Norway"
    POLAND = "PL", "Poland"
    PORTUGAL = "PT", "Portugal"
    ROMANIA = "RO", "Romania"
    SAN_MARINO = "SM", "San Marino"
    SERBIA = "RS", "Serbia"
    SLOVAKIA = "SK", "Slovakia"
    SLOVENIA = "SI", "Slovenia"
    SPAIN = "ES", "Spain"
    SWEDEN = "SE", "Sweden"
    SWITZERLAND = "CH", "Switzerland"
    TURKEY = "TR", "Turkey"
    UKRAINE = "UA", "Ukraine"
    UNITED_KINGDOM = "GB", "United Kingdom"
    VATICAN_CITY = "VA", "Vatican City"

    # Mediterranean non-European countries
    ALGERIA = "DZ", "Algeria"
    EGYPT = "EG", "Egypt"
    ISRAEL = "IL", "Israel"
    LEBANON = "LB", "Lebanon"
    LIBYA = "LY", "Libya"
    MOROCCO = "MA", "Morocco"
    PALESTINE = "PS", "Palestine"
    SYRIA = "SY", "Syria"
    TUNISIA = "TN", "Tunisia"


class TransportationType(models.TextChoices):
    TRANSPORT = 'transport', 'Select transportation type'
    NO_TRANSPORTATION = 'no transportation', 'No transportation - I\'ll take care of it'
    PRIVATE_BUS = 'private bus', 'Private Bus'
    PUBLIC_BUSES = 'public buses', 'Public Buses'
    TRAINS = 'trains', 'Trains'
    FLIGHTS = 'flights', 'Flights'
    TAXI = 'taxi', 'Taxi'
    AIRPORT_STATION_TRANSFERS = 'airport/station transfers', 'Airport/Station Transfers'


class AccommodationsType(models.TextChoices):
    ACC = 'acc', 'Select accommodations type'
    NONE = 'none', 'None -  I\'ll take care of it'
    TWO_TREE_STAR_HOTELS = '2-3 star hotels', '2-3 Star Hotels'
    FOUR_FIVE_STAR_HOTELS = '4-5 star hotels', '4-5 Star Hotels'
    HOSTELS_WITH_PRIVATE_BATHROOM = 'hostels with private bathroom', 'Hostels with private bathroom'
    APARTMENT = 'apartment', 'Apartment'
    CAMPING = 'camping', 'Camping'


class MealsType(models.TextChoices):
    MEALS = 'meal', 'Select meals service'
    NO_MEALS_INCLUDED = 'no meals included', 'No meals included'
    BREAKFAST_ONLY = 'breakfast only (BB)', 'Breakfast Only (BB)'
    BREAKFAST_AND_DINNER = 'breakfast & dinner (HB)', 'Breakfast & Dinner (HB)'
    BREAKFAST_LUNCH_DINNER = 'breakfast, lunch & dinner (FB)', 'Breakfast, Lunch & Dinner (FB)'


class StaffChoices(models.TextChoices):
    STAFF = 'staff', "Select staff service"
    TOUR_LEADER = 'Tour leader during the entire trip', 'Tour leader during the entire trip'
    OFFICIAL_TOURIST_GUIDES = 'Official tourist guides in each city'


class GroupChoice(models.TextChoices):
    GROUP = "group", "Select type of group"
    CULTURAL_SIGHTSEEING = "cultural_sightseeing", "Cultural Group - Sightseeing"
    SCHOOLS_YOUTH = "schools_youth", "Schools, Students or Youth"
    BACKPACKERS = "backpackers", "Backpackers"
    THEME_PARKS = "theme_parks", "Theme Parks (Eurodisney, Pinocchio, Mirabilandia, Puerto Aventura, Harry Potter...)"
    STUDY_LANGUAGE = "study_language", "Study or Language Package"
    FESTIVALS_EVENTS = "festivals_events", "Festivals or Events"
    SPORT = "sport", "Sport"
    FAMILY = "family", "Family"
    RELIGIOUS = "religious", "Religious"
    RELAX_HEALTH_SPAS = "relax_health_spas", "Relax, Health, and SPAs"
    ADVENTURE_NATURE = "adventure_nature", "Adventure, Nature, Eco-tourism"
    FOODIES_GASTRO_WINE = "foodies_gastro_wine", "Foodies - Gastro Tours - Wine Tours"
    SHOPPING = "shopping", "Shopping Tours"
    YOGA_MEDITATION = "yoga_meditation", "Yoga or Meditation"
    THEME_TOUR = "theme_tour", "Theme Tour (Urban Art, Architecture, Science, Cinema...)"
    PHOTO_TOURS = "photo_tours", "Photo Tours"
    CRUISES = "cruises", "Cruises"


class CurrencyChoices(models.TextChoices):
    CURRENCY = 'currency', 'Select currency'
    EUR = 'eur', 'EUR'
    USD = 'usd', 'USD'
    MXN = 'mxn', 'MXN'
    CHF = 'chf', 'CHF'
