from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from calc.forms import InvestmentForm
from calc.house import House
from calc.mortgage import Mortgage
from calc.investment import Investment
from decimal import Decimal
import copy

class AboutView(View):
	
	template_name = 'calc/about.html'
	
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	
class IndexView(View): 

	template_name = 'calc/index.html'
	form_class = InvestmentForm
	
	def get(self, request, *args, **kwargs):
		
		float_parameters = ['closing_cost', 'maintenance_cost', 'property_tax', 'down_payment', 'interest_rate', 'yearly_appreciation', 'realtor_cost', 'federal_tax_bracket', 'state_tax_bracket', 'insurance']
		
		context_dict = {}
		
		for parameter in float_parameters:
			if parameter in request.GET:
				try:
					context_dict[parameter] = float(request.GET[parameter])
				except:
					pass
				
		int_parameters = ['price', 'alternative_rent']
		
		for parameter in int_parameters:
			if parameter in request.GET:
				try:
					context_dict[parameter] = int(request.GET[parameter])
				except:
					pass
		
		return render(request, self.template_name, context_dict)
	

class InvestmentView(View): 
	
	no_leverage = {
		'yearly_interest_rate': 0,
		'down_payment_percent': 1,
		'name': 'mortgage_driver_irr'
	}

	no_alternative_rent = {
		'alternative_rent': 0,
		'name': 'alternative_rent_driver_irr'
	}

	no_tax_shield = {
		'state_tax_rate': 0,
		'federal_tax_rate': 0,
		'name': 'tax_shield_driver_irr'
	}

	no_appreciation = {
		'yearly_appreciation_rate': 0,
		'name': 'appreciation_driver_irr'
	}

	no_expenses = {
		'yearly_property_tax_rate': 0,
		'yearly_maintenance_as_percent_of_value': 0, 
		'insurance': 0,
		'closing_cost_as_percent_of_value': 0,
		'name': 'expenses_driver_irr'
	}

	other_scenarios = [
		no_leverage,
		no_alternative_rent,
		no_tax_shield,
		no_appreciation,
		no_expenses
	]
	
	@staticmethod
	def buildInvestment(scenario):
		TERM_IN_YEARS = 30
		
		house = House(
			scenario['price'], 
			scenario['yearly_appreciation_rate'], 
			scenario['yearly_property_tax_rate'], 
			scenario['yearly_maintenance_as_percent_of_value'], 
			scenario['insurance']
		)
		
		mortgage = Mortgage(
			house, 
			scenario['yearly_interest_rate'], 
			TERM_IN_YEARS, 
			scenario['down_payment_percent']
		)	
		
		investment = Investment(
			house, 
			mortgage, 
			scenario['closing_cost_as_percent_of_value'], 
			scenario['alternative_rent'], 
			scenario['realtor_cost'], 
			scenario['federal_tax_rate'], 
			scenario['state_tax_rate']
		)
		
		return investment
	
	@staticmethod
	def get_unified_scenario(comprehensive_scenario, modified_scenario):
		unified_scenario = copy.deepcopy(comprehensive_scenario)
		
		for var, value in modified_scenario.items():
			unified_scenario[var] = value
			
		return unified_scenario

	@staticmethod
	def getIRRDelta(base_irr, alternative_irr):
		irr_delta = []
		for year in range(1, len(base_irr)):
			# Handles case where one of the IRRs is null due to no positive cash flows
			try:
				delta =  base_irr[year] - alternative_irr[year]
				irr_delta.append(round(delta,2))
			except TypeError:
				irr_delta.append(None)
		
		return irr_delta
		
	
	def get(self, request, *args, **kwargs):

		form = InvestmentForm(request.GET)
		if form.is_valid():				
			
			standard_investment = {
				'price': form.cleaned_data['price'],
				'yearly_appreciation_rate': form.cleaned_data['yearly_appreciation'],
				'yearly_property_tax_rate': form.cleaned_data['property_tax'],
				'yearly_maintenance_as_percent_of_value': form.cleaned_data['maintenance_cost'],
				'insurance': form.cleaned_data['insurance'],
				'yearly_interest_rate': form.cleaned_data['interest_rate'],
				'down_payment_percent': form.cleaned_data['down_payment'],
				'closing_cost_as_percent_of_value': form.cleaned_data['closing_cost'],
				'alternative_rent': form.cleaned_data['alternative_rent'] * 12,
				'realtor_cost': form.cleaned_data['realtor_cost'],
				'federal_tax_rate': form.cleaned_data['federal_tax_bracket'],
				'state_tax_rate': form.cleaned_data['state_tax_bracket'],		
			}

			# Base stream
			investment = self.buildInvestment(standard_investment)
			base_irr, cash_stream = investment.getYearlyCashFlowsAndIRR()
			mortgage_payment = int(round(investment.mortgage.getMonthlyPayment()))
			context_dict = {
				'base_irr': base_irr,
				'cash_stream': cash_stream,
				'mortgage_payment': mortgage_payment
			}

			high_appreciation = {
				'yearly_appreciation_rate': standard_investment['yearly_appreciation_rate'] + Decimal(.01),
			}
			
			low_appreciation = {
				'yearly_appreciation_rate': standard_investment['yearly_appreciation_rate'] - Decimal(.01),
			}
			
			scenario = self.get_unified_scenario(standard_investment, high_appreciation)
			investment = self.buildInvestment(scenario)
			high_irr, _ = investment.getYearlyCashFlowsAndIRR()
			context_dict['high_irr'] = high_irr
			
			scenario = self.get_unified_scenario(standard_investment, low_appreciation)
			investment = self.buildInvestment(scenario)
			low_irr, _ = investment.getYearlyCashFlowsAndIRR()
			context_dict['low_irr'] = low_irr
			
			for scenario in self.other_scenarios:
				unified_scenario = self.get_unified_scenario(standard_investment, scenario)
				investment = self.buildInvestment(unified_scenario)
				scenario_irr, _ = investment.getYearlyCashFlowsAndIRR()
				irr_delta = self.getIRRDelta(base_irr, scenario_irr)
				context_dict[scenario['name']] = irr_delta
			
			return JsonResponse(context_dict)
		else:
			print(form.errors)
		
		return JsonResponse(form.errors, status=400)