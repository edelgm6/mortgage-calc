var first_click = true;

//$('#calculate').click(function () {
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
	
	//$.get('stream/', get_data, function (data) {
	$.ajax({
		method: 'GET',
		url: 'stream/',
		data: get_data
	})
	.done(function (data) {

		var get_url = ("?price=" + get_data['price'] + "&closing_cost=" + get_data['closing_cost'] + "&maintenance_cost=" + get_data['maintenance_cost'] + "&property_tax=" + get_data['property_tax'] + "&down_payment=" + get_data['down_payment'] + "&interest_rate=" + get_data['interest_rate'] + "&yearly_appreciation=" + get_data['yearly_appreciation'] + "&alternative_rent=" + get_data['alternate_rent'] + "&realtor_cost=" + get_data['realtor_cost'] + "&federal_tax_bracket=" + get_data['federal_tax_bracket'] + "&state_tax_bracket=" + get_data['state_tax_bracket'] + "&insurance=" + get_data['insurance'])
		window.history.pushState("object or string", "Mortgage ROI", "/" + get_url);
		
		var mortgage_payment = convertNumberToString(data.mortgage_payment * -1);
		$('#mortgage_payment').text(mortgage_payment);
		$('#rent_payment').text($('#id_alternative_rent').val())
		
		var table_body = $('#tbody');
		var response = data.cash_stream;
		var first_year_ppmt_greater_than_ipmt = false;
		var first_year_positive_cash_flow = false;
		var peak_irr = -100.00;
		var peak_irr_year = 0;
		$.each(response, function (key, value) {
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
				if (value.irr > peak_irr) {
					peak_irr = value.irr;
					peak_irr_year = value.year;
				};
			};

			/*
			if (!first_year_positive_cash_flow && value.year != 'Purchase') {
				var cash_flow = value.total;
				if (cash_flow > 0) {
					first_year_positive_cash_flow = true;
					$('#first_year_positive_cash_flow').text(value.year);
				};
			};
			*/

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
			//console.log(peak_irr);
			$('#peak_irr').text(peak_irr);
			$('#sell_year').text(peak_irr_year);
			
			buildIRRChart(response);
			buildPMTChart(response);
			buildCashFlowChart(response);
			if (Object.keys(irrChartObject).length>0) {
				irrChartObject.update();
				pmtChartObject.update();
				cashFlowChartObject.update();	
			};
			$('#thead').fadeIn(1000);
			$('.takeaways-content').fadeIn(1000);
			if (first_click) {
				$(window).scrollTo('#takeaways', 800);
				first_click = false;
			};	
			/*
			$(".mortgage").each(function (index) {
				$(this).delay(150 * index).fadeIn(1000);
			});
			*/
			$(".mortgage").fadeIn(1000);
		}, 3000);	


	});
});

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

function buildIRRChart(streams) {

	var labels = [];
	var data = [];
	var high_data = [];
	var low_data = [];

	for (var i = 2; i < streams.length; i++) {
		labels.push(streams[i].year);
		data.push(streams[i].irr);
		high_data.push(streams[i].high_irr);
		low_data.push(streams[i].low_irr);
	};
	
	if (Object.keys(irrChartObject).length==0) {
		irrChart(labels, data, high_data, low_data);
	} else {
		irrChartObject['data']['labels'] = labels;
		irrChartObject['data']['datasets'][0]['data'] = data;
		irrChartObject['data']['datasets'][1]['data'] = high_data;
		irrChartObject['data']['datasets'][2]['data'] = low_data;	
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
		
		/*
		console.log('year' + streams[i].year)
		console.log('rent' + rent)
		console.log('flow' + flow)
		console.log('cumrent' + cum_rent_flow[i])
		console.log('cumown' + cum_cash_flow[i])
		*/
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
