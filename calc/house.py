import numpy
from decimal import Decimal
import math

class House:
	"""Respresentation of the investment's asset.
	
	Attributes:
		price (int): Asset purchase price in dollars, no cents.
		yearly_appreciation_rate (Decimal): Yearly value growth rate of the asset.
		yearly_property_tax_rate (Decimal): Yearly property tax rate as a % of 
			the asset value.
		yearly_maintenance_rate (Decimal): Yearly cost of maintenance 
			as a % of the asset value.
		yearly_insurance_rate (Decimal): Yearly cost of insurance as 
			a % of the asset value.
	"""
	
	def __init__(self, price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value, yearly_insurance_as_percent_of_value):
		self.price = price
		self.yearly_appreciation_rate = yearly_appreciation_rate
		self.yearly_property_tax_rate = yearly_property_tax_rate
		self.yearly_maintenance_rate = yearly_maintenance_as_percent_of_value
		self.yearly_insurance_rate = yearly_insurance_as_percent_of_value
		
	def get_future_value(self, year):
		"""Return future value of the asset given number of years after purchase.
		
		Args:
			year (int): Number of years after the purchase of the asset.
			
		Returns:
			Decimal: Future value of the asset.
		
		"""
		growth_rate = self.yearly_appreciation_rate
			
		return Decimal(self.price * ((1 + growth_rate) ** year))