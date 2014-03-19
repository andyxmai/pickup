$("#sports_select li a").click(function() {
	var sport = $(this).attr("value");
	var sports = localStorage.getItem("sports");
	var obj ={};
	
	if($(this).hasClass("selected")) {
		if(sports){
		   obj = JSON.parse(sports);  
		}
		if(sport in obj) {
			delete obj[sport];
			if (jQuery.isEmptyObject(obj)) {
				if (!($("#next_step_button").hasClass("disabled"))) {
					$("#next_step_button").addClass("disabled");
				}
			}
		}

		$(this).removeClass("selected");
	} else {
		$(this).addClass("selected");
		console.log(sport);
		console.log(sports);
		if(sports){
		   obj = JSON.parse(sports);  
		}
		if (!(sport in obj)) {
			console.log('here');
			obj[sport] = true;
		}

		if ($("#next_step_button").hasClass("disabled")) {
			$("#next_step_button").removeClass("disabled");
		}
	}

	localStorage.setItem("sports",JSON.stringify(obj));

	console.log(JSON.parse(localStorage.getItem("sports")));
});
$("#next_step_button").click(function() {
	$.ajax({
	  type: "POST",
	  url: "/first_login/",
	  data: { 
	    'csrfmiddlewaretoken':'{{csrf_token}}',
	    'sports': localStorage.getItem("sports")
	  },
	  success: function(data) {
	    window.location.href = '/first_login2'
	  },
	});
});