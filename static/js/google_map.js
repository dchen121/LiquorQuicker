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
    var map_top = bounds.getNorthEast().lat();
    var map_bottom = bounds.getSouthWest().lat();
    var map_right = bounds.getNorthEast().lng();
    var map_left = bounds.getSouthWest().lng();
    var lat = null;
    var lng = null;

    if (currentLocation) {
      lat = currentLocation.position.lat();
      lng = currentLocation.position.lng();
    }

    $.post('/load_locations/', { 
      lat: lat,
      lng: lng,
      top: map_top, 
      bottom: map_bottom, 
      right: map_right, 
      left: map_left,
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

function createResultEntry(storeId, storeName, address) {
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


function plotLocations(locations) {
  for (var j = 0; j < locations.length; j++) {
    loc = locations[j];
    marker = createMarker({'lat': loc.fields.latitude, 'lng': loc.fields.longitude });
    createResultEntry(loc.pk, loc.fields.name, loc.fields.address + ", " + loc.fields.city);
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