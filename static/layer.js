    var src = 'http://dl.dropbox.com/s/8k8453dk6i6u33r/neighborhoods.kml';
    var layer = new google.maps.KmlLayer(src);
    google.maps.event.addListener(layer, 'status_changed', function() {
      if (layer.getStatus() != 'OK') {
        alert('Google Maps could not load. Status returned is' +layer.getStatus());
      };
    });
    layer.setMap(map);