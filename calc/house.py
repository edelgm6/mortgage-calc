import numpy
from decimal import Decimal
import math

class House:
	def __init__(self, price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value, yearly_insurance_as_percent_of_value):
		self.price = price
		self.yearly_appreciation_rate = yearly_appreciation_rate
		self.yearly_property_tax_rate = yearly_property_tax_rate
		self.yearly_maintenance_as_percent_of_value = yearly_maintenance_as_percent_of_value
		self.yearly_insurance_as_percent_of_value = yearly_insurance_as_percent_of_value
		
	def get_future_value(self, year):
		growth_rate = self.yearly_appreciation_rate
			
		return Decimal(self.price * ((1 + growth_rate) ** year))