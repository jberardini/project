"""Welcome to the Neighborhood"""

# -*- coding: utf-8 -*-

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session

from model import connect_to_db, db, User, Neighborhood, Service, FavPlace
from flask_debugtoolbar import DebugToolbarExtension
import os
from api_call import format_neighborhood, create_service_list, get_neighborhood
import json

app = Flask(__name__)

app.secret_key = 'secret'

@app.route('/')
def index():
    """Homepage"""

    neighborhoods = db.session.query(Neighborhood).all()
    services = db.session.query(Service).all()

    return render_template('homepage.html', neighborhoods=neighborhoods,
                           services=services)


@app.route('/neighborhood-map')
def show_map():
    """Shows a map of the user's neighborhood with highlighted services"""

    neighborhood = request.args.get('neighborhood')
    service_ids = request.args.getlist('service')
    neighborhood = format_neighborhood(neighborhood)

    session['neighborhood'] = neighborhood
    session['service_ids'] = service_ids
    api_key=os.environ['GOOGLE_API_KEY']
    print api_key

    return render_template('neighborhood.html', api_key=api_key)

@app.route('/info.json')
def get_yelp_info():
    "Gets info from yelp and geocode info from Google"
    neighborhood = session['neighborhood']
    service_ids = session['service_ids']
    api_key=os.environ['GOOGLE_API_KEY']

    neighborhood_location = get_neighborhood(neighborhood, api_key)
    service_locations = create_service_list(service_ids, neighborhood)
    all_info = {'neighborhood': neighborhood_location, 
                'services': service_locations}
    
    return jsonify(all_info)

@app.route('/set_favorite')
def set_favorite():
    service_id = request.args.get('service_id', 0, type=int)
    name = request.args.get('name', 0, type=str)
    full_neighborhood = session['neighborhood'].split(',')
    neighborhood_name = full_neighborhood[0]
    neighborhood=db.session.query(Neighborhood).filter_by(name=neighborhood_name).one()
    user_id = session['user_id']

    place_search = db.session.query(FavPlace).filter_by(name=name).all()
    if not place_search:
        new_fav_place = FavPlace(name=name, user_id=user_id, service_id=service_id, 
                             neighborhood_id=neighborhood.neighborhood_id)
        db.session.add(new_fav_place)
    else:
        place = place_search[0]
        db.session.delete(place)
    db.session.commit() 
    
    data = jsonify('Added to favorite places')
    # what the server returns is what the js is going to receive as "data"
    return data

@app.route('/user/<user_id>')
def show_user_page(user_id):
    """Show's the user's page, with favorite places"""

    user = db.session.query(User).filter_by(user_id=user_id).one()
    fav_places = user.fav_places
    print user.fav_places

    api_key=os.environ['GOOGLE_API_KEY']

    return render_template('user_info.html', user=user, api_key=api_key,
                            fav_places=fav_places)

@app.route('/login')
def log_in():
    """Allows user to log in"""

    return render_template('log-in.html')

@app.route('/logged-in', methods=['POST'])
def process_login():
    """Processes user-inputted log-in information"""

    email = request.form.get('email')
    password = request.form.get('password')
    user = db.session.query(User).filter_by(email=email).all()

    if user:
        if user[0].password == password:
            session['user_id'] = user[0].user_id
            flash('You are now logged in.')
            return redirect('/user/'+ str(user[0].user_id))
        else:
            flash('Invalid credentials.')
            return redirect('/login')
    else:
        flash('We didn\'t find an account that matches that email. Sign up below')
        return redirect('/sign-up')

@app.route('/logged-out')
def process_logout():
    """Logs user out"""
    del session['user_id']
    return redirect('/')

@app.route('/sign-up')
def sign_up():
    """Allows user to register for an account"""

    return render_template('sign-up.html')

@app.route('/process-signup', methods=['POST'])
def process_sign_up():
    """Processes new user sign-up"""

    email = request.form.get('email')
    password = request.form.get('password')
    user = db.session.query(User).filter_by(email=email).all()

    if not user:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created. Please log in.')
        return redirect('/login')
    else:
        flash('There is already an account associated with that email')
        return redirect('/sign-up')

# @app.route('/add-to-favorites', methods=['POST'])
# def add_to_favorites():


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app) 
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
