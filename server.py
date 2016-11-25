"""Welcome to the Neighborhood"""

# -*- coding: utf-8 -*-

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session, g
from model import connect_to_db, db, User, Neighborhood, Service, FavPlace
from flask_debugtoolbar import DebugToolbarExtension
from os import environ
from api_call import get_geocode, create_service_list
import json
import geoalchemy2
from sqlalchemy import and_
from db_queries import query_from_address, send_fav_to_db, get_rec_list, get_favs_info, get_favs_list

app = Flask(__name__)

app.secret_key = 'secret'
api_key = environ['GOOGLE_API_KEY']

app.jinja_env.undefined = StrictUndefined

JS_TESTING_MODE = False

@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE


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
    
    neighborhood_id = request.args.get('neighborhood_id')
    services = request.args.getlist('services[]')
    address = request.args.get('address')
    city = request.args.get('city')
    state = request.args.get('state')


    if address:
        address = '{}, {}, {}'.format(address, city, state)
        address_location = get_geocode(address, api_key)
        neighborhood_item = query_from_address(address_location)

    else:
        neighborhood_item = db.session.query(Neighborhood).filter(Neighborhood.neighborhood_id==neighborhood_id).one()

    neighborhood = '{}, {}, {}'.format(neighborhood_item.name,
                                       neighborhood_item.city,
                                       neighborhood_item.state)

    neighborhood_location = get_geocode(neighborhood, api_key)
    service_locations = create_service_list(services, neighborhood)
    coordinates = json.loads(db.session.scalar(geoalchemy2.functions.ST_AsGeoJSON(neighborhood_item.geom)))

    

    all_info = {'neighborhood': neighborhood_location, 
                'services': service_locations,
                'name': neighborhood,
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

    send_fav_to_db(neighborhood_name, city, name, user_id, service_id, url, lat, lng)    
    
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

    favs = get_favs_list(user)
    recs = get_rec_list(favs)


    fav_place_info = get_favs_info(favs)
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
    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app) 
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
