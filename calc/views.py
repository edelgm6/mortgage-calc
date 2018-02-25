from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from calc.forms import InvestmentForm
from calc.house import House, Mortgage, Investment

class InvestmentView(View): 
	
	form_class = InvestmentForm
	
	def get(self, request, *args, **kwargs):
		
		form = self.form_class(request.GET)
		if form.is_valid():			
			
			price = form.cleaned_data['price']
			yearly_appreciation_rate = form.cleaned_data['yearly_appreciation']
			yearly_property_tax_rate = form.cleaned_data['property_tax']
			yearly_maintenance_as_percent_of_value = form.cleaned_data['maintenance_cost']
			
			house = House(price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value)
			
			yearly_interest_rate = form.cleaned_data['interest_rate']
			term_in_years = 30
			down_payment_percent = form.cleaned_data['down_payment']
			
			mortgage = Mortgage(house, yearly_interest_rate, term_in_years, down_payment_percent)
			
			closing_cost_as_percent_of_value = form.cleaned_data['closing_cost']
			alternative_rent = form.cleaned_data['alternative_rent']
			realtor_cost = form.cleaned_data['realtor_cost']
			
			investment = Investment(house, mortgage, closing_cost_as_percent_of_value, alternative_rent, realtor_cost)
			
			cash_stream = investment.getYearlyCashFlowsAndIRR()
			
			context_dict = {
				'cash_stream': cash_stream
			}
			
			return JsonResponse(context_dict)
		
		return JsonResponse(form.errors)

class IndexView(View): 

	template_name = 'calc/index.html'
	form_class = InvestmentForm
	
	def get(self, request, *args, **kwargs):
		
		context_dict = {'form': self.form_class}
		
		return render(request, self.template_name, context_dict)
	
	
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():			
			
			price = form.cleaned_data['price']
			yearly_appreciation_rate = form.cleaned_data['yearly_appreciation']
			yearly_property_tax_rate = form.cleaned_data['property_tax']
			yearly_maintenance_as_percent_of_value = form.cleaned_data['maintenance_cost']
			
			house = House(price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value)
			
			yearly_interest_rate = form.cleaned_data['interest_rate']
			term_in_years = 30
			down_payment_percent = form.cleaned_data['down_payment']
			
			mortgage = Mortgage(house, yearly_interest_rate, term_in_years, down_payment_percent)
			
			closing_cost_as_percent_of_value = form.cleaned_data['closing_cost']
			alternative_rent = form.cleaned_data['alternative_rent']
			
			investment = Investment(house, mortgage, closing_cost_as_percent_of_value, alternative_rent)
			
			cash_stream = investment.getYearlyCashFlowsAndIRR()
			
			context_dict = {
				'form': form,
				'cash_stream': cash_stream
			}
			
			print(cash_stream)
			
			return render(request, self.template_name, context_dict)
		
		context_dict = {'form': form}
		
		return render(request, self.template_name, context_dict)