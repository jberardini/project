 function initMap() {
        var infoWindow = new google.maps.InfoWindow({width: 150});
      
        $.get('/info.json', function (results) {
          var position = results.neighborhood
          var map = new google.maps.Map(document.getElementById("map"), {
          zoom: 15,
          center: position
        });


          // creates markers
          for (var key in results.services) {
            service = results.services[key];

            var marker = new google.maps.Marker({
              position: new google.maps.LatLng(service.lat, service.lng),
              map: map,
          });

            html = (
              '<div class="window-content">' +
                  '<p><b>Name: </b>' + service.name + '</p>' +
                  '<p><b>Url: </b>' + service.url + '</p>' +
              '</div>');

             bindInfoWindow(marker, map, infoWindow, html);

        }
      });

      var marker, html;
      function bindInfoWindow(marker, map, infoWindow, html) {
          google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
          });
      }
    }

