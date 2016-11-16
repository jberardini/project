'use strict';

function initMap() {
  $.get('/fav.json',  function (results) {
    var center = results.neighborhood;
    console.log(center)
    console.log(results.neighborhood);
    var map = new google.maps.Map(document.getElementById('favs_map'), {
      center: center,
      zoom: 15
    });

    for (var key in results.fav_places) {
      var service = results.fav_places[key];
      $('#fav_places').append('<li>'+key+'</li>');
      var position = new google.maps.LatLng(service.lat, service.lng);
      var image = "/../"+ service.picture
      console.log(image)
      var marker = new google.maps.Marker({
        position: position,
        map: map,
        icon: image,
      });

      for (var rec in results.recs){
        var rec_info = results.recs[rec];
        $('#recs').append('<li><a href='+rec_info.url+' target=_blank><img src=/../'+rec_info.picture+'/>'+rec_info.name+'</a></li>');
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