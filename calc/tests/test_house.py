from django.test import TestCase
from calc.house import House, Mortgage, Investment
from decimal import Decimal

class HouseTestCase(TestCase):
	
	def test_can_create_house(self):
		price = 100000
		yearly_property_tax_rate = .02 
		yearly_appreciation_rate = .05
		yearly_maintenance_as_percent_of_value = .01
		yearly_insurance_as_percent_of_value = .01
        
		house = House(price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value, yearly_insurance_as_percent_of_value)
		
		self.assertEqual(house.price, price)
		self.assertEqual(house.yearly_property_tax_rate, yearly_property_tax_rate)
		self.assertEqual(house.yearly_appreciation_rate, yearly_appreciation_rate)
		self.assertEqual(house.yearly_maintenance_as_percent_of_value, yearly_maintenance_as_percent_of_value)
		self.assertEqual(house.yearly_insurance_as_percent_of_value, yearly_insurance_as_percent_of_value)