$('#calculate').click(function() {
	$.get('stream/', {price: '100000', closing_cost: '.03', maintenance_cost: '.02', property_tax: '.01', down_payment: '.2', interest_rate: '.05', yearly_appreciation: '.06', alternative_rent: '2000'}, function(data) {
        alert(JSON.stringify(data));
		var table_body = $('#tbody');
		var response = data.cash_stream;
		$.each(response, function(key,value) {
			var $tr = $("<tr>", {'class': 'mortgage', 'style': 'display:none;'});
			$(table_body).append(($tr)
				.append($('<td>')
					.text(value.year)
				)
				.append($('<td>')
					.text(value.principal_payment)
				)
				.append($('<td>')
					.text(value.debt_payment)
				)
				.append($('<td>')
					.text(value.other_costs)
				)
				.append($('<td>')
					.text(value.saved_rent)
				)
				.append($('<td>')
					.text(value.total)
				)
				.append($('<td>')
					.text(value.value)
				)
				.append($('<td>')
					.text(value.debt)
				)
				.append($('<td>')
					.text(value.equity)
				)
				.append($('<td>')
					.text(value.irr)
				)
			)
		});
		$(".mortgage").each(function(index) {
			$(this).delay(150 * index).fadeIn(1000);
		});
	});
});