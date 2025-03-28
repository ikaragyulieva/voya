from django.db import models


class CityChoices(models.TextChoices):
    SELECT_CITY = '', 'Select a city'
    GENERIC_CITY = 'Generic', 'Generic city'
    NO_CITY = '-', '-'
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
    DUDLEY = 'Dudley', 'Dudley'
    LEICESTER = 'Leicester', 'Leicester'
    GENERIC = 'Generic city', 'Generic city'


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
    PRIVATE_BUS = 'Private bus', 'Private bus'
    PUBLIC_BUSES = 'Public buses', 'Public buses'
    TRAINS = 'Trains', 'Trains'
    FLIGHTS = 'Flights', 'Flights'
    TAXI = 'Taxi', 'Taxi'
    AIRPORT_STATION_TRANSFERS = 'Airport/Station transfers', 'Airport/Station transfers'
    NO_TRANSPORTATION = 'No transportation', 'No transportation'
    OTHER = 'Other', 'Other'


class PublicTransportationType(models.TextChoices):
    PUB_TRANSP = '', 'Select an option'
    PUBLIC_BUS = 'Public bus', 'Public bus'
    TRAIN = 'Train', 'Train'
    FLIGHTS = 'Flights', 'Flights'
    FERRY = 'Ferry', 'Ferry'
    METRO = 'Metro', 'Metro'
    OTHER = 'Other', 'Other'


class PrivateTransportationType(models.TextChoices):
    PR_TRANSP = '', 'Select an option'
    PRIVATE_BUS = 'Private bus', 'Private bus'
    PRIVATE_CAR = 'Private car', 'Private car'
    PRIVATE_VAN = 'Private van', 'Private van'
    PRIVATE_BOAT = 'Private boat', 'Private boat'
    LUXURY_CAR = 'Luxury car (4pax)', 'Luxury car (4 pax)'
    LUXURY_VAN = 'Luxury van (7pax)', 'Luxury van (7 pax)'
    LUXURY_BUS = 'Luxury bus (8+pax)', 'Luxury bus (8+ pax)'
    CHECK_POINT = 'Check point', 'Check point'
    DRIVER_ACCOMMODATION = 'Driver accommodation', 'Driver accommodation'
    DRIVER_MEALS = 'Driver meals', 'Driver meals'
    MOTORWAYS_PARKINGS = 'Motorways and parkings', 'Motorways and parkings'
    OTHER = 'Other', 'Other'


class AccommodationsType(models.TextChoices):
    ACC = 'acc', 'Select accommodations type'
    TWO_TREE_STAR_HOTELS = '2-3 Star hotels', '2-3 Star Hotels'
    TREE_FOUR_STAR_HOTELS = '3-4 Star hotels', '3-4 Star Hotels'
    FOUR_FIVE_STAR_HOTELS = '4-5 Star hotels', '4-5 Star Hotels'
    HOSTELS_WITH_PRIVATE_BATHROOM = 'Hostels with private bathroom', 'Hostels with private bathroom'
    APARTMENT = 'Apartment', 'Apartment'
    CAMPING = 'Camping', 'Camping'
    NONE = 'None', 'None -  I\'ll take care of it'
    OTHER = 'Other', 'Other'


class HotelType(models.TextChoices):
    ACC = '', 'Select an option'
    TWO_STAR_HOTEL = '2 Stars hotel', '2 Stars hotel'
    THREE_STAR_HOTEL = '3 Stars hotel', '3 Stars hotel'
    FOUR_STAR_HOTEL = '4 Stars hotel', '4 Stars hotel'
    FIVE_STAR_HOTEL = '5 Stars hotel', '5 Stars hotel'
    HOSTEL_WITH_PRIVATE_BATHROOM = 'Hostel private bathroom', 'Hostel with private bathroom'
    APARTMENT = 'Apartment', 'Apartment'
    CAMPING = 'Camping', 'Camping'


class MealsType(models.TextChoices):
    MEALS = 'Meal', 'Select meals service'
    BREAKFAST_ONLY = 'Breakfast only (BB)', 'Breakfast only (BB)'
    BREAKFAST_AND_DINNER = 'Breakfast & dinner (HB)', 'Breakfast & dinner (HB)'
    BREAKFAST_LUNCH_DINNER = 'Breakfast, lunch & dinner (FB)', 'Breakfast, lunch & dinner (FB)'
    NO_MEALS_INCLUDED = 'No meals included', 'No meals included'
    OTHER = 'Other', 'Other'


class StaffChoices(models.TextChoices):
    STAFF = 'staff', "Select staff service"
    TOUR_LEADER = 'Tour leader during the entire trip', 'Tour leader during the entire trip'
    OFFICIAL_TOURIST_GUIDES = 'Official tourist guides in each city'
    NO_NEED = 'No need', 'No staff needed'
    OTHER = 'Other', 'Other'


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
    VACATION = "vacation", "Vacation"


class CurrencyChoices(models.TextChoices):
    CURRENCY = '', 'Select an option'
    EUR = 'eur', 'EUR'
    USD = 'usd', 'USD'
    MXN = 'mxn', 'MXN'
    CHF = 'chf', 'CHF'


class ActivityTypeChoices(models.TextChoices):
    CHOICE = '', 'Select an option'
    TICKET = 'Ticket', 'Ticket'
    PACK = 'Pack', 'Package'
    OTHER = 'Other', 'Other'
