$('#calculate').click(function() {
	$('.overlay').show(); 
	
	$('.mortgage').remove();
	
	$.get('stream/', {price: '100000', closing_cost: '.03', maintenance_cost: '.02', property_tax: '.01', down_payment: '.2', interest_rate: '.05', yearly_appreciation: '.06', alternative_rent: '6000'}, function(data) {
		var table_body = $('#tbody');
		var response = data.cash_stream;
		var first_year_ppmt_greater_than_ipmt = false;
		var first_year_positive_cash_flow = false;
		buildChart(response);
		$.each(response, function(key,value) {
			var $tr = $("<tr>", {'class': 'mortgage', 'style': 'display:none;'});
			var $td_year = $("<td>", {'text': value.year});
			var $td_principal_payment = $("<td>", {'text': value.principal_payment});
			var $td_debt_payment = $("<td>", {'text': value.debt_payment});
			var $td_other_costs = $("<td>", {'text': value.other_costs});
			var $td_saved_rent = $("<td>", {'text': value.saved_rent});
			var $td_total = $("<td>", {'text': value.total});
			var $td_value = $("<td>", {'text': value.value});
			var $td_debt = $("<td>", {'text': value.debt});
			var $td_equity = $("<td>", {'text': value.equity});
			var $td_irr = $("<td>", {'text': value.irr});
			
			if (value.year == 5) {
				$('#year_5_irr').text(value.irr);
			} else if (value.year == 10) {
				$('#year_10_irr').text(value.irr);
			} else if (value.year == 20) {
				$('#year_20_irr').text(value.irr);
			} else if (value.year == 30) {
				$('#year_30_irr').text(value.irr);
			};
			
			if (!first_year_ppmt_greater_than_ipmt && value.year != 'Purchase') {
				var ppmt = Number(value.principal_payment.replace(/,/g, ''));
				var ipmt = Number(value.debt_payment.replace(/,/g, ''));
				
				if (ppmt < ipmt) {
					first_year_ppmt_greater_than_ipmt = true;
					$('#first_year_ppmt_greater_than_ipmt').text(value.year);
				};
			};
			
			if (!first_year_positive_cash_flow && value.year != 'Purchase') {
				var cash_flow = Number(value.total.replace(/,/g, ''));
				if (cash_flow > 0) {
					first_year_positive_cash_flow = true;
					$('#first_year_positive_cash_flow').text(value.year);
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
			
			$($tr).children().each(function() {
				if($(this).text().indexOf("-") >= 0) {
					$(this).addClass("text-danger");
				};
			});
		});
		setTimeout(function(){
			$('.overlay').removeAttr('style');
			$('#takeaways').fadeIn(1000);
			$('#thead').fadeIn(1000);
			$(".mortgage").each(function(index) {
				$(this).delay(150 * index).fadeIn(1000);
			});
		},3000); 
		

	});
});

function buildChart(streams) {
	
	var labels = [];
	var data = [];
	
	for (var i=1; i < streams.length; i++) {
		labels.push(streams[i].year);
		data.push(streams[i].irr.replace('%', ''));
	}
	
	var ctx = $("#myChart");
	var myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'IRR',
				data: data,
				borderColor: 'white',
			}],
		},
		options: {
			legend: {
				display: false,
			},
			title: {
				display: false,
				text: 'Annualized return by year',
				fontColor: 'white',
			},
			scales: {
				yAxes: [{
					scaleLabel: {
						display: true,
						labelString: 'Annualized return',
						fontColor: 'white',
					},
					gridLines: {
						color: 'white',
					},
					ticks: {
						fontColor: 'white',
						callback: function(value, index, values) {
							return value + '%';
						},
					}
				}],
				xAxes: [{
					scaleLabel: {
						display: true,
						labelString: 'Years since purchase',
						fontColor: 'white',
					},
					gridLines: {
						color: 'transparent',
					},
					ticks: {
						fontColor: 'white',
					}
				}],
			},
		},
	});
};