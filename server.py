"""Welcome to the Neighborhood"""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session

from model import connect_to_db, db, User, Neighborhood, Service, FavPlace

app = Flask(__name__)

app.secret_key = 'secret'

@app.route('/')
def index():
    """Homepage"""

    return render_template('homepage.html')

@app.route('/neighborhood-map')
def show_map():
    """Shows a map of the user's neighborhood with highlighted services"""

    return render_template('neighborhood.html')

@app.route('/user/<user_id>')
def show_user_page(user_id):
    """Show's the user's page, with favorite places"""

    return render_template('user_info.html')

@app.route('/login')
def log_in():
    """Allows user to log in"""

    return render_template('log-in.html')

@app.route('/logged-in')
def process_login():
    """Processes user-inputted log-in information"""

    # email = request.form.get('email')
    # user = db.session.query(User).filter_by(email=email)

    return redirect('/')

@app.route('/logged-out')
def process_logout():
    """Logs user out"""

    return redirect('/')