Chart.defaults.global.defaultFontColor = 'white';
Chart.defaults.global.elements.line.fill = false;
Chart.defaults.global.zeroLineColor = 'white';

var ctx = $("#irrChart");
var irrChart = new Chart(ctx, {
	type: 'line',
	data: {
		labels: [],
		datasets: [{
			label: 'IRR',
			data: [],
			borderColor: 'white',
		}],
	},
	options: {
		legend: {
			display: false,
		},
		scales: {
			yAxes: [{
				scaleLabel: {
					display: true,
					labelString: 'Annualized return',

				},
				gridLines: {
					color: 'lightgray',
					zeroLineColor: 'white',
				},
				ticks: {
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
			}],
		},
	},
});

var ctx = $("#pmtChart");
var pmtChart = new Chart(ctx, {
	type: 'line',
	data: {
		labels: [],
		datasets: [{
			label: 'Principal',
			data: [],
			borderColor: 'green',
		},
		{
			label: 'Interest',
			data: [],
			borderColor: 'darkred',
		}],
	},
	options: {
		scales: {
			yAxes: [{
				scaleLabel: {
					display: true,
					labelString: 'Payment',

				},
				gridLines: {
					color: 'lightgray',
					zeroLineColor: 'white',
				},
				ticks: {
					callback: function(value, index, values) {
						return '$' + value;
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
			}],
		},
	},
});

var ctx = $("#cashFlowChart");
var cashFlowChart = new Chart(ctx, {
	type: 'line',
	data: {
		labels: [],
		datasets: [{
			label: 'Cash flow',
			data: [],
			borderColor: 'blue',
		},
		{
			label: 'Cumulative cash flow',
			data: [],
			borderColor: 'black',
		}],
	},
	options: {
		scales: {
			yAxes: [{
				scaleLabel: {
					display: true,
					labelString: 'Payment',

				},
				gridLines: {
					color: 'lightgray',
					zeroLineColor: 'white',
				},
				ticks: {
					callback: function(value, index, values) {
						return '$' + value;
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
			}],
		},
	},
});