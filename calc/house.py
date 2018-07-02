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
		
	def getHomeValueStreams(self):
		base_case = [self.price]
		BASE_GROWTH_RATE = self.yearly_appreciation_rate
		
		for year in range(1,31):
			base_case.append(base_case[year-1] * (1+BASE_GROWTH_RATE))
			
		return base_case