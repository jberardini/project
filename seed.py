from model import Neighborhood
from model import Service

from model import connect_to_db, db
from server import app

def load_neighborhoods():
    """Loads neighborhoods from neighborhoods.txt"""

    print "Neighborhoods"

    #prevents adding duplicate entries when the file is rerun
    Neighborhood.query.delete()

    #read file and insert data
    for row in open('seed_data/neighborhoods.txt'):
        name = row.rstrip()

        neighborhood = Neighborhood(name=name)

        db.session.add(neighborhood)

    db.session.commit()

def load_services():
    """Loads services from services.txt"""

    print "Services"

    #prevents adding duplicate entries when the file is rerun
    Service.query.delete()

    #read file and insert data
    for row in open('seed_data/services.txt'):
        name, yelp_code = row.rstrip().split("| ")

        service = Service(name=name, yelp_code=yelp_code)

        db.session.add(service)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_neighborhoods()
    load_services()

