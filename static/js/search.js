$(document).ready(function() {
	$('#search-bar').submit(function(event) {
		geocoder.geocode({'address': $('#search-bar-input').val()}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				if (currentLocation) {
					currentLocation.setMap(null);
					currentLocation = null;
				}
				map.setCenter(results[0].geometry.location);
				marker = new google.maps.Marker({
					map: map,
					position: map.getCenter(),
					icon: {
						path: google.maps.SymbolPath.CIRCLE,
						scale: 10,
						strokeColor: "green"
					},
					zIndex: -10000
				});
				currentLocation = marker;

				var lat = results[0].geometry.location.lat();
				var lng = results[0].geometry.location.lng();
				var count = 5;
				$.get('/closest_points', { lat: lat, lng: lng }, function(data) {
					var bounds = map.getBounds();
					bounds.extend(new google.maps.LatLng(data[0].fields.latitude,data[0].fields.longitude));
					map.fitBounds(bounds);
				});
			} else {
				// Add an error message
			}
		});
		event.preventDefault();
	});
});