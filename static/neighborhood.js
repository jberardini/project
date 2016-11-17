'use strict';


function createMap(results) {
  $('#neighborhood-welcome').html('Welcome to'+ ' ' +String(results.name))
  var position = results.neighborhood
  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: position
  });
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

    var html = (
      '<div class="window-content">' +
         '<p>' + service_info.name + '</p>' +
         '<p><b>Url: </b> <a href=' + service_info.url + ' target=_blank>Website</a></p>' +
         '<p><b>Add to Favorites:</b></p>' +
         '<img src=/static/img/like-1.png class=favorite data-url='+service_info.url+' data-neighborhood="'+service_info.neighborhood+'" id='+service_id+' data-name="'+service_info.name+'" data-lat='+service_info.lat+' data-lng='+service_info.lng+'>' +
      '</div>');


    infoWindow.setContent(html);

    bindInfoWindow(marker, map, infoWindow);
  }

  map.data.addGeoJson(results.coordinates);

  var prevInfoWindow=false;
  function bindInfoWindow(marker, map, infoWindow) {
    google.maps.event.addListener(marker, 'click', function() {
      if (prevInfoWindow) {
        prevInfoWindow.close();
      }

    prevInfoWindow = infoWindow;
    infoWindow.open(map, marker);
      if ($('#logged-out').length === 0) {
        $('.favorite').on('click', heartClick);
      } else {
        $('.favorite').on('click', function() {
          if (window.confirm('You must create an account to save a favorite place. Click ok to sign up.')) {
            window.location.href='/sign-up';
          }
        });
      }
    });
  }
}


function heartClick() {
  var service_id = parseInt($(this).attr('id'))
  var name = $(this).attr('data-name')
  var neighborhood = $(this).attr('data-neighborhood')
  var url = $(this).attr('data-url')
  var lat = parseFloat($(this).attr('data-lat'))  
  var lng = parseFloat($(this).attr('data-lng'))
  $.get('/set_favorite', {service_id: service_id, name: name, neighborhood: neighborhood, url: url, lat: lat, lng: lng}, function() {
    if ($('.favorite').attr('src')==='/static/img/like-1.png') {
      $('.favorite').attr('src', '/static/img/like.png');
    } else {
      $('.favorite').attr('src', '/static/img/like-1.png');
    }
  });
}




// function heartClick() {
//   alert('hello');
//   }