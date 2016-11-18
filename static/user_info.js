'use strict';
var map;

function createSuggestedElement(rec, rec_info, results) {
  // creating html element
  var $li = $("<li></li>");
  var $img = $("<img></img>");
  var imgUrl =  '/../' + rec_info.picture;
  var $a = $("<a></a>")
  var $button = $('<button></button>');
  var name = rec_info.name 

  //setting attributes of html element
  $img.attr('src', imgUrl);
  $a.html(rec_info.name)
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
    $.get('/set_favorite', {'service_id': rec, 'name': rec_info.name,
                            'neighborhood': results.neighborhood_name,
                            'url': rec_info.url, 'lat': rec_info.lat,
                            'lng': rec_info.lng }, function() {
                              console.log('Success!')
                            });
  });
  $li.append($img);
  $li.append($a);

  $li.append($button)
  return $li;
}

function initMap() {
  $.get('/fav.json',  function (results) {
    var center = results.neighborhood;
    map = new google.maps.Map(document.getElementById('favs_map'), {
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
        var suggested_element = createSuggestedElement(rec, rec_info, results); 
        
        $('#recs').append(suggested_element);
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
