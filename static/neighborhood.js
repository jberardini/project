'use strict';


// var neighborhood = $('#neighborhood').val()
// var services = $('input:checkbox:checked').map(function() {
//     return parseInt($(this).val());
// }).get();
// console.log(services);

$('#search').click(function(evt) {
    evt.preventDefault();
    var neighborhood = $('#neighborhood').val();
    var services = $('input:checkbox:checked').map(function() {
        return parseInt($(this).val());
    }).get();
    $.get('/info.json', {neighborhood: neighborhood, services: services}, function() {
      console.log('hello'); 
   });       
});

// services = JSON.stringify(services);
function initMap() {
  // var neighborhood = $('#info').attr('data-neighborhood')
  // console.log(neighborhood)
  // var service_ids = $('#info').attr('data-services')
  // console.log(service_ids)

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
      if (prevInfoWindow) {
        prevInfoWindow.close();
      }

    prevInfoWindow = infoWindow;
    infoWindow.open(map, marker);
      console.log($('#logged-in').length)
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


function heartClick(){
  var service_id = parseInt($(this).attr('id'))
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