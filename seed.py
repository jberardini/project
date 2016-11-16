from model import Neighborhood
from model import Service

from model import connect_to_db, db
from server import app
import shapefile
# from geoalchemy2.types import Geometry
# from geoalchemy2.elements import WKTElement
import geoalchemy2.functions
import subprocess
# import os.subprocess

def load_neighborhoods():
    """Loads neighborhoods from neighborhoods.txt"""

    print "Neighborhoods"

    #prevents adding duplicate entries when the file is rerun
    Neighborhood.query.delete()
    
    # read file and insert data

    # sf = shapefile.Reader('neighborhoods.shp')

    # shapeRecs = sf.iterShapeRecords()
    # for shapeRec in shapeRecs:
    #     state = shapeRec.record[0]
    #     county = shapeRec.record[1]
    #     city = shapeRec.record[2]
    #     name = shapeRec.record[3]
    #     geom = shapeRec.shape.points
    #     neighborhood = Neighborhood(state=state, county=county,
    #                                 city=city, name=name,
    #                                 geom=geom)

    #     db.session.add(neighborhood)

    # p1=subprocess.Popen(['cmd', '/C', 'shp2pgsql', '-a' '-I' '-s 4269' 'neighborhoods.shp' 'neighborhoods_new'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # p2 = subprocess.Popen(['psql', '-U vagrant' '-d neighbor'], stdin=p1.stdout, 
    #     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # p1.stdout.close()
    # stdout, stderr= p2.communicate()
    # sf = shapefile.Reader('neighborhoods.shp')

    # records = sf.records()

    # for record in records:
    #     state, county, city, name, geom = record

        

    db.session.commit()

def load_services():
    """Loads services from services.txt"""

    print "Services"

    #prevents adding duplicate entries when the file is rerun
    Service.query.delete()

    #read file and insert data
    for row in open('seed_data/services.txt'):
        name, yelp_code, picture = row.rstrip().split("|")

        service = Service(name=name, yelp_code=yelp_code, picture=picture)

        db.session.add(service)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_neighborhoods()
    load_services()

