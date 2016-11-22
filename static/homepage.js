'use strict';

function getMap(evt) {
  evt.preventDefault();
  var neighborhood_id = $('#neighborhood > option:selected').val();
  var services = $('input:checkbox:checked').map(function() {
    return parseInt($(this).val());
  }).get();
  var address = $('#address').val();
  $.get('/info.json', {'neighborhood_id': neighborhood_id, 'services': services, 'address': address}, createMap);       
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
    $('.images').remove();
    $('.img-container').remove();
    $('#geo-search').appendTo('#new-search-bar');
    $('#service-search').appendTo('#new-search-bar');
    $('.container').css('border-color', 'white').css('width', 300).css('margin-top', 0).css('height', 25).css('padding-top', 0).css('text-align', 'left')
    $('.img-label').css('margin-left', 30).css('margin-bottom', 2).css('margin-right', 2).css('margin-top', 2)
    $('.checkbox').css('position', 'relative').css('float', 'left')
    $('#welcome-page').hide();
    $('#search-option').hide();
    window.scrollTo(0,0);
  });
});
