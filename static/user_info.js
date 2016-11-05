'use strict';


function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 37.7749, lng: -122.4194},
    zoom: 12
  });
  var src = 'http://dl.dropbox.com/s/8k8453dk6i6u33r/neighborhoods.kml';
  var layer = new google.maps.KmlLayer(src);
  google.maps.event.addListener(layer, 'status_changed', function() {
    if (layer.getStatus() != 'OK') {
      alert('Google Maps could not load. Status returned is' +layer.getStatus());
    };
  });


  layer.setMap(map);
}

google.maps.event.addDomListener(window, 'load', initMap);

