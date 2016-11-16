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
    user_neighborhood = db.Column(db.String(100))

    def __repr__(self):
        """Provides a representation of users"""

        return '<User user_id = {} email = {} neighborhood = {}>'.format(self.user_id,
                                                                         self.email,
                                                                         self.user_neighborhood)

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
    geom = db.Column(Geometry('MULTIPOLYGON', srid=4269), nullable=False)

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

def connect_to_db(app):
    """Connect the database to Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///neighbor'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

