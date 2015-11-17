$(document).ready(function() {
	$('#search-bar').submit(function(event) {
		geocoder.geocode({'address': $('#search-bar-input').val()}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				map.setCenter(results[0].geometry.location);
				map.setZoom(14);
			} else {
				// Add no results found error message
				// $( "span" ).text( "Not valid!" ).show().fadeOut( 1000 );
			}
		});
		event.preventDefault();
		// location = $('#search-bar-input').val();
		// console.log(location);
		
	});
});