from model import connect_to_db, db, User, Neighborhood, Service, FavPlace
import geoalchemy2

def query_from_address(address_location):
    """Finds which neighborhood an address is located in"""
    point1 = 'POINT(' + str(address_location['lng']) + " " + str(address_location['lat'])+ ')'

    point = geoalchemy2.elements.WKTElement(point1, srid=4326)

    neighborhood_item = db.session.query(Neighborhood).filter(Neighborhood.geom.ST_Contains(geoalchemy2.functions.ST_Transform(point, 4269))).one()

    return neighborhood_item