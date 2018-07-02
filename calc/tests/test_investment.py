from django.test import TestCase
from calc.house import House, Mortgage, Investment
from decimal import Decimal
		
class InvestmentTestCase(TestCase):
	
	def test_irr(self):
		price = 100000
		yearly_property_tax_rate = .01 
		yearly_appreciation_rate = .05
		yearly_maintenance_as_percent_of_value = .01
		yearly_insurance_as_percent_of_value = .01
		
		house = House(price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value, yearly_insurance_as_percent_of_value)
		yearly_interest_rate = .05
		term_in_years = 30
		down_payment_percent = .20
		
		realtor_cost_as_percent_of_value = .06
		federal_tax_rate = .32
		state_tax_rate = .06
		
		mortgage = Mortgage(house, yearly_interest_rate, term_in_years, down_payment_percent)
		
		closing_cost_as_percent_of_value = .03
		alternative_rent = 2000
		
		investment = Investment(house, mortgage, closing_cost_as_percent_of_value, alternative_rent, realtor_cost_as_percent_of_value, federal_tax_rate, state_tax_rate)
		
		cash_flows = investment.getYearlyCashFlowsAndIRR()
		
		print(cash_flows)