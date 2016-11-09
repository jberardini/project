var neighborhood = $('#neighborhood').val()
var services = $('input:checkbox:checked').map(function() {
    return parseInt($(this).val());
}).get();


$('#search').click(function(evt) {
    evt.preventDefault();
    $.get('/info.json', {neighborhood: neighborhood, services: services}, function() {
       alert('hello') 
   });       
});