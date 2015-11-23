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
					var farPoint = new google.maps.LatLng(data[0].fields.latitude,data[0].fields.longitude);
					var zoom = 20;
					map.setZoom(zoom);
					while (!map.getBounds().contains(farPoint) || zoom <= 0) {
						map.setZoom(--zoom);
					}
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

function createResultEntry(storeId, storeName, address, rating) {
  $('<li/>', {
    'class': 'result',
    'data-storeid': storeId
  }).appendTo('ul.results-list');
  $('<strong/>', {
    text: storeName
  }).appendTo(".result[data-storeid='" + storeId + "']");
  $('<p/>', {
    text: address
  }).appendTo(".result[data-storeid='" + storeId + "']");
  if (rating) {
    $('<p/>', {
      text: "Rating: " + rating
    }).appendTo(".result[data-storeid='" + storeId + "']");
  }
  $('<a/>', {
    href: '/store/' + storeId,
    text: "More Information..."
  }).appendTo(".result[data-storeid='" + storeId + "']");
}

function linkResultToMarker(marker, storeId) {
  $(".result[data-storeid='" + storeId + "']").hover(function() {
    marker.setOpacity(1.0);
    $(this).css("background-color", "#B9E5F3");
  }, function() {
    if (!marker.getAnimation()) {
      marker.setOpacity(0.5);
      $(this).css("background-color", "");
    }
  });

  $(".result[data-storeid='" + storeId + "']").click(function() {
    if ($(this).hasClass('active')) {
      marker.setAnimation(null);
      marker.setOpacity(0.5);
      $(this).removeClass('active');
      $(this).css("background-color", "");
    } else {
      $('.result.active').trigger('click');
      marker.setAnimation(google.maps.Animation.BOUNCE);
      $(this).addClass('active');
    }
  });
}

function linkMarkerToResult(marker, storeId) {
  marker.addListener('mouseover', function() {
    $(".result[data-storeid='" + storeId + "']").trigger('mouseenter');
    var resultPosition = $(".result[data-storeid='" + storeId + "']").offset().top;
    var paneTop = $(".results-container").offset().top;
    var paneBottom = paneTop + $(".results-container").height();

    if (resultPosition > paneBottom || resultPosition < paneTop) {
      $(".results-container").animate({
          scrollTop: resultPosition - 45 - 50
      }, 500);
    }
  });

  marker.addListener('mouseout', function() {
    $(".results-container").stop(true,false);
    $(".result[data-storeid='" + storeId + "']").trigger('mouseleave');
  });

  marker.addListener('click', function() {
    $(".result[data-storeid='" + storeId + "']").trigger('click');
  });
}
