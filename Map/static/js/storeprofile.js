$(document).ready(function() {
	$("#favourite-btn").click(function(e) {
		var store = $(this).attr("data-storeid");
		var user = $(this).attr("data-userid");
		$.get('/favourite_store', { store: store, user: user }, function(data) {
			if (data) {
				$("#favourite-btn").attr("disabled", true);
			}
		});
	});
});

window.onload = function loadDropdownMenu() {

    var locations = {{ locations|safe }};
    cities = [];
    for (var j = 0; j < locations.length; j++) {
      loc = locations[j];
      if (!contains(cities, loc.fields.city)) {
        cities.push(loc.fields.city);
      }
    }
    cities.sort();

    var dropdown_menu = document.getElementById('DropdownCities');

    for (var i = 0; i < cities.length; i++) {
      city = cities[i];
      var newLi = document.createElement('li');

      var newA = document.createElement('a');
      newA.style.textAlign = "center";
      newA.setAttribute("href", '/filter/' + city);
      newA.innerHTML = city + "<br>";

      newLi.appendChild(newA);
      dropdown_menu.appendChild(newLi); // append <li><a href=('filter/' + city) align='center'> city </a></li><br> to dropdown_menu
    }
  }

  function contains(list, item) {
    for (var i = 0; i < list.length; i++) {
      if (item === list[i]) {
        return true;
      }
    }
    return false;
  }




  