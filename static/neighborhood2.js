'use strict';


function createHomeInfoWindow(neighborhood, service_id, service_info) {
  var $windowhtml = $("<div></div>");
  var $bname = $("<p></p>");
  var $url = $("<a target=_blank>Visit website</a>");
  var $fav_instructions = $("<p>Add to favorites: </p>");
  var $img = $("<img src=/static/img/like-1.png class=favorite></img>")
  $bname.html(service_info.name);
  $url.attr('href', service_info.url);
  $windowhtml.append($bname).append($url).append($fav_instructions).append($img);
  return $windowhtml.html();
}


function createMap(results) {
  $('#neighborhood-welcome').html('Welcome to'+ ' ' +String(results.name))
  var position = results.neighborhood
  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: position
  });

  map.data.addGeoJson(results.coordinates);

   // creates markers
  for (var service_id in results.services) {
    var service_info = results.services[service_id];
    var image = service_info.picture
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(service_info.lat, service_info.lng),
      map: map,
      icon: image,
    });

    var infoWindow = new google.maps.InfoWindow({width: 150});
    var windowhtml = createHomeInfoWindow(results.neighborhood, service_id, service_info)

    infoWindow.setContent(windowhtml);

    bindHomeInfoWindow(marker, map, infoWindow, results.name, service_id, service_info);
  }
}

var prevHomeInfoWindow=false;

function bindHomeInfoWindow(marker, map, infoWindow, name, service_id, service_info) {
 google.maps.event.addListener(marker, 'click', function() {
   if (prevHomeInfoWindow) {
      prevHomeInfoWindow.close();
   }
   prevHomeInfoWindow = infoWindow;
   infoWindow.open(map, marker);

   if ($('#logged-out').length === 0) {
     $('.favorite').on('click', function(){
        heartClick(name, service_id, service_info);
     });
   } else {
     $('.favorite').on('click', function() {
       if (window.confirm('You must create an account to save a favorite place. Click ok to sign up.')) {
         window.location.href='/sign-up';
       }
     });
   }

  });
}

function heartClick(neighborhood, service_id, service_info) {
  $.get('/set_favorite', {service_id: service_id, 
                              name: service_info.name, 
                              neighborhood: neighborhood, 
                              url: service_info.url, 
                              lat: service_info.lat, 
                              lng: service_info.lng}, function() {
    if ($('.favorite').attr('src')==='/static/img/like-1.png') {
      $('.favorite').attr('src', '/static/img/like.png');
    } else {
      $('.favorite').attr('src', '/static/img/like-1.png');
    }
  });
}

function helloWorld() {
  return "Hello world!";
}
  





