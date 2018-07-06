from django.test import TestCase
from calc.house import House
from decimal import Decimal

class HouseTestCase(TestCase):

	price = 500000
	yearly_property_tax_rate = .02 
	yearly_appreciation_rate = .05
	yearly_maintenance_as_percent_of_value = .01
	yearly_insurance_as_percent_of_value = .01
	
	def _create_house(self):
        
		house = House(self.price, self.yearly_appreciation_rate, self.yearly_property_tax_rate, self.yearly_maintenance_as_percent_of_value, self.yearly_insurance_as_percent_of_value)
		
		return house
	
	def test_can_create_house(self):
		house = self._create_house()
		
		self.assertEqual(house.price, self.price)
		self.assertEqual(house.yearly_property_tax_rate, self.yearly_property_tax_rate)
		self.assertEqual(house.yearly_appreciation_rate, self.yearly_appreciation_rate)
		self.assertEqual(house.yearly_maintenance_as_percent_of_value, self.yearly_maintenance_as_percent_of_value)
		self.assertEqual(house.yearly_insurance_as_percent_of_value, self.yearly_insurance_as_percent_of_value)
		
	def test_get_home_value_streams_returns_start_and_end_values(self):
		
		house = self._create_house()
		year_zero_value = house.get_future_value(0)
		
		self.assertEqual(year_zero_value, self.price)
		
		year_thirty_value = house.get_future_value(30)
		
		last_value = self.price * (1+self.yearly_appreciation_rate)**30
		self.assertEqual(round(last_value), round(year_thirty_value))
		