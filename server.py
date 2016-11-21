"""Welcome to the Neighborhood"""

# -*- coding: utf-8 -*-

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from model import connect_to_db, db, User, Neighborhood, Service, FavPlace
from flask_debugtoolbar import DebugToolbarExtension
from os import environ
from api_call import get_geocode, create_service_list
import json
import geoalchemy2
from sqlalchemy import and_
from db_queries import query_from_address

app = Flask(__name__)

app.secret_key = 'secret'
api_key = environ['GOOGLE_API_KEY']

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""

    neighborhoods = db.session.query(Neighborhood).all()
    services = db.session.query(Service).all()

    return render_template('homepage.html', neighborhoods=neighborhoods,
                           services=services, api_key=api_key)


@app.route('/info.json')
def get_yelp_info():
    "Gets info from yelp and geocode info from Google"
    
    neighborhood = request.args.get('neighborhood')
    services = request.args.getlist('services[]')
    address = request.args.get('address')


    if address:
        address_location = get_geocode(address, api_key)
        neighborhood_item = query_from_address(address_location)
        neighborhood = "{}, {}, {}".format(neighborhood_item.name, 
                                           neighborhood_item.city, 
                                           neighborhood_item.state)



    else:
        name, city, state = neighborhood.split(', ')
        neighborhood_item = db.session.query(Neighborhood).filter(and_(Neighborhood.name==name, Neighborhood.city==city)).one()

    neighborhood_location = get_geocode(neighborhood, api_key)
    service_locations = create_service_list(services, neighborhood)
    coordinates = json.loads(db.session.scalar(geoalchemy2.functions.ST_AsGeoJSON(neighborhood_item.geom)))

    all_info = {'neighborhood': neighborhood_location, 
                'services': service_locations,
                'name': neighborhood_item.name,
                'coordinates': {
                    'type': 'FeatureCollection', 
                    'features': [
                        {'type': 'Feature',     
                         'geometry': coordinates
                        }]
                    }
                }
    

    return jsonify(all_info)


@app.route('/set_favorite')
def set_favorite():
    """Gets user favorite and adds to db"""

    user_id = session['user_id']
    service_id = request.args.get('service_id', 0, type=int)
    name = request.args.get('name', 0, type=str)
    neighborhood = request.args.get('neighborhood', 0, type=str)
    url = request.args.get('url', 0, type=str)
    lat = request.args.get('lat', 0, type=float)
    lng = request.args.get('lng', 0, type=float)

    neighborhood_name, city, state = neighborhood.split(', ')

    neighborhood=db.session.query(Neighborhood).filter_by(name=neighborhood_name, city=city).one()
    place_search = db.session.query(FavPlace).filter_by(name=name).all()

    if not place_search:
        new_fav_place = FavPlace(name=name, user_id=user_id, service_id=service_id, 
                                 neighborhood_id=neighborhood.neighborhood_id, url=url,
                                 lat=lat, lng=lng)
        db.session.add(new_fav_place)
    else:
        place = place_search[0]
        db.session.delete(place)
    db.session.commit() 
    
    data = jsonify('Added to favorite places')
    return data


@app.route('/user/<user_id>')
def show_user_page(user_id):
    """Show's the user's page, with favorite places"""


    return render_template('user_info.html', api_key=api_key)


@app.route('/fav.json')
def get_fav_place_info():
    """Gets info about fav places from Yelp's API"""

    user_id=session['user_id']
    user = db.session.query(User).filter_by(user_id=user_id).one()
    neighborhood = "{}, {}, {}".format(user.neighborhood.name, user.neighborhood.city,user.neighborhood.state)
    coordinates = json.loads(db.session.scalar(geoalchemy2.functions.ST_AsGeoJSON(user.neighborhood.geom)))



    fav_places = user.fav_places
    service_ids = []
    fav_place_info={}
    for fav_place in fav_places:
        service_ids.append(fav_place.service_id)
        fav_place_info[fav_place.name]={'url': fav_place.url,
                                        'lat': fav_place.lat,
                                        'lng': fav_place.lng,
                                        'picture': fav_place.service.picture}


    services = db.session.query(Service).all()
    all_service_ids = []
    for service in services:
        all_service_ids.append(service.service_id)
    
    recs = set(all_service_ids) ^ set(service_ids)
    
    neighborhood_location = get_geocode(neighborhood, api_key)
    recs_info = create_service_list(recs, neighborhood)

    important_info = {'neighborhood': neighborhood_location,
                      'neighborhood_name': neighborhood, 
                      'fav_places': fav_place_info,
                      'recs': recs_info,
                      'coordinates': {
                          'type': 'FeatureCollection', 
                          'features': [
                              {'type': 'Feature',     
                               'geometry': coordinates
                              }]
                          }}


    return jsonify(important_info)


@app.route('/login')
def log_in():
    """Allows user to log in"""

    return render_template('log-in.html', api_key=api_key)

@app.route('/logged-in', methods=['POST'])
def process_login():
    """Processes user-inputted log-in information"""

    email = request.form.get('email')
    password = request.form.get('password')
    user = db.session.query(User).filter_by(email=email).one()

    if user:
        if user.password == password:
            session['user_id'] = user.user_id
            flash('You are now logged in.')
            return redirect('/user/' + str(user.user_id))
        else:
            flash('Your password is incorrect.')
            return redirect('/login')
    else:
        flash('We didn\'t find an account that matches that email. Sign up below')
        return redirect('/sign-up')


@app.route('/logged-out')
def process_logout():
    """Logs user out"""

    del session['user_id']
    flash('You have been logged out.')
    return redirect('/')


@app.route('/sign-up')
def sign_up():
    """Allows user to register for an account"""

    neighborhoods = db.session.query(Neighborhood).all()

    return render_template('sign-up.html', neighborhoods=neighborhoods, api_key=api_key)


@app.route('/process-signup', methods=['POST'])
def process_sign_up():
    """Processes new user sign-up"""

    email = request.form.get('email')
    password = request.form.get('password')
    user_neighborhood = request.form.get('neighborhood')
    name, city, state = user_neighborhood.split(', ')

    neighborhood_id = db.session.query(Neighborhood.neighborhood_id).filter(and_(Neighborhood.name==name, Neighborhood.city==city)).one()
    print neighborhood_id
    user = db.session.query(User).filter_by(email=email).all()


    if not user:
        new_user = User(email=email, password=password, neighborhood_id=neighborhood_id)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created. Please log in.')
        return redirect('/login')
    else:
        flash('There is already an account associated with that email')
        return redirect('/sign-up')


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app) 
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
