from django.test import TestCase
from calc.house import House
from calc.mortgage import Mortgage
from calc.investment import Investment
from decimal import Decimal
		
class InvestmentTestCase(TestCase):

	# House variables
	price = 500000
	yearly_property_tax_rate = .02 
	yearly_appreciation_rate = .05
	yearly_maintenance_as_percent_of_value = .01
	yearly_insurance_as_percent_of_value = .01
	
	# Mortgage variables
	yearly_interest_rate = .05
	term_in_years = 30
	down_payment_percent = .2
	
	# Investment variables
	realtor_cost_as_percent_of_value = .06
	federal_tax_rate = .32
	state_tax_rate = .06
	closing_cost_as_percent_of_value = .03
	alternative_rent = 1500
	
	# Output based on values generated from this Google Sheet
	# https://docs.google.com/spreadsheets/d/1j4b3ZiP2LsMpawOkTHDcCzCRLOuV2KtaUuEGtLwS4E0/edit?usp=sharing
	
	def _create_house(self):
        
		house = House(self.price, self.yearly_appreciation_rate, self.yearly_property_tax_rate, self.yearly_maintenance_as_percent_of_value, self.yearly_insurance_as_percent_of_value)
		
		return house
	
	def _create_mortgage(self):
		
		house = self._create_house()
		mortgage = Mortgage(house, self.yearly_interest_rate, self.term_in_years, self.down_payment_percent)
		
		return mortgage

	def _create_investment(self):
		
		house = self._create_house()
		mortgage = Mortgage(house, self.yearly_interest_rate, self.term_in_years, self.down_payment_percent)
		investment = Investment(house, mortgage, self.closing_cost_as_percent_of_value, self.alternative_rent, self.realtor_cost_as_percent_of_value, self.federal_tax_rate, self.state_tax_rate)
		
		return investment
	
	def test_can_create_investment(self):
		
		investment = self._create_investment()
		
		self.assertEqual(investment.realtor_cost, self.realtor_cost_as_percent_of_value)
		self.assertEqual(investment.federal_tax_rate, self.federal_tax_rate)
		self.assertEqual(investment.state_tax_rate, self.state_tax_rate)
		self.assertEqual(investment.closing_cost_as_percent_of_value, self.closing_cost_as_percent_of_value)
		self.assertEqual(investment.alternative_rent, self.alternative_rent)
		
	def test_get_value(self):
		
		investment = self._create_investment()
		
		self.assertEqual(investment.getValue(0), self.price)
		self.assertEqual(investment.getValue(1), self.price * (1+self.yearly_appreciation_rate))
		self.assertEqual(investment.getValue(15), self.price * (1+self.yearly_appreciation_rate)**15)
	
	def test_get_year_zero_cash_flow_returns_cost_of_equity_plus_closing_costs(self):
		
		investment = self._create_investment()
		
		year_zero_cash_flow = investment.getYearZeroCashFlow()
		equity_check = investment.starting_equity * -1
		closing_costs = investment.house.price * investment.closing_cost_as_percent_of_value * -1
		self.assertEqual(year_zero_cash_flow, equity_check + closing_costs)
		
	def test_get_average_value_in_year_returns_current_plus_next_divided_by_two(self):
		
		investment = self._create_investment()
		
		CURRENT_VALUE = 100000
		
		next_year_value = CURRENT_VALUE * (1 + self.yearly_appreciation_rate)
		
		self.assertEqual(investment.getAverageValueInYear(CURRENT_VALUE), (CURRENT_VALUE + next_year_value) / 2)
		
	def test_get_sale_proceeds_returns_equity_less_realtor_costs(self):
		
		investment = self._create_investment()
		
		CURRENT_VALUE = 100000
		CURRENT_EQUITY = 50000
		
		realtor_cost = CURRENT_VALUE * self.realtor_cost_as_percent_of_value
		
		self.assertEqual(investment.getSaleProceeds(CURRENT_VALUE, CURRENT_EQUITY), CURRENT_EQUITY - realtor_cost)
		
	def test_get_interest_tax_benefit_if_debt_over_debt_limit(self):
		
		investment = self._create_investment()
		
		DEBT_VALUE = -1000000
		DEBT_LIMIT = 750000
		INTEREST_PAYMENT = 1000
		
		tax_benefit = investment.getInterestTaxBenefit(DEBT_VALUE, INTEREST_PAYMENT)
		
		multiplier = DEBT_LIMIT / DEBT_VALUE
		tax_rate = investment.federal_tax_rate + investment.state_tax_rate
		
		self.assertEqual(tax_benefit, multiplier * INTEREST_PAYMENT * tax_rate)
		
		