from fredapi import Fred
from django.test import TestCase

class APITestCase(TestCase):

	def test_key(self):
		
		API_KEY = '32671d3a69acf1397ebf0fdb75ab6ef9'
		CASE_SCHILLER = 'SFXRSA'
		fred = Fred(api_key=API_KEY)
		data = fred.get_series(CASE_SCHILLER)

