$(document).ready(function () {
	$('[data-toggle="tooltip"]').tooltip();
	$(".form-control").focusin(function () {
		var input_name = $(this).attr('name')
		var collapsible = $("div[name=" + input_name + "]");
		var expanded = $(collapsible).attr('class');
		if (expanded == "collapse") {
			$(collapsible).collapse('toggle');
		}
	});
	$(".form-control").focusout(function () {
		var input_name = $(this).attr('name')
		var collapsible = $("div[name=" + input_name + "]");
		var expanded = $(collapsible).attr('class');
		if (expanded == "collapse show") {
			setTimeout(function () {
				$(collapsible).collapse('toggle');
			}, 100);

		};
	});

});

$("#investmentForm").validate({
	submitHandler: function(form) {
		investmentFormSubmit()
	},
	ignore: false,
	invalidHandler: function (e, validator) {
		// loop through the errors:
		for (var i = 0; i < validator.errorList.length; i++) {
			// "uncollapse" section containing invalid input/s:
			$(validator.errorList[i].element).closest('.collapse').collapse('show');

		}
	},
	errorElement: "div",
	errorPlacement: function (error, element) {
		// Add the `invalid-feedback` class to the error element
		error.addClass("invalid-feedback");

		//if (element.prop("type") === "checkbox") {
		//	error.insertAfter(element.parent("label"));
		//} else {
		//Some inputs have an append div after -- check if that exists
		//If so, slot the error after the div.  Else put it after the input
		if (element.siblings(".input-group-append").length > 0) {
			var $targetdiv = element.siblings(".input-group-append")
			error.insertAfter($targetdiv);
		} else {
			error.insertAfter(element);
		}

		//}
	},
	/*
	highlight: function (element, errorClass, validClass) {
		$(element).parents(".col-md-7").addClass("invalid-feedback").removeClass("valid-feedback");
	},
	unhighlight: function (element, errorClass, validClass) {
		$(element).parents(".col-md-7").addClass("valid-feedback").removeClass("invalid-feedback");
	}*/
});

$("#id_price,#id_alternative_rent").keyup(function (event) {

	// skip for arrow keys
	if (event.which >= 37 && event.which <= 40) return;

	// block any non-number
	if ((event.shiftKey || (event.keyCode < 48 || event.keyCode > 57)) && (event.keyCode < 96 || event.keyCode > 105)) {
		event.preventDefault();
	}

	// format number
	$(this).val(function (index, value) {
		return value
			.replace(/\D/g, "")
			.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	});
});

$("#reset_defaults").click(function () {
	var closing_cost_default = 3.0;
	var property_tax_default = 2.0;
	var insurance_default = .5;
	var maintenance_cost_default = 1.0;
	var realtor_cost_default = 6.0;

	$("#id_closing_cost").val(closing_cost_default);
	$("#id_property_tax").val(property_tax_default);
	$("#id_insurance").val(insurance_default);
	$("#id_maintenance_cost").val(maintenance_cost_default);
	$("#id_realtor_cost").val(realtor_cost_default);
});