$(document).ready(function() {
	$("#favourite-btn").click(function(e) {
		var store = $(this).attr("data-storeid");
		var user = $(this).attr("data-userid");
		$.get('/favourite_store', { store: store, user: user }, function(data) {
			$("#favourite-btn").attr("disabled", true);
		});
	});
});