'use strict';

function initMap() {
  $.get('/fav.json',  function (results) {
    var center = results.neighborhood;
    var map = new google.maps.Map(document.getElementById('favs_map'), {
      center: center,
      zoom: 15
    });

    for (var key in results.fav_places) {
      var service = results.fav_places[key];
      $('#fav_places').append('<li>'+key+'</li>');
      var position = new google.maps.LatLng(service.lat, service.lng);
      var image = "/../"+ service.picture
      var marker = new google.maps.Marker({
        position: position,
        map: map,
        icon: image,
      });

      $('#recs').empty();

      for (var rec in results.recs){
        var rec_info = results.recs[rec];
        console.log(rec_info.url);
        var my_string = '<li><a href='+rec_info.url+' target=_blank><img src=/../'+
                          rec_info.picture+'/>'+rec_info.name+'</a><button class=add2map onclick="addToMap('
                          +rec+', "'+rec_info.name+'", "'+results.neighborhood_name+
                          '", "'+rec_info.url+'", '+rec_info.lat+', '+rec_info.lng+
                          ')">Add to favorites</button></li>';
        console.log(my_string);
        $('#recs').append(my_string);
      }

      var infoWindow = new google.maps.InfoWindow({width: 150});

       var html = (
         '<div class="window-content">' +
             '<p>' + key + '</p>' +
             '<p><b>Url: </b> <a href=' + service.url + ' target=_blank>Website</a></p>' +
         '</div>');

      infoWindow.setContent(html);

      bindFavInfoWindow(marker, map, infoWindow);
    }
  });

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
}

google.maps.event.addDomListener(window, 'load', initMap);

function addToMap(service_id, name, neighborhood, url, lat, lng) {
  alert('hi!')
  // $.get('/set_favorite', {service_id: service_id, name: name, 
  //                         neighborhood: neighborhood, url: url, lat: lat, lng: lng})
  // make an AJAX call to some route to (1) send the data on the place, (2) add it to the DB, and (3) create a marker on a map with an info window, using coordinates, picture, name and url
}
