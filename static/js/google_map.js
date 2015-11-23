var map;
var geocoder;
var markers = [];
var currentLocation = null;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 49.2561055, lng: -123.1939531},
    zoom: 11
  });
  geocoder = new google.maps.Geocoder();

  map.addListener('idle', function() {
    var bounds = map.getBounds();
    var mapTop = bounds.getNorthEast().lat();
    var mapBottom = bounds.getSouthWest().lat();
    var mapRight = bounds.getNorthEast().lng();
    var mapLeft = bounds.getSouthWest().lng();
    var minRating = parseInt($('input[name="min-rating"').val());
    var sortByRating = $('input[name="sort-by"][value="rating"]').is(":checked");
    var lat = null;
    var lng = null;

    if (currentLocation) {
      lat = currentLocation.position.lat();
      lng = currentLocation.position.lng();
    }

    $.post('/load_locations/', { 
      lat: lat,
      lng: lng,
      top: mapTop, 
      bottom: mapBottom, 
      right: mapRight, 
      left: mapLeft,
      minRating: minRating,
      sortByRating: sortByRating, 
      csrfmiddlewaretoken: getCookie("csrftoken")
    }, function(data) {
      clearMarkers();
      $('ul.results-list').empty();
      plotLocations(data);
    }, 'json');
  });
}

function clearMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}

function createMarker(latLng) {
  var marker = new google.maps.Marker({
    map: map,
    position: latLng,
    zIndex: 10,
    opacity: 0.5
  });
  markers.push(marker);
  return marker;
}

function plotLocations(locations) {
  for (var j = 0; j < locations.length; j++) {
    loc = locations[j];
    marker = createMarker({'lat': loc.fields.latitude, 'lng': loc.fields.longitude });
    createResultEntry(loc.pk, loc.fields.name, loc.fields.address + ", " + loc.fields.city, loc.fields.avg_rating);
    linkResultToMarker(marker, loc.pk);
    linkMarkerToResult(marker, loc.pk);
  }
}

// Django code for getting csrftoken for AJAX requests (https://docs.djangoproject.com/en/1.8/ref/csrf/#ajax)
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}