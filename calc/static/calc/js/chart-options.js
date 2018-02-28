Chart.defaults.global.defaultFontColor = 'white';
Chart.defaults.global.elements.line.fill = false;
Chart.defaults.global.zeroLineColor = 'white';

const zeroArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];

var primary = '#E4F1FF';
var secondary = '#CCA5A2';
var tertiary = '#D7FFE7';
var irr = $("#irrChart");

function irrChart(labels, base, high, low) {
	var irrChart = new Chart(irr, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'Base appreciation',
				data: base,
				borderColor: primary,
			},
			{
				label: 'High (Base+1%)',
				data: high,
				borderColor: tertiary,
			},
			{
				label: 'Low (Base-1%)',
				data: low,
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
};

var pmt = $("#pmtChart");

function pmtChart(labels, principal, interest) {
	var pmtChart = new Chart(pmt, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'Principal',
				data: principal,
				borderColor: primary,
			},
			{
				label: 'Interest',
				data: interest,
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
};
	
var ctx = $("#cashFlowChart");
function cashFlowChart(labels, own, rent) {
	var cashFlowChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'Own',
				data: own,
				borderColor: primary,
			},
			{
				label: 'Rent',
				data: rent,
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
};