'use strict';

function getMap(evt) {
  evt.preventDefault();
  var neighborhood_id = $('#neighborhood > option:selected').val();
  var services = $('input:checkbox:checked').map(function() {
    return parseInt($(this).val());
  }).get();
  var address = $('#address').val();
  var city = $('#city').val();
  var state = $('#state').val();
  $.get('/info.json', {'neighborhood_id': neighborhood_id, 'services': services, 'address': address, 'city': city, 'state': state}, createMap);       
}

function chooseNeighborhoodSearch() {
  $('#address').val('');
  $('.address-search').hide();
  $('.neighborhood-search').show();
  $('.geo-go').show();
}

function chooseAddressSearch() {
  $('#neighborhood').val('blank')
  $('.neighborhood-search').hide();
  $('.address-inputs').css('display', 'table');
  $('.address-search').show();
  $('.geo-go').show();
}

function scrollWindow(evt) {
  evt.preventDefault();
  $('body, html').animate({
    scrollTop: $($(this).attr('href')).offset().top
  }, 800);
}

var moveItems = function() {
  $('.images').remove();
  $('.img-container').remove();
  $('#geo-search').appendTo('#new-search-bar');
  $('.geo-go').remove();
  $('#service-search').appendTo('#new-search-bar').css('background-color', 'white').css('padding-top', 0);
  $('.container').css('border-color', 'white').css('width', 300).css('margin-top', 0).css('height', 25).css('padding-top', 0).css('text-align', 'left').css('background-color', 'white')
  $('.img-label').css('margin-left', 30).css('margin-bottom', 2).css('margin-right', 2).css('margin-top', 2)
  $('.checkbox').css('position', 'relative').css('float', 'left')
  $('#welcome-page').hide();
  $('#search-option').hide();
}


$(document).ready(function () {
  $('#neighborhood-search').on('click', chooseNeighborhoodSearch);
  $('#address-search').on('click', chooseAddressSearch);
  $('.jumper').on('click', scrollWindow)
  $('#search').on('click', getMap)
  $('#search').on('click', function() {
    $.when( moveItems() ).done(function() {
      $('#geo-search').removeClass().css('margin-top', 30).css('margin-left', 30).css('margin-bottom', 20)
      $('#service-search').css('margin-left', 30)
      $('.search-type').css('font-size', 12)
      $('.neighborhood-search').css('color', 'black').css('font-size', 12)
      $('.address-search').css('color', 'black').css('font-size', 12)
      $('.img-label').css('color', 'black').css('font-size', 12)
      $('.explanation').css('color', 'black').css('font-size', 12)
      $('#neighborhood-welcome').css('font-family', 'Raleway, sans-serif')
      });
    window.scrollTo(0,0);
  });
});
