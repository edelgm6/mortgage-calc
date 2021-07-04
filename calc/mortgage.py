import numpy_financial as npf
import numpy
from decimal import Decimal
import math

class Mortgage:
	"""Respresentation of the investment's mortgage.

	Attributes:
		house (House): House object for the mortgage.
		yearly_interest_rate (Decimal): Yearly mortgage interest rate.
		term_in_years (int): Years for mortgage amortization.
		down_payment_percent (Decimal): Down payment as a % of the house price.

	"""

	def __init__(self, house, yearly_interest_rate, term_in_years, down_payment_percent):
		self.house = house
		self.yearly_interest_rate = yearly_interest_rate
		self.term_in_years = term_in_years
		self.down_payment_amount = self.house.price * down_payment_percent
		self.mortgage_amount = self.house.price - self.down_payment_amount
		self.monthly_payment = self._get_monthly_payment()
		self.yearly_payment = self._get_yearly_payment()

	def _get_monthly_payment(self):
		monthly_rate = self.yearly_interest_rate / 12
		months = self.term_in_years * 12
		mortgage_amount = self.mortgage_amount
		return npf.pmt(monthly_rate, months, mortgage_amount)

	def _get_yearly_payment(self):
		yearly_rate = self.yearly_interest_rate
		years = self.term_in_years
		mortgage_amount = self.mortgage_amount
		return Decimal(npf.pmt(yearly_rate, years, mortgage_amount))

	def get_principal_payment(self, year):
		"""Return principal payment for a given year post-investment.

		Args:
			year (int): Number of years after the purchase of the asset.

		Returns:
			Decimal: Principal payment in given year.

		"""

		yearly_rate = self.yearly_interest_rate
		years = self.term_in_years
		mortgage_amount = self.mortgage_amount
		return Decimal(npf.ppmt(yearly_rate, year, years, mortgage_amount))

	def get_interest_payment(self, year):
		"""Return principal payment for a given year post-investment.

		Args:
			year (int): Number of years after the purchase of the asset.

		Returns:
			Decimal: Interest payment in given year.

		"""
		yearly_rate = self.yearly_interest_rate
		years = self.term_in_years
		mortgage_amount = self.mortgage_amount
		ipmt = npf.ipmt(yearly_rate, year, years, mortgage_amount)

		# asscalar needed to enable conversion of the ndarray to Decimal values
		return Decimal(numpy.asscalar(ipmt))

	def get_pmi_payment(self, debt):
		"""Return pmi payment for a given year post-investment.

		Args:
			debt (Decimal): Mortgage debt balance

		Returns:
			Decimal: Cost of PMI insurance.

		"""

		PMI_INSURANCE = Decimal(.01)
		pmi = 0

		# Debt is a negative value, hence the < -.8
		if debt / self.house.price < -.8:
			pmi = debt * PMI_INSURANCE

		return pmi
