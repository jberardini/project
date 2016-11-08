import requests
from os import environ
from rauth import OAuth1Session
from model import connect_to_db, db, User, Neighborhood, Service, FavPlace

# def format_neighborhood(neighborhood):
#     """Formats neighborhood name for API call"""

#     neighborhood = "{}, San Francisco, CA".format(neighborhood)
#     return neighborhood


def get_neighborhood(neighborhood, api_key):
    """Gets approximate neighborhood location from Google's Geocode API"""

    payload = {'address': neighborhood, 'key': api_key}
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', 
                     params=payload)

    neighborhood_info = r.json()

    coordinates = neighborhood_info['results'][0]['geometry']['location']
    
    return coordinates

def get_yelp_code(service_id):
    """Gets code for yelp query from database"""

    service = db.session.query(Service).filter_by(service_id=service_id).one()
    yelp_code = service.yelp_code

    return yelp_code

def get_picture(service_id):
    """Gets picture url from database"""

    service = db.session.query(Service).filter_by(service_id=service_id).one()
    picture = service.picture

    return picture

def make_yelp_call(location, category_filter="", term=""):
    """Gets information from Yelp's API"""

    payload = {'limit': 1, 'sort': 0, 'category_filter': category_filter,
              'location': location, 'term': term}

    consumer_key=environ['YELP_CONSUMER_KEY']
    consumer_secret=environ['YELP_CONSUMER_SECRET']
    access_token_key=environ['YELP_ACCESS_TOKEN_KEY']
    access_token_secret=environ['YELP_ACCESS_TOKEN_SECRET']

    session = OAuth1Session(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = access_token_key,
        access_token_secret = access_token_secret)

    r = session.get('http://api.yelp.com/v2/search', 
                    params=payload)

    yelp_info = r.json()
    session.close()
    return yelp_info


def create_service_list(service_ids, neighborhood):
    """Loops through each service requested and adds the result to a dictionary"""

    services = {}
    for service_id in service_ids:
        service_code = get_yelp_code(service_id)
        picture = get_picture(service_id)
        yelp_info = make_yelp_call(category_filter=service_code, 
                                      location=neighborhood)
        lat =  yelp_info['businesses'][0]['location']['coordinate']['latitude']
        lng = yelp_info['businesses'][0]['location']['coordinate']['longitude']
        name = yelp_info['businesses'][0]['name']
        url = yelp_info['businesses'][0]['url']

        display_info = {'name': name, 'url': url, 'lat': lat, 
                        'lng': lng, 'picture': picture}

        services[service_id] = display_info

    return services

def get_fav_places(user_id, neighborhood):
    """Gets fav places from Yelp's API"""
    
    user = db.session.query(User).filter_by(user_id=user_id).one()
    fav_places = user.fav_places
    fav_place_info={}
    for fav_place in fav_places:
        yelp_info = make_yelp_call(location=neighborhood, term=fav_place.name)
        lat = yelp_info['businesses'][0]['location']['coordinate']['latitude']
        lng = yelp_info['businesses'][0]['location']['coordinate']['longitude']
        url = yelp_info['businesses'][0]['url']
        picture = fav_place.service.picture

        fav_place_info[fav_place.name] = {'url': url, 'lat': lat, 'lng': lng, 
                                          'picture': picture}

    return fav_place_info
