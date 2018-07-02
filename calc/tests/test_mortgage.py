from django.test import TestCase
from calc.house import House, Mortgage, Investment
from decimal import Decimal

class MortgageTestCase(TestCase):
	
	def test_can_create_mortgage(self):
		price = 100000
		yearly_property_tax_rate = .01 
		yearly_appreciation_rate = .05
		yearly_maintenance_as_percent_of_value = .01
		yearly_insurance_as_percent_of_value = .01
		
		house = House(price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value, yearly_insurance_as_percent_of_value)
		yearly_interest_rate = .05
		term_in_years = 30
		down_payment_percent = .2
		
		mortgage = Mortgage(house, yearly_interest_rate, term_in_years, down_payment_percent)
		
		self.assertEqual(mortgage.down_payment_amount, 20000)
		
		payment = mortgage.monthly_payment
		self.assertEqual(str(int(payment)), '-429')
		