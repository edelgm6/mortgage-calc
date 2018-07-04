from django.test import RequestFactory, TestCase
from calc.house import House
from calc.mortgage import Mortgage
from calc.investment import Investment
from calc.views import AboutView, IndexView

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
		
