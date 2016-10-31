import requests
import os
import rauth


#hardcoding search parameters
payload = {}
# payload['term'] ='Pacific Heights'
payload['limit'] = 1
payload['sort'] = 0
payload['category_filter'] = 'grocery'
payload['location'] = 'Visitacion Valley, San Francisco, CA'
print payload

def get_results(payload):
    """Gets results from Yelp's API"""
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

    dry_cleaners = r.json()
    session.close()

    return dry_cleaners

dry_cleaners = get_results(payload)
print dry_cleaners['businesses'][0]['name']
print dry_cleaners['businesses'][0]['rating']
print dry_cleaners['businesses'][0]['url']