# Public Contract: given a city name as an argument, this module will return the abbreviated state or site name for the city in question

# TO-DO: set up an alert mechanism that will handle cities that aren't in the 'cities' list
# TO-DO: configure so that city names are not case-sensitive


import settings

cities = {"NEW CASTLE": "DE", "WINTHROP": "ME", "BALTIMORE": "HQ", "DURHAM": "HQ", "Columbus": "OH", "ROANOKE": "VA", "PROVIDENCE": "RI",
          "HENRICO": "VA", "DES MOINES": "IA", "WOODLAWN": "HQ", "SIOUX FALLS": "SD", "TUMWATER": "WA", "Federal Way": "WA", "WASHINGTON": "DC", "LINCOLN": "NE", "error": "??"}

site_id = {"NEW CASTLE": "S09", "WINTHROP": "S22", "BALTIMORE": "Z25", "DURHAM": "L1V", "Columbus": "S38", "ROANOKE": "S10", "PROVIDENCE": "S44",
          "HENRICO": "S88", "DES MOINES": "S18", "WOODLAWN": "Z25", "SIOUX FALLS": "S47", "TUMWATER": "S54", "Federal Way": "V23", "WASHINGTON": "S11", "LINCOLN": "S30", "error": "??"}


def city_to_site(cityname):
    for city, site in cities.items():
        if city == cityname:
            settings.site = site
            # print(settings.site)


def city_to_site_id(cityname):
    for city, site in site_id.items():
        if city == cityname:
            settings.site = site
        elif site == cityname:
            settings.site = site
            # print(settings.site)


def site_id_to_state(cityname):
    for city, site in site_id.items():
        if site == cityname:
            settings.city = city
            # print(settings.city)
            for city, state in cities.items():
                if settings.city ==  city:
                    settings.state = state
                    # print(settings.state)