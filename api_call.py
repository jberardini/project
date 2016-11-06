import requests
import os
import rauth
import requests
from model import connect_to_db, db, User, Neighborhood, Service, FavPlace

def format_neighborhood(neighborhood):
    """Formats neighborhood name for API call"""
    neighborhood = "{}, San Francisco, CA".format(neighborhood)
    return neighborhood


def get_neighborhood(neighborhood, api_key):
    """Gets approximate neighborhood location from Google's Geocode API"""
    payload = {'address': neighborhood, 'key': api_key}
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', 
                     params=payload)

    neighborhood_info = r.json()

    print neighborhood_info
    coordinates = neighborhood_info['results'][0]['geometry']['location']
    
    return coordinates


def get_service(service_id, neighborhood):
    """Gets services from Yelp's API"""
    service = db.session.query(Service).filter_by(service_id=service_id).one()
    print service.yelp_code

    payload = {'limit': 1, 'sort': 0, 'category_filter': service.yelp_code,
              'location': neighborhood}
    print payload

    consumer_key=os.environ['YELP_CONSUMER_KEY']
    consumer_secret=os.environ['YELP_CONSUMER_SECRET']
    access_token_key=os.environ['YELP_ACCESS_TOKEN_KEY']
    access_token_secret=os.environ['YELP_ACCESS_TOKEN_SECRET']

    session = rauth.OAuth1Session(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = access_token_key,
        access_token_secret = access_token_secret)

    r = session.get('http://api.yelp.com/v2/search', 
                          params=payload)

    service_info = r.json()
    session.close()
    print service_info
    lat_long =  service_info['businesses'][0]['location']['coordinate']
    name =  service_info['businesses'][0]['name']
    url = service_info['businesses'][0]['url']

    display_info = {'name': name, 'url': url, 'lat': lat_long['latitude'], 
                   'lng': lat_long['longitude'], 'picture': service.picture}

    return display_info

def create_service_list(service_ids, neighborhood):
    """Loops through each service requested and adds the result to a dictionary"""

    services = {}
    for service_id in service_ids:
        display_info = get_service(service_id, neighborhood)
        services[service_id] = display_info

    return services