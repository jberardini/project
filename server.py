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
    neighborhood_location = get_neighborhood(neighborhood)
    service_locations = create_service_list(service_ids, neighborhood)
    print service_locations

    api_key=os.environ['GOOGLE_API_KEY']


    return render_template('neighborhood.html', neighborhood_location=neighborhood_location, 
                           service_locations=json.dumps(service_locations), api_key=api_key)

@app.route('/user/<user_id>')
def show_user_page(user_id):
    """Show's the user's page, with favorite places"""

    return render_template('user_info.html')

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



if __name__ == "__main__":
    app.debug = True
    connect_to_db(app) 
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")