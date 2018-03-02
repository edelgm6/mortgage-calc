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

$("#id_price,#id_alternative_rent").keyup( function(event) {

  // skip for arrow keys
  if (event.which >= 37 && event.which <= 40) return;

	// block any non-number
  if ((event.shiftKey || (event.keyCode < 48 || event.keyCode > 57)) && (event.keyCode < 96 || event.keyCode > 105)) {
      event.preventDefault();
  }
	
  // format number
  $(this).val(function(index, value) {
    return value
    .replace(/\D/g, "")
    .replace(/\B(?=(\d{3})+(?!\d))/g, ",")
    ;
  });
});