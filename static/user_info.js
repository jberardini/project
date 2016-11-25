'use strict';
var map;

function createSuggestedElement(rec, rec_info, results) {
  // creating html element
  var $li = $("<li></li>");
  var $img = $("<img></img><div class=space></div>");
  var $a = $("<a target=_blank></a>")
  var $button = $('<button></button>');
  var name = rec_info.name 
  var imgUrl =  '/../' + rec_info.picture;

  //setting attributes of html element
  $img.attr('src', imgUrl);
  $a.html("  "+rec_info.name+"  ")
  $a.attr('href', rec_info.url)
  $button.html('add to favorites')

  // adds a new marker on the map
  $button.on('click', function() {
     var position = new google.maps.LatLng(rec_info.lat, rec_info.lng);
     var marker = new google.maps.Marker({
        position: position,
        map: map,
        icon: imgUrl,
      });

    var infoWindow = new google.maps.InfoWindow({width: 150});
    var windowhtml = createInfoWindow(rec_info.name, rec_info.url)

    infoWindow.setContent(windowhtml);

    bindFavInfoWindow(marker, map, infoWindow);

    $.get('/set_favorite', {'service_id': rec, 'name': rec_info.name,
                            'neighborhood': results.neighborhood_name,
                            'url': rec_info.url, 'lat': rec_info.lat,
                            'lng': rec_info.lng }, function() {
                              console.log('Success!')
                            });
  });

  $li.append($img);
  $li.append($a);
  $li.append($button);
  return $li;
}


var prevInfoWindow=false;

function bindFavInfoWindow(marker, map, infoWindow) {
 google.maps.event.addListener(marker, 'click', function() {
   if (prevInfoWindow) {
      prevInfoWindow.close();
   }
   prevInfoWindow = infoWindow;
   infoWindow.open(map, marker);
  });
}

function createInfoWindow(name, url) {
  var $windowhtml = $("<div></div>");
  var $bname = $("<p></p>");
  var $url = $("<a target=_blank>Visit website</a>");
  $bname.html(name);
  $url.attr('href', url);
  $windowhtml.append($bname);
  $windowhtml.append($url);
  return $windowhtml.html();
}


function initMap() {
  $.get('/fav.json',  function (results) {
    var center = results.neighborhood;
    map = new google.maps.Map(document.getElementById('favs_map'), {
      center: center,
      zoom: 15
    });

    if (jQuery.isEmptyObject(results.fav_places)) {
      $('#fav_places').append('<li> You do not have any favorite places</li>');
    }

    for (var key in results.fav_places) {
      var service = results.fav_places[key];
      var position = new google.maps.LatLng(service.lat, service.lng);
      var image = "/../"+ service.picture
      var marker = new google.maps.Marker({
        position: position,
        map: map,
        icon: image,
      });

      var infoWindow = new google.maps.InfoWindow({width: 150});
      var windowhtml = createInfoWindow(key, service.url);

      infoWindow.setContent(windowhtml);

      bindFavInfoWindow(marker, map, infoWindow);

      generateFavListing(results.fav_places, key);


    }

    $('#recs').empty();
    for (var rec in results.recs){
      var rec_info = results.recs[rec];
      var suggested_element = createSuggestedElement(rec, rec_info, results); 
      $('#recs').append(suggested_element);
    }

    map.data.addGeoJson(results.coordinates);
    $('#neighborhood-welcome').append("<h1>Welcome to " + results.neighborhood_name+"</h1>")
  });
}


function generateFavListing(places, key) {
 $('#fav_places').append('<li>'+key+'</li>');
}


google.maps.event.addDomListener(window, 'load', initMap);