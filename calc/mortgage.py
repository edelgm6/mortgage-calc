import numpy
from decimal import Decimal
import math

class Mortgage:
	def __init__(self, house, yearly_interest_rate, term_in_years, down_payment_percent):
		self.house = house
		self.yearly_interest_rate = yearly_interest_rate
		self.term_in_years = term_in_years
		self.down_payment_amount = self.house.price * down_payment_percent
		self.mortgage_amount = self.house.price - self.down_payment_amount
		self.monthly_payment = self.getMonthlyPayment()
	
	def getMonthlyPayment(self):
		monthly_rate = self.yearly_interest_rate / 12
		months = self.term_in_years * 12
		mortgage_amount = self.mortgage_amount
		return numpy.pmt(monthly_rate, months, mortgage_amount)
	
	def getYearlyPayment(self):
		yearly_rate = self.yearly_interest_rate
		years = self.term_in_years
		mortgage_amount = self.mortgage_amount
		if yearly_rate == 0:
			return Decimal(-mortgage_amount / years)
		else:
			return numpy.pmt(yearly_rate, years, mortgage_amount)
	
	def getPrincipalPayment(self, years_since_investment):
		yearly_rate = self.yearly_interest_rate
		years = self.term_in_years
		year = years_since_investment
		mortgage_amount = self.mortgage_amount
		if yearly_rate == 0:
			return Decimal(-mortgage_amount / years)
		else:
			return numpy.ppmt(yearly_rate, year, years, mortgage_amount)
	
	def getInterestPayment(self, years_since_investment):
		yearly_rate = self.yearly_interest_rate
		if yearly_rate == 0:
			return 0
		else:
			years = self.term_in_years
			year = years_since_investment
			mortgage_amount = self.mortgage_amount
			ipmt = numpy.ipmt(yearly_rate, year, years, mortgage_amount)
			return numpy.asscalar(ipmt)
	
	def getPMIPayment(self, debt):
		PMI_INSURANCE = Decimal(.01)
		pmi = 0
		if debt / self.house.price < -.8:
			pmi = debt * PMI_INSURANCE
		
		return pmi