var map;
var geocoder;
var markers = [];

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 49.2561055, lng: -123.1939531},
    zoom: 11
  });
  geocoder = new google.maps.Geocoder();

  map.addListener('idle', function() {
    bounds = map.getBounds();
    map_top = bounds.getNorthEast().lat();
    map_bottom = bounds.getSouthWest().lat();
    map_right = bounds.getNorthEast().lng();
    map_left = bounds.getSouthWest().lng();
    $.getJSON('/load_locations', { 
      top: map_top, 
      bottom: map_bottom, 
      right: map_right , 
      left: map_left 
    }, function(data) {
      clearMarkers();
      plotLocations(data);
    });
  });
  }

function clearMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}

function createMarker(storeName, address, latLng) {
  var marker = new google.maps.Marker({
    map: map,
    position: latLng
  });

  marker.addListener('click', function() {
    var contentString = "<strong>" + storeName + "</strong></br>" +
                        "<p>" + address + "</p>";
    var infowindow = new google.maps.InfoWindow ({
      content: contentString
    });
    infowindow.open(map, marker);
  });

  markers.push(marker);
}

function plotLocations(locations) {
  for (var j = 0; j < locations.length; j++) {
    loc = locations[j];
    createMarker(loc.fields.name, loc.fields.address + ", " + loc.fields.city, {'lat': loc.fields.latitude, 'lng': loc.fields.longitude });
  }
}

