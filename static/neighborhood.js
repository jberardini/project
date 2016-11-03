"use strict"
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
       var service = results.services[key];

       var marker = new google.maps.Marker({
         position: new google.maps.LatLng(service.lat, service.lng),
         map: map,
     });


    var marker, html;

       html = (
         '<div class="window-content">' +
             '<p id='+key + '>' + service.name + '</p>' +
             '<p><b>Url: </b> <a href=' + service.url + '>Website</a></p>' +
             '<p><b>Add to Favorites:</b></p>' +
             '<img src=/static/img/like-1.png onclick=heartClick('+key+'); class=favorite data-name="'+service.name+
             '">' +
         '</div>');

        bindInfoWindow(marker, map, infoWindow, html);
   }


 });

 function bindInfoWindow(marker, map, infoWindow, html) {
     google.maps.event.addListener(marker, 'click', function () {
       infoWindow.close();
       infoWindow.setContent(html);
       infoWindow.open(map, marker);
    });
 }

 
}


function heartClick (key){ 
  // console.log($(this))
  // console.log(key)
  // // var name = $(this).attr('data-name');
  // console.log(name)
  name = $('#'+key).html()
  $.get('/set_favorite', {'key': key, 'name':name}, function(){
  });
 }

 


// function heartClick() {
//   alert('hello');
//   }