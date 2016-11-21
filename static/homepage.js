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

function scrollWindow(evt) {
  evt.preventDefault();
  $('body, html').animate({
    scrollTop: $($(this).attr('href')).offset().top
  }, 1000);
}


$(document).ready(function () {
  $('#neighborhood-search').on('click', chooseNeighborhoodSearch);
  $('#address-search').on('click', chooseAddressSearch);
  $('.jumper').on('click', scrollWindow)
  $('#search').on('click', getMap)
  $('#search').on('click', function() {
    $('#geo-search').appendTo('#new-search-bar');
    $('#service-search').appendTo('#new-search-bar');
    $('#welcome-page').hide();
    $('#search-option').hide();
    window.scrollTo(0,0);
  });
});
