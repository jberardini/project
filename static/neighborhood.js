'use strict';
function initMap() {
   
 
   $.get('/info.json', function (results) {
     var position = results.neighborhood
     var map = new google.maps.Map(document.getElementById("map"), {
     zoom: 15,
     center: position
   });


     // creates markers
     for (var key in results.services) {
       var service = results.services[key];
       var image = service.picture
       var marker = new google.maps.Marker({
         position: new google.maps.LatLng(service.lat, service.lng),
         map: map,
         icon: image,
     });

      var infoWindow = new google.maps.InfoWindow({width: 150});

       var html = (
         '<div class="window-content">' +
             '<p id='+key + '>' + service.name + '</p>' +
             '<p><b>Url: </b> <a href=' + service.url + ' target=_blank>Website</a></p>' +
             '<p><b>Add to Favorites:</b></p>' +
             '<img src=/static/img/like-1.png class=favorite id='+key+' data-name="'+service.name+
             '">' +
         '</div>');

      infoWindow.setContent(html);

      bindInfoWindow(marker, map, infoWindow);
   }

 });

  var prevInfoWindow=false;
 function bindInfoWindow(marker, map, infoWindow) {
     google.maps.event.addListener(marker, 'click', function() {
       console.log(prevInfoWindow)
       if (prevInfoWindow) {
          prevInfoWindow.close();
       }

       prevInfoWindow = infoWindow;
       infoWindow.open(map, marker);
       $('.favorite').on('click', heartClick);
       console.log(prevInfoWindow)
    });
 }

 
}


function heartClick(){
  var service_id = parseInt($(this).attr('id'))
  console.log(service_id)
  var name = $(this).attr('data-name')
  $.get('/set_favorite', {service_id: service_id, name: name}, function() {
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