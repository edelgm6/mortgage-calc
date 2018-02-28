Chart.defaults.global.defaultFontColor = 'white';
Chart.defaults.global.elements.line.fill = false;
Chart.defaults.global.zeroLineColor = 'white';

const zeroArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

var primary = '#E4F1FF';
//var secondary = '#4B7199';
//var secondary = '#FFB8A4';
var secondary = '#CCA5A2';
var tertiary = '#D7FFE7';
var ctx = $("#irrChart");
var irrChart = new Chart(ctx, {
	type: 'line',
	data: {
		labels: [],
		datasets: [{
			label: 'Base appreciation',
			data: zeroArray,
			borderColor: primary,
		},
		{
			label: 'High (Base+1%)',
			data: zeroArray,
			borderColor: tertiary,
		},
		{
			label: 'Low (Base-1%)',
			data: zeroArray,
			borderColor: secondary,
		}],
	},
	options: {
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
			borderColor: primary,
		},
		{
			label: 'Interest',
			data: [],
			borderColor: secondary,
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
						return '$' + value + 'K';
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
		//	label: 'Cash flow',
		//	data: [],
		//	borderColor: 'blue',
		//},
		//{
			label: 'Own',
			data: [],
			borderColor: primary,
		},
		{
			label: 'Rent',
			data: [],
			borderColor: secondary,
		}],
	},
	options: {
		scales: {
			yAxes: [{
				scaleLabel: {
					display: true,
					labelString: 'Cumulative spend',

				},
				gridLines: {
					color: 'lightgray',
					zeroLineColor: 'white',
				},
				ticks: {
					callback: function(value, index, values) {
						return '$' + value + 'K';
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