$(document).ready(function() {
	$('#search-bar').submit(function(event) {
		geocoder.geocode({'address': $('#search-bar-input').val()}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				if (currentLocation) {
					currentLocation.setMap(null);
					currentLocation = null;
				}
				map.setCenter(results[0].geometry.location);
				markLocation(results[0].geometry.location);
				
				var lat = results[0].geometry.location.lat();
				var lng = results[0].geometry.location.lng();
				var count = 5;
				$.get('/closest_points', { lat: lat, lng: lng }, function(data) {
					map.setZoom(20);
					var bounds = map.getBounds();
					bounds.extend(new google.maps.LatLng(data[4].fields.latitude,data[4].fields.longitude));
					map.fitBounds(bounds);
				});
			} else {
				// Add an error message
			}
		});
		event.preventDefault();
	});
});


function markLocation(latLng) {
	marker = new google.maps.Marker({
		map: map,
		position: latLng,
		icon: {
			path: google.maps.SymbolPath.CIRCLE,
			scale: 10,
			strokeColor: "green"
		},
		zIndex: -10000
	});
	currentLocation = marker;

	currentLocation.addListener('click', function() {
		currentLocation.setMap(null);
		currentLocation = null;
	});
}