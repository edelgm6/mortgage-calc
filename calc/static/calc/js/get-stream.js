var first_click = true;

function investmentFormSubmit() {
	$('.overlay').show();

	$('.mortgage').remove();
	
	var get_data = {
		'price': $('#id_price').val().replace(/,/g, ""),
		'closing_cost': $('#id_closing_cost').val(),
		'maintenance_cost': $('#id_maintenance_cost').val(),
		'property_tax': $('#id_property_tax').val(),
		'down_payment': $('#id_down_payment').val(),
		'interest_rate': $('#id_interest_rate').val(),
		'yearly_appreciation': $('#id_yearly_appreciation').val(),
		'alternative_rent': $('#id_alternative_rent').val().replace(/,/g, ""),
		'realtor_cost': $('#id_realtor_cost').val(),
		'federal_tax_bracket': $('#id_federal_tax_bracket').val(),
		'state_tax_bracket': $('#id_state_tax_bracket').val(),
		'insurance': $('#id_insurance').val()
	};
	
	$.ajax({
		method: 'GET',
		url: 'stream/',
		data: get_data
	})
	.done(function (data) {

		var get_url = ("?price=" + get_data['price'] + "&closing_cost=" + get_data['closing_cost'] + "&maintenance_cost=" + get_data['maintenance_cost'] + "&property_tax=" + get_data['property_tax'] + "&down_payment=" + get_data['down_payment'] + "&interest_rate=" + get_data['interest_rate'] + "&yearly_appreciation=" + get_data['yearly_appreciation'] + "&alternative_rent=" + get_data['alternative_rent'] + "&realtor_cost=" + get_data['realtor_cost'] + "&federal_tax_bracket=" + get_data['federal_tax_bracket'] + "&state_tax_bracket=" + get_data['state_tax_bracket'] + "&insurance=" + get_data['insurance'])
		window.history.pushState("object or string", "Mortgage ROI", "/" + get_url);
		
		var mortgage_payment = convertNumberToString(data.mortgage_payment * -1);
		$('#mortgage_payment').text(mortgage_payment);
		$('#rent_payment').text($('#id_alternative_rent').val())
		//If down payment is 1 then give the takeaways content class to the no mortgage div
		if (get_data['down_payment'] >= 100){
			$('#takeaways_no_mortgage').addClass('takeaways-content');
			$('#takeaways_has_mortgage').removeClass('takeaways-content').hide();
		} else {
			$('#takeaways_has_mortgage').addClass('takeaways-content')
			$('#takeaways_no_mortgage').removeClass('takeaways-content').hide();
		};
		
		var table_body = $('#tbody');
		var cash_stream = data.cash_stream;
		var first_year_ppmt_greater_than_ipmt = false;
		var first_year_positive_cash_flow = false;
		var peak_irr = -100.00;
		var peak_irr_year = 0;
		$.each(cash_stream, function (key, value) {
			var $tr = $("<tr>", {
				'class': 'mortgage',
				'style': 'display:none;'
			});
			var $td_year = $("<td>", {
				'text': value.year
			});
			var $td_principal_payment = $("<td>", {
				'text': convertNumberToString(value.principal_payment)
			});
			var $td_debt_payment = $("<td>", {
				'text': convertNumberToString(value.debt_payment)
			});
			var $td_other_costs = $("<td>", {
				'text': convertNumberToString(value.other_costs)
			});
			var $td_saved_rent = $("<td>", {
				'text': convertNumberToString(value.saved_rent)
			});
			var $td_total = $("<td>", {
				'text': convertNumberToString(value.total)
			});
			var $td_value = $("<td>", {
				'text': convertNumberToString(value.value)
			});
			var $td_debt = $("<td>", {
				'text': convertNumberToString(value.debt)
			});
			var $td_equity = $("<td>", {
				'text': convertNumberToString(value.equity)
			});
			var $td_irr = $("<td>", {
				'text': value.irr + '%'
			});

			if (!first_year_ppmt_greater_than_ipmt && value.year != 'Purchase') {
				var ppmt = value.principal_payment;
				var ipmt = value.debt_payment;

				if (ppmt < ipmt) {
					first_year_ppmt_greater_than_ipmt = true;
					$('#first_year_ppmt_greater_than_ipmt').text(value.year);
				};
			};
			
			if (value.year != 'Purchase') {
				if (data.base_irr[value.year] > peak_irr) {
					peak_irr = data.base_irr[value.year];
					peak_irr_year = value.year;
				};
			};

			$(table_body).append(($tr)
				.append(($td_year))
				.append(($td_principal_payment))
				.append(($td_debt_payment))
				.append(($td_other_costs))
				.append(($td_saved_rent))
				.append(($td_total))
				.append(($td_value))
				.append(($td_debt))
				.append(($td_equity))
				.append(($td_irr))
			);

			$($tr).children().each(function () {
				if ($(this).text().indexOf("-") >= 0) {
					$(this).addClass("text-danger");
				};
			});
		});
		
		setTimeout(function () {
			$('.overlay').removeAttr('style');
			$('#peak_irr').text(peak_irr);
			$('#sell_year').text(peak_irr_year);
			
			buildIRRChart(data.base_irr, data.high_irr, data.low_irr);
			buildValueDriversChart(data.mortgage_driver_irr, data.alternative_rent_driver_irr, data.tax_shield_driver_irr, data.appreciation_driver_irr);
			buildPMTChart(cash_stream);
			buildCashFlowChart(cash_stream);
			if (Object.keys(irrChartObject).length>0) {
				irrChartObject.update();
				pmtChartObject.update();
				cashFlowChartObject.update();
				valueDriversChartObject.update();
			};
			$('#thead').fadeIn(1000);
			$('.takeaways-content').fadeIn(1000);
			if (first_click) {
				$(window).scrollTo('#takeaways', 800);
				first_click = false;
			};	
			$(".mortgage").fadeIn(1000);
		}, 3000);	


	});
};

