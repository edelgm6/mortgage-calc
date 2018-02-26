from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from decimal import Decimal

class InvestmentForm(forms.Form):
	
	FEDERAL_TAX_RATE = (
		('.1', ('10% - Income $9,525/$19,050 Single/Married')),
		('.12', ('12% - Income $38,700/$77,400 Single/Married')),
		('.22', ('22% - Income $82,500/$165,000 Single/Married')),
		('.24', ('24% - Income $157,500/$315,000 Single/Married')),
		('.32', ('32% - Income $200,000/$400,000 Single/Married')),
		('.35', ('35% - Income $500,000/$600,000 Single/Married')),
		('.37', ('37% - Income $500,000+/$600,000+ Single/Married')),
	)
	
	price = forms.IntegerField()
	closing_cost = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	maintenance_cost = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	property_tax = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	down_payment = forms.DecimalField(max_value=1, min_value=0, max_digits=3, decimal_places=2)
	interest_rate = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	yearly_appreciation = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	alternative_rent = forms.IntegerField(min_value=0)
	realtor_cost = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	federal_tax_bracket = forms.ChoiceField(choices=FEDERAL_TAX_RATE, initial=.24)
	state_tax_bracket = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	
	def clean_federal_tax_bracket(self):
		data = self.cleaned_data['federal_tax_bracket']
		return Decimal(data)
	
	def clean_state_tax_bracket(self):
		data = self.cleaned_data['state_tax_bracket']
		return Decimal(data)