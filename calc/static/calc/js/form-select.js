$(document).ready( function() {
	$(".form-control").focusin( function() {
		var input_name = $(this).attr('name')
		var collapsible = $("div[name=" + input_name + "]");
		var expanded = $(collapsible).attr('class');
		if(expanded == "collapse"){
			$(collapsible).collapse('toggle');
		}
    });
	$(".form-control").focusout( function() {
		var input_name = $(this).attr('name')
		var collapsible = $("div[name=" + input_name + "]");
		var expanded = $(collapsible).attr('class');
		if(expanded == "collapse show"){
			setTimeout(function() {
				$(collapsible).collapse('toggle');
			}, 100);
			
		};
    });
});