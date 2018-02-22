$(document).ready( function() {
	$("input.form-control").focusin( function(event) {
		var input_name = $(this).attr('name')
		var collapsible = $("div[name=" + input_name + "]");
		var expanded = $(collapsible).attr('class');
		if(expanded == "collapse"){
			$(collapsible).collapse('toggle');
		}
    });
	$("input.form-control").focusout( function(event) {
		var input_name = $(this).attr('name')
		var collapsible = $("div[name=" + input_name + "]");
		var expanded = $(collapsible).attr('class');
		if(expanded == "collapse show"){
			$(collapsible).collapse('toggle');
		}
    });
});