'use strict';

function getMap(evt) {
  evt.preventDefault();
  var neighborhood = $('#neighborhood > option:selected').val();
  console.log(neighborhood)
  var services = $('input:checkbox:checked').map(function() {
    return parseInt($(this).val());
  }).get();
  var address = $('#address').val();
  console.log(address)
  $.get('/info.json', {'neighborhood': neighborhood, 'services': services, 'address': address}, createMap);       
}

function chooseNeighborhoodSearch() {
  $('#address').val('');
  $('.address-search').hide();
  $('.neighborhood-search').show();
}

function chooseAddressSearch() {
  $("select option[value='blank']").attr('selected', true);
  $('.neighborhood-search').hide();
  $('.address-search').show();
}


$(document).ready(function () {
  $('#neighborhood-search').on('click', chooseNeighborhoodSearch);
  $('#address-search').on('click', chooseAddressSearch);
  $('#search').on('click', getMap);
})
