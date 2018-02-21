from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class InvestmentForm(forms.Form):
	price = forms.IntegerField()
	closing_cost = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	maintenance_cost = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	property_tax = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	down_payment = forms.DecimalField(max_value=1, min_value=0, max_digits=3, decimal_places=2)
	interest_rate = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	yearly_appreciation = forms.DecimalField(max_value=1, min_value=0, max_digits=2, decimal_places=2)
	alternative_rent = forms.IntegerField(min_value=0)