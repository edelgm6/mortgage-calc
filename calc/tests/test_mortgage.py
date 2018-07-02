from django.test import TestCase
from calc.house import House
from calc.mortgage import Mortgage
from decimal import Decimal

class MortgageTestCase(TestCase):

	
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
	
	# Output based on values generated from this Google Sheet
	# https://docs.google.com/spreadsheets/d/1j4b3ZiP2LsMpawOkTHDcCzCRLOuV2KtaUuEGtLwS4E0/edit?usp=sharing
	
	def _create_house(self):
        
		house = House(self.price, self.yearly_appreciation_rate, self.yearly_property_tax_rate, self.yearly_maintenance_as_percent_of_value, self.yearly_insurance_as_percent_of_value)
		
		return house
	
	def _create_mortgage(self):
		
		house = self._create_house()
		mortgage = Mortgage(house, self.yearly_interest_rate, self.term_in_years, self.down_payment_percent)
		
		return mortgage
	
	def test_can_create_mortgage(self):
		
		mortgage = self._create_mortgage()
		
		self.assertEqual(mortgage.term_in_years, self.term_in_years)
		self.assertEqual(mortgage.yearly_interest_rate, self.yearly_interest_rate)
		
	def test_mortgage_amount_equals_house_price_less_down_payment_amount(self):
		
		mortgage = self._create_mortgage()
		
		self.assertEqual(mortgage.mortgage_amount, self.price * (1 - self.down_payment_percent))
		
	def test_down_payment_amount_equals_house_price_times_down_payment_percent(self):
		
		mortgage = self._create_mortgage()
		
		self.assertEqual(mortgage.down_payment_amount, self.price * self.down_payment_percent)
		
	def test_get_yearly_payment_returns_26021_with_interest(self):
	
		mortgage = self._create_mortgage()
		
		self.assertEqual(round(mortgage.getYearlyPayment()), -26021)
		
	def test_get_principal_payment_returns_correct_amounts(self):
		
		mortgage = self._create_mortgage()
		
		self.assertEqual(round(mortgage.getPrincipalPayment(1)), -6021)
		self.assertEqual(round(mortgage.getPrincipalPayment(30)), -24781)
		self.assertEqual(round(mortgage.getPrincipalPayment(15)), -11920)
		
	def test_get_interest_payment_returns_correct_amounts(self):
		
		mortgage = self._create_mortgage()
		
		self.assertEqual(round(mortgage.getInterestPayment(1)), -20000)
		self.assertEqual(round(mortgage.getInterestPayment(30)), -1239)
		self.assertEqual(round(mortgage.getInterestPayment(15)), -14100)
		
	def test_get_interest_payment_returns_0_if_rate_is_0(self):
		
		mortgage = self._create_mortgage()
		mortgage.yearly_interest_rate = 0
		
		self.assertEqual(round(mortgage.getInterestPayment(1)), 0)
		self.assertEqual(round(mortgage.getInterestPayment(30)), 0)
		self.assertEqual(round(mortgage.getInterestPayment(15)), 0)
		
	def test_get_pmi_insurance_returns_0_if_debt_less_than_80pct_of_purchase(self):
		
		mortgage = self._create_mortgage()
		debt = -.5 * self.price
		
		self.assertEqual(mortgage.getPMIPayment(debt), 0)
		
	def test_get_pmi_insurance_returns_1pct_of_debt_if_debt_more_than_80pct_of_purchase(self):
		
		mortgage = self._create_mortgage()
		debt = -.9 * self.price
		
		self.assertEqual(round(mortgage.getPMIPayment(Decimal(debt))), round(.01 * debt))
		
		