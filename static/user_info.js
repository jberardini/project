'use strict';
function initMap() {
    var position = {lat: -25.363, lng: 131.044};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: position,
    });
}