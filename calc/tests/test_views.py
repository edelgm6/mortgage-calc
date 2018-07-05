from django.test import RequestFactory, TestCase
from calc.house import House
from calc.mortgage import Mortgage
from calc.investment import Investment
from calc.views import AboutView, IndexView, InvestmentView
import json

class AboutViewTest(TestCase):
	def setUp(self):
		
		self.factory = RequestFactory()
		
	def test_view_returns_200(self):
		
		request = self.factory.get('/about')
		response = AboutView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		
		
class IndexViewTest(TestCase):
	def setUp(self):
		
		self.factory = RequestFactory()
		
	def test_view_returns_200_without_parameter(self):
		
		request = self.factory.get('/')
		response = IndexView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		
	def test_view_returns_200_with_parameters(self):
		
		get_parameters = {
			'closing_cost': .03, 
			'maintenance_cost': .01, 
			'property_tax': .01, 
			'down_payment': .2, 
			'interest_rate': 'whatever', #tests the except: portion of the try/except blocks 
			'yearly_appreciation': .05, 
			'realtor_cost': .06, 
			'federal_tax_bracket': .32, 
			'state_tax_bracket': .06, 
			'insurance': .01, 
			'price': 500000, 
			'alternative_rent': 'whatever', #tests the except: portion of the try/except blocks
		}
		
		request = self.factory.get('/', get_parameters)
		response = IndexView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		
class InvestmentViewTest(TestCase):
	# Output based on values generated from this Google Sheet
	# https://docs.google.com/spreadsheets/d/1j4b3ZiP2LsMpawOkTHDcCzCRLOuV2KtaUuEGtLwS4E0/edit?usp=sharing
	
	def setUp(self):
		
		self.factory = RequestFactory()
		
	def test_view_returns_400_without_parameters(self):
		
		request = self.factory.get('/stream')
		response = InvestmentView.as_view()(request)
		self.assertEqual(response.status_code, 400)
	
	
	def test_view_returns_200_with_parameters(self):

		get_parameters = {
			'closing_cost': 3.0, 
			'maintenance_cost': 1.0, 
			'property_tax': 2.0, 
			'down_payment': 20.0, 
			'interest_rate': 5.0,
			'yearly_appreciation': 5.0, 
			'realtor_cost': 6.0, 
			'federal_tax_bracket': '.32', 
			'state_tax_bracket': 6.0, 
			'insurance': 1.0, 
			'price': 500000, 
			'alternative_rent': 1500,
		}
		
		request = self.factory.get('/stream', get_parameters)
		response = InvestmentView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		
		response_dict = json.loads(response.content)
		self.assertEqual(response_dict['base_irr'][30], 5.37)
		self.assertEqual(response_dict['base_irr'][2], -8.09)
		print(response_dict['high_irr'])
		self.assertEqual(response_dict['high_irr'][30], 6.71)
		self.assertEqual(response_dict['high_irr'][2], -3.86)
		self.assertEqual(response_dict['low_irr'][30], 3.96)
		self.assertEqual(response_dict['low_irr'][2], -12.46)
		
		# Comparison IRRs don't have the year 0 IRR of NA, so have to use 1/29 instead of 2/30
		print(response_dict['mortgage_driver_irr'])
		self.assertEqual(response_dict['mortgage_driver_irr'][29], 0.76)
		self.assertEqual(response_dict['mortgage_driver_irr'][1], -8.61)
		self.assertEqual(response_dict['alternative_rent_driver_irr'][29], 5.31)
		self.assertEqual(response_dict['alternative_rent_driver_irr'][1], 15.87)
		self.assertEqual(response_dict['tax_shield_driver_irr'][29], 1.43)
		self.assertEqual(response_dict['tax_shield_driver_irr'][1], 8.99)
		self.assertEqual(response_dict['appreciation_driver_irr'][29], 8.16)
		self.assertEqual(response_dict['appreciation_driver_irr'][1], 23.84)
		self.assertEqual(response_dict['expenses_driver_irr'][29], -8.15)
		self.assertEqual(response_dict['expenses_driver_irr'][1], -22.71)
