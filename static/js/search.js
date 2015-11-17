$(document).ready(function() {
	$('#search-bar').submit(function(event) {
		event.preventDefault()
		location = $('#search-bar-input').val();
		console.log(location);
		// geocoder.geocode({'address': location}, function(results, status) {
		// 	if (status == google.maps.GeocoderStatus.OK) {
		// 		map.setCenter(results[0].geometry.location);
		// 	} else {
		// 		alert("something went wrong");
		// 	}
		// });
	});
});