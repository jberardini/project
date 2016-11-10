'use strict';

function getMap(evt) {
    evt.preventDefault();
    var neighborhood = $('#neighborhood > option:selected').val();
    console.log(neighborhood)
    var services = $('input:checkbox:checked').map(function() {
      return parseInt($(this).val());
    }).get();
    console.log(services)
    $.get('/info.json', {'neighborhood': neighborhood, 'services': services}, createMap);       
}


$(document).ready(function () {
  $('#search').on('click', getMap);
})
