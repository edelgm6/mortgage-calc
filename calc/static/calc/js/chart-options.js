Chart.defaults.global.defaultFontColor = 'white';
Chart.defaults.global.elements.line.fill = false;
Chart.defaults.global.zeroLineColor = 'white';

var primary = '#E4F1FF';
var secondary = '#CCA5A2';
var tertiary = '#D7FFE7';

var valueDrivers = $("#valueDriversChart");
var valueDriversChartObject = {};
function valueDriversChart(labels, mortgage, rent) {
	valueDriversChartObject = new Chart(valueDrivers, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'Mortgage',
				data: mortgage,
				borderColor: primary,
			},
			{
				label: 'Avoided rent',
				data: rent,
				borderColor: tertiary,
			}],
		},
		options: {
			maintainAspectRatio: false,
			scales: {
				yAxes: [{
					scaleLabel: {
						display: true,
						labelString: 'Annualized return gain/loss',

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


var irr = $("#irrChart");
var irrChartObject = {};
function irrChart(labels, base, high, low) {
	irrChartObject = new Chart(irr, {
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
			maintainAspectRatio: false,
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
var pmtChartObject = {};
function pmtChart(labels, principal, interest) {
	pmtChartObject = new Chart(pmt, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'Principal',
				data: principal,
				borderColor: tertiary,
			},
			{
				label: 'Interest',
				data: interest,
				borderColor: secondary,
			}],
		},
		options: {
			maintainAspectRatio: false,
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
	
var cash = $("#cashFlowChart");
var cashFlowChartObject = {};
function cashFlowChart(labels, own, rent) {
	cashFlowChartObject = new Chart(cash, {
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
			maintainAspectRatio: false,
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