function buildTable(data) {
	
}

function convertNumberToString(number) {
	try {
		var x = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		return x;
	} catch (err) {
		console.log(err);
		return number;
	}
};

function buildValueDriversChart(mortgage, rent, tax_shield, appreciation) {

	var labels = [];
	for (var i = 1; i < mortgage.length; i++) {
		labels.push(i+1);
	};
	
	//Slice(1) needed as first value (i.e., slice (0)) is year 1 -- want 2->30
	if (Object.keys(valueDriversChartObject).length==0) {
		valueDriversChart(labels, mortgage.slice(1), rent.slice(1), tax_shield.slice(1), appreciation.slice(1));
	} else {
		valueDriversChartObject['data']['labels'] = labels;
		valueDriversChartObject['data']['datasets'][0]['data'] = mortgage.slice(1);
		valueDriversChartObject['data']['datasets'][1]['data'] = rent.slice(1);	
		valueDriversChartObject['data']['datasets'][2]['data'] = tax_shield.slice(1);
		valueDriversChartObject['data']['datasets'][3]['data'] = appreciation.slice(1);
	};

};

function buildIRRChart(irr, high_irr, low_irr) {

	var labels = [];
	for (var i = 2; i < irr.length; i++) {
		labels.push(i);
	};
	
	//Slice(2) needed as slice (0) is NA and slice(1) is too extreme, want 2->30
	if (Object.keys(irrChartObject).length==0) {
		irrChart(labels, irr.slice(2), high_irr.slice(2), low_irr.slice(2));
	} else {
		irrChartObject['data']['labels'] = labels;
		irrChartObject['data']['datasets'][0]['data'] = irr.slice(2);
		irrChartObject['data']['datasets'][1]['data'] = high_irr.slice(2);
		irrChartObject['data']['datasets'][2]['data'] = low_irr.slice(2);	
	};

};

function buildCashFlowChart(streams) {
	var labels = [];
	var cash_flow = [];
	var cum_cash_flow = [];
	var cum_rent_flow = [];

	var cum_flow = 0;
	var cum_rent = 0;
	for (var i = 0; i < streams.length; i++) {
		labels.push(streams[i].year);

		var rent = streams[i].saved_rent;
		if (i > 0) {
			var rent = (streams[i].saved_rent * -1/1000);
		} else {
			var rent = 0;
		};
		
		var flow = (streams[i].total / 1000) + rent;
		cum_cash_flow.push((flow + cum_flow).toFixed(2));
		
		cum_rent_flow.push((cum_rent + rent).toFixed(2));
		cum_rent = cum_rent + rent;
		cum_flow = cum_flow + flow;
	};

	labels[0] = '0';
	if (Object.keys(cashFlowChartObject).length==0) {
		cashFlowChart(labels, cum_cash_flow, cum_rent_flow);
	} else {
		cashFlowChartObject['data']['labels'] = labels;
		cashFlowChartObject['data']['datasets'][0]['data'] = cum_cash_flow;
		cashFlowChartObject['data']['datasets'][1]['data'] = cum_rent_flow;
	};
	

};

function buildPMTChart(streams) {
	var labels = [];
	var ipmt = [];
	var ppmt = [];

	for (var i = 1; i < streams.length; i++) {
		labels.push(streams[i].year);
		ipmt.push((streams[i].debt_payment * -1/1000).toFixed(2));
		ppmt.push((streams[i].principal_payment * -1/1000).toFixed(2));
	};
	if (Object.keys(cashFlowChartObject).length==0) {
		pmtChart(labels, ppmt, ipmt);
	} else {
		pmtChartObject['data']['labels'] = labels;
		pmtChartObject['data']['datasets'][0]['data'] = ppmt;
		pmtChartObject['data']['datasets'][1]['data'] = ipmt;
	};
	

};
