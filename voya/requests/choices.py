from django.db import models


class CityChoices(models.TextChoices):
    SELECT_CITY = '', 'Select a city'
    AMSTERDAM = 'Amsterdam', 'Amsterdam'
    ATHENS = 'Athens', 'Athens'
    ÁVILA = 'Ávila', 'Ávila'
    BARCELONA = 'Barcelona', 'Barcelona'
    BELGRADE = 'Belgrade', 'Belgrade'
    BERLIN = 'Berlin', 'Berlin'
    BOLOGNA = 'Bologna', 'Bologna'
    BORDEAUX = 'Bordeaux', 'Bordeaux'
    BOURGES = 'Bourges', 'Bourges'
    BRUGES = 'Bruges', 'Bruges'
    BRUSSELS = 'Brussels', 'Brussels'
    BUDAPEST = 'Budapest', 'Budapest'
    CAPPADOCIA = 'Cappadocia', 'Cappadocia'
    CAPRI = 'Capri', 'Capri'
    CHAMONIX = 'Chamonix', 'Chamonix'
    CINQUE_TERRE = 'Cinque Terre', 'Cinque Terre'
    COIRA_CHUR = 'Coira/Chur', 'Coira/Chur'
    COLMAR = 'Colmar', 'Colmar'
    COMO = 'Como', 'Como'
    COPENHAGEN = 'Copenhagen', 'Copenhagen'
    CRACOW = 'Cracow', 'Cracow'
    DUBLIN = 'Dublin', 'Dublin'
    DUBROVNIK = 'Dubrovnik', 'Dubrovnik'
    EDINBURGH = 'Edinburgh', 'Edinburgh'
    FÁTIMA = 'Fátima', 'Fátima'
    FLORENCE = 'Florence', 'Florence'
    FRANKFURT = 'Frankfurt', 'Frankfurt'
    GARBAGNATE_MILANESE = 'Garbagnate Milanese', 'Garbagnate Milanese'
    GENEVA = 'Geneva', 'Geneva'
    GHENT = 'Ghent', 'Ghent'
    GLASGOW = 'Glasgow', 'Glasgow'
    GOTHENBURG = 'Gothenburg', 'Gothenburg'
    HARROGATE = 'Harrogate', 'Harrogate'
    HELSINKI = 'Helsinki', 'Helsinki'
    HIGHLANDS = 'Highlands', 'Highlands'
    HVAR = 'Hvar', 'Hvar'
    IBIZA = 'Ibiza', 'Ibiza'
    ISTANBUL = 'Istanbul', 'Istanbul'
    LISBON = 'Lisbon', 'Lisbon'
    LISIEUX = 'Lisieux', 'Lisieux'
    LIVERPOOL = 'Liverpool', 'Liverpool'
    LOIRE = 'Loire', 'Loire'
    LONDON = 'London', 'London'
    LOURDES = 'Lourdes', 'Lourdes'
    LUCERNE = 'Lucerne', 'Lucerne'
    LYON = 'Lyon', 'Lyon'
    MADRID = 'Madrid', 'Madrid'
    MILAN = 'Milan', 'Milan'
    MONTECATINI_TERME = 'Montecatini Terme', 'Montecatini Terme'
    MONTSERRAT = 'Montserrat', 'Montserrat'
    MOSCOW = 'Moscow', 'Moscow'
    MUNICH = 'Munich', 'Munich'
    MYKONOS = 'Mykonos', 'Mykonos'
    NAPLES = 'Naples', 'Naples'
    NUREMBERG = 'Nuremberg', 'Nuremberg'
    NICE = 'Nice', 'Nice'
    OPORTO = 'Oporto', 'Oporto'
    OSLO = 'Oslo', 'Oslo'
    PAMPLONA = 'Pamplona', 'Pamplona'
    PARIS = 'Paris', 'Paris'
    PRAGUE = 'Prague', 'Prague'
    PISA = 'Pisa', 'Pisa'
    REYKJAVIK = 'Reykjavik', 'Reykjavik'
    ROME = 'Rome', 'Rome'
    SALZBURG = 'Salzburg', 'Salzburg'
    SANTIAGO_DE_COMPOSTELA = 'Santiago de Compostela', 'Santiago de Compostela'
    SANTORINI = 'Santorini', 'Santorini'
    SEVILLE = 'Seville', 'Seville'
    SOFIA = 'Sofia', 'Sofia'
    SPLIT = 'Split', 'Split'
    STOCKHOLM = 'Stockholm', 'Stockholm'
    VARNA = 'Varna', 'Varna'
    VENICE = 'Venice', 'Venice'
    VIENNA = 'Vienna', 'Vienna'
    VINCI = 'Vinci', 'Vinci'
    WARSAW = 'Warsaw', 'Warsaw'
    ZAGREB = 'Zagreb', 'Zagreb'
    ZARAGOZA = 'Zaragoza', 'Zaragoza'
    ZURICH = 'Zurich', 'Zurich'
    REIMS = 'Reims', 'Reims'
    GRENOBLE = 'Grenoble', 'Grenoble'
    JEREZ_DE_LA_FRONTERA = 'Jerez de la Frontera', 'Jerez de la Frontera'
    CHEFCHAOUEN = 'Chefchaouen', 'Chefchaouen'
    FEZ = 'Fez', 'Fez'
    RABAT = 'Rabat', 'Rabat'
    TANGER = 'Tanger', 'Tanger'
    TARRAGONA = 'Tarragona', 'Tarragona'




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
    CHOOSE_COUNTRY = '', 'Select country'
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
    SCOTLAND = 'Scotland', 'Scotland'
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
    TRANSPORT = '', 'Select an option'
    NO_TRANSPORTATION = 'no transportation', 'No transportation - I\'ll take care of it'
    PRIVATE_BUS = 'private bus', 'Private Bus'
    PUBLIC_BUSES = 'public buses', 'Public Buses'
    TRAINS = 'trains', 'Trains'
    FLIGHTS = 'flights', 'Flights'
    TAXI = 'taxi', 'Taxi'
    AIRPORT_STATION_TRANSFERS = 'airport/station transfers', 'Airport/Station Transfers'


