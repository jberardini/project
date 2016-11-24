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


def get_favs_list(user):
    """Gets a user's favorite places"""

    fav_places = user.fav_places

    return fav_places


def get_rec_list(fav_places):
    "Returns a list of services to recommend"


    service_ids = []

    for fav_place in fav_places:
        service_ids.append(fav_place.service_id)

    services = db.session.query(Service).all()

    all_service_ids = []

    for service in services:
        all_service_ids.append(service.service_id)
    
    recs = set(all_service_ids) ^ set(service_ids)

    return recs

def get_favs_info(favs_list):
    """Returns a list of information about favorite places"""

    fav_place_info={}

    for fav_place in favs_list:
        fav_place_info[fav_place.name]={'url': fav_place.url,
                                        'lat': fav_place.lat,
                                        'lng': fav_place.lng,
                                        'picture': fav_place.service.picture}

    return fav_place_info