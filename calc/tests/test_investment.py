from django.test import TestCase
from calc.house import House
from calc.mortgage import Mortgage
from calc.investment import Investment
from decimal import Decimal
		
class InvestmentTestCase(TestCase):

	# House variables
	price = 500000
	yearly_property_tax_rate = Decimal(.02)
	yearly_appreciation_rate = Decimal(.05)
	yearly_maintenance_as_percent_of_value = Decimal(.01)
	yearly_insurance_as_percent_of_value = Decimal(.01)
	
	# Mortgage variables
	yearly_interest_rate = Decimal(.05)
	term_in_years = 30
	down_payment_percent = Decimal(.2)
	
	# Investment variables
	realtor_cost_as_percent_of_value = Decimal(.06)
	federal_tax_rate = Decimal(.32)
	state_tax_rate = Decimal(.06)
	closing_cost_as_percent_of_value = Decimal(.03)
	alternative_rent = 1500 * 12
	
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
		
		mortgage = self._create_mortgage()
		investment = Investment(mortgage.house, mortgage, self.closing_cost_as_percent_of_value, self.alternative_rent, self.realtor_cost_as_percent_of_value, self.federal_tax_rate, self.state_tax_rate)
		
		return investment
	
	def test_can_create_investment(self):
		
		investment = self._create_investment()
		
		self.assertEqual(investment.realtor_cost_rate, self.realtor_cost_as_percent_of_value)
		self.assertEqual(investment.federal_tax_rate, self.federal_tax_rate)
		self.assertEqual(investment.state_tax_rate, self.state_tax_rate)
		self.assertEqual(investment.closing_cost_rate, self.closing_cost_as_percent_of_value)
		self.assertEqual(investment.alternative_rent, self.alternative_rent)
	
	def test_get_year_zero_cash_flow_returns_cost_of_equity_plus_closing_costs(self):
		
		investment = self._create_investment()
		
		year_zero_cash_flow = investment._get_year_zero_cash_flow()
		equity_check = investment.starting_equity * -1
		closing_costs = investment.house.price * investment.closing_cost_rate * -1
		self.assertEqual(year_zero_cash_flow, equity_check + closing_costs)
		
	def test_get_sale_proceeds_returns_equity_less_realtor_costs(self):
		
		investment = self._create_investment()
		
		CURRENT_DEBT = -50000
		CURRENT_EQUITY = 50000
		current_value = CURRENT_EQUITY - CURRENT_DEBT
		
		realtor_cost = current_value * self.realtor_cost_as_percent_of_value
		
		self.assertEqual(investment._get_sale_proceeds(CURRENT_DEBT, CURRENT_EQUITY), CURRENT_EQUITY - realtor_cost)
		
	def test_get_interest_tax_benefit_if_debt_over_debt_limit(self):
		
		investment = self._create_investment()
		
		DEBT_VALUE = Decimal(-1000000)
		DEBT_LIMIT = 750000
		INTEREST_PAYMENT = 1000
		
		tax_benefit = investment._get_interest_tax_benefit(DEBT_VALUE, INTEREST_PAYMENT)
		
		multiplier = DEBT_LIMIT / DEBT_VALUE
		tax_rate = investment.federal_tax_rate + investment.state_tax_rate
		
		self.assertEqual(tax_benefit, multiplier * INTEREST_PAYMENT * tax_rate)
		
	def test_get_interest_tax_benefit_if_debt_under_debt_limit(self):
		
		investment = self._create_investment()
		
		DEBT_VALUE = -500000
		DEBT_LIMIT = 750000
		INTEREST_PAYMENT = 1000
		
		tax_benefit = investment._get_interest_tax_benefit(DEBT_VALUE, INTEREST_PAYMENT)
		
		multiplier = -1
		tax_rate = investment.federal_tax_rate + investment.state_tax_rate
		
		self.assertEqual(tax_benefit, multiplier * INTEREST_PAYMENT * tax_rate)
		
	def test_get_property_tax_benefit_if_over_SALT_limit(self):
		
		investment = self._create_investment()
		
		PROPERTY_TAX_BILL = -20000
		
		self.assertEqual(investment._get_property_tax_benefit(PROPERTY_TAX_BILL), 10000 * self.federal_tax_rate)
		
	def test_get_property_tax_benefit_if_umder_SALT_limit(self):
		
		investment = self._create_investment()
		
		PROPERTY_TAX_BILL = -5000
		
		self.assertEqual(investment._get_property_tax_benefit(PROPERTY_TAX_BILL), PROPERTY_TAX_BILL * self.federal_tax_rate * -1)
		
	def test_get_alternative_rent_streams_returns_escalating_rent(self):
		
		investment = self._create_investment()
		
		year_zero_rent = investment._get_future_rent(0)
		year_one_rent = investment._get_future_rent(1)
		year_ten_rent = investment._get_future_rent(10)
		
		self.assertEqual(year_zero_rent, self.alternative_rent)
		self.assertEqual(year_one_rent, self.alternative_rent * (1 + self.yearly_appreciation_rate) ** 1)
		self.assertEqual(round(year_ten_rent), round(self.alternative_rent * (1 + self.yearly_appreciation_rate) ** 10))
		
	def test_get_yearly_cash_flows_and_irr_returns_termainal_irr_value(self):
		
		investment = self._create_investment()
		
		irr, cash_flows = investment.get_yearly_cash_flows_and_irr()
		self.assertEqual(irr[30], 5.37)
		self.assertEqual(irr[0], 'NA')
		self.assertEqual(irr[2], -8.09)
		self.assertEqual(cash_flows[30]['debt'], 0)
		
	def test_get_yearly_cash_flows_and_irr_returns_right_cash_flow_values(self):
		
		investment = self._create_investment()
		
		_, cash_flows = investment.get_yearly_cash_flows_and_irr()

		self.assertEqual(cash_flows[30]['debt'], 0)
		self.assertEqual(cash_flows[0]['debt'], -round(self.price * (1 - self.down_payment_percent)))
		self.assertEqual(cash_flows[30]['equity'], cash_flows[30]['value'])
		self.assertEqual(cash_flows[30]['year'], 30)
		
	def test_get_yearly_cash_flows_and_irr_returns_NA_IRRs(self):
		
		house = self._create_house()
		mortgage = Mortgage(house, self.yearly_interest_rate, self.term_in_years, Decimal(.01))
		investment = Investment(house, mortgage, self.closing_cost_as_percent_of_value, self.alternative_rent, self.realtor_cost_as_percent_of_value, self.federal_tax_rate, self.state_tax_rate)
		
		irr, _ = investment.get_yearly_cash_flows_and_irr()

		self.assertEqual(irr[1], None)
		
	def test_convert_to_readable_string_returns_string(self):
		
		NUMBER = 2156.76
		
		round_integer = Investment._convert_to_round_integer(NUMBER)

		self.assertEqual(round_integer, 2157)
		