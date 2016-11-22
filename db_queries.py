from model import connect_to_db, db, User, Neighborhood, Service, FavPlace
import geoalchemy2

def query_from_address(address_location):
    """Finds which neighborhood an address is located in"""
    point1 = 'POINT(' + str(address_location['lng']) + " " + str(address_location['lat'])+ ')'

    point = geoalchemy2.elements.WKTElement(point1, srid=4326)

    neighborhood_item = db.session.query(Neighborhood).filter(Neighborhood.geom.ST_Contains(geoalchemy2.functions.ST_Transform(point, 4269))).one()

    return neighborhood_item


def send_fav_to_db(neighborhood_name, city, name, user_id, service_id, url, lat, lng):
    """Adds or removes favorite from database"""
    
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