class PublicTransportationType(models.TextChoices):
    PUB_TRANSP = '', 'Select an option'
    PUBLIC_BUS = 'public bus', 'Public Bus'
    TRAIN = 'train', 'Train'
    FLIGHTS = 'flights', 'Flights'
    FERRY = 'ferry', 'Ferry'
    METRO = 'metro', 'Metro'
    OTHER = 'other', 'Other'


class PrivateTransportationType(models.TextChoices):
    PR_TRANSP = '', 'Select an option'
    PRIVATE_BUS = 'private bus', 'Private bus'
    PRIVATE_CAR = 'private car', 'Private car'
    PRIVATE_VAN = 'private van', 'Private van'
    PRIVATE_BOAT = 'private boat', 'Private boat'
    LUXURY_CAR = 'luxury car (4pax)', 'Luxury car (4 pax)'
    LUXURY_VAN = 'luxury van (7pax)', 'Luxury van (7 pax)'
    LUXURY_BUS = 'luxury bus (8+pax)', 'Luxury bus (8+ pax)'

    OTHER = 'other', 'Other'


class AccommodationsType(models.TextChoices):
    ACC = 'acc', 'Select accommodations type'
    NONE = 'none', 'None -  I\'ll take care of it'
    TWO_TREE_STAR_HOTELS = '2-3 star hotels', '2-3 Star Hotels'
    FOUR_FIVE_STAR_HOTELS = '4-5 star hotels', '4-5 Star Hotels'
    HOSTELS_WITH_PRIVATE_BATHROOM = 'hostels with private bathroom', 'Hostels with private bathroom'
    APARTMENT = 'apartment', 'Apartment'
    CAMPING = 'camping', 'Camping'


class HotelType(models.TextChoices):
    ACC = '', 'Select an option'
    TWO_STAR_HOTEL = '2 star hotel', '2 Stars hotel'
    THREE_STAR_HOTEL = '3 star hotel', '3 Stars hotel'
    FOUR_STAR_HOTEL = '4 star hotel', '4 Stars hotel'
    FIVE_STAR_HOTEL = '5 star hotel', '5 Stars hotel'
    HOSTEL_WITH_PRIVATE_BATHROOM = 'hostel private bathroom', 'Hostel with private bathroom'
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
    CURRENCY = '', 'Select an option'
    EUR = 'eur', 'EUR'
    USD = 'usd', 'USD'
    MXN = 'mxn', 'MXN'
    CHF = 'chf', 'CHF'


class ActivityTypeChoices(models.TextChoices):
    CHOICE = '', 'Select an option'
    TICKET = 'ticket', 'Ticket'
    PACK = 'pack', 'Package'
    OTHER = 'other', 'Other'
