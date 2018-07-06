from django.test import TestCase
from calc.forms import InvestmentForm

class InvestmentFormTest(TestCase):
	
	def test_form_is_valid_with_valid_data(self):
		
		form_data = {
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
		
		form = InvestmentForm(data=form_data)
		self.assertTrue(form.is_valid())