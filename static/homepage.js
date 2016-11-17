'use strict';

function getMap(evt) {
  evt.preventDefault();
  var neighborhood = $('#neighborhood > option:selected').val();
  var services = $('input:checkbox:checked').map(function() {
    return parseInt($(this).val());
  }).get();
  var address = $('#address').val();
  $.get('/info.json', {'neighborhood': neighborhood, 'services': services, 'address': address}, createMap);       
}

function chooseNeighborhoodSearch() {
  $('#address').val('');
  $('.address-search').hide();
  $('.neighborhood-search').show();
}

function chooseAddressSearch() {
  $('#neighborhood').val('blank')
  $('.neighborhood-search').hide();
  $('.address-search').show();
}


$(document).ready(function () {
  $('#neighborhood-search').on('click', chooseNeighborhoodSearch);
  $('#address-search').on('click', chooseAddressSearch);
  $('#search').on('click', getMap);
})
