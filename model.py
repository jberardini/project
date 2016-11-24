from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.types import Geometry

db = SQLAlchemy()

#####################################################
# Model definitions

class User(db.Model):
    """User of site"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, 
                        primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64))
    address = db.Column(db.String(100))
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'))

    neighborhood = db.relationship('Neighborhood', backref=db.backref('users', 
                                                                      order_by=user_id))

    def __repr__(self):
        """Provides a representation of users"""

        return '<User user_id = {} email = {}>'.format(self.user_id, self.email)

class Neighborhood(db.Model):
    """Neighborhoods in the Bay Area"""

    __tablename__ = 'neighborhoods'

    neighborhood_id = db.Column(db.Integer, autoincrement=True,
                                primary_key=True)

    state = db.Column(db.String(2), nullable=False)
    county = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    regionid = db.Column(db.Integer)
    geom = db.Column(Geometry('MULTIPOLYGON', srid=4269), nullable=True)

    def __repr__(self):
        """Provides a representation of neighborhoods"""

        return '<Neighborhood neighborhood_id = {} name = {}>'.format(self.neighborhood_id,
                                                                     self.name)


class Service(db.Model):
    """Services a user can search for"""

    __tablename__ = 'services'

    service_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    yelp_code = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        """Provides a representation of services"""

        return '<Service service_id = {} name = {}>'.format(self.service_id,
                                                           self.name)

class FavPlace(db.Model):
    """User-favorited places"""

    __tablename__='fav_places'

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.neighborhood_id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))
    url = db.Column(db.String(500), nullable = False)
    lat = db.Column(db.Float, nullable = False)
    lng = db.Column(db.Float, nullable = False)


    user = db.relationship('User', backref=db.backref('fav_places', order_by=place_id))
    neighborhood = db.relationship('Neighborhood', backref=db.backref('fav_places', 
                                                                      order_by=place_id))
    service = db.relationship('Service', backref=db.backref('fav_places', 
                                                         order_by=place_id))

    def __repr__(self):
        """Provides a representation of favorite places"""

        return '<FavPlace place_id = {} name = {}>'.format(self.place_id,
                                                          self.name)

######################################################################
# Helper functions

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Neighborhood.query.delete()
    Service.query.delete()


    # Add sample employees and departments
    mission = Neighborhood(state='CA', county='San Francisco', city='San Francisco', name='Mission')
    pacheights = Neighborhood(state='CA', county='San Francisco', city='San Francisco', name='Pacific Heights')
    castro = Neighborhood(state='CA', county='San Francisco', city='San Francisco', name='Castro')

    hair_salon = Service(yelp_code='hair', name='hair salon', picture='static/img/hair-salon.png')
    dry_cleaning = Service(yelp_code='drycleaninglaundry', name='dry-cleaning and laundry', picture='static/img/drycleaning.png')
    doctor = Service(yelp_code='physicians', name='doctor', picture='static/img/doctor.png')
    nail_salon = Service(yelp_code='othersalons', name='nail salon', picture='static/img/nail-salon.png')

    jill = User(email='jill@gmail.com', password='easy', first_name='Jill', neighborhood_id=1)


    new_favorite = FavPlace(name='Jill\'s World', user_id=1, neighborhood_id=1, service_id=1, 
                            url='jillsworld.com', lat= 37, lng = -122)

    db.session.add_all([mission, pacheights, castro, hair_salon, dry_cleaning, doctor, nail_salon, jill, new_favorite])
    db.session.commit()



def connect_to_db(app, db_uri='postgresql:///neighbor'):
    """Connect the database to Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

