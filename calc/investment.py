import numpy
import math
from decimal import Decimal
from django.conf import settings
	
class Investment:
	"""Respresentation of the Investment.
	
	Attributes:
		house (House): House object for the investment.
		mortgage (Mortgage): Mortgage object for the investment.
		closing_cost_rate (Decimal): Buyer's closing costs as a % of the house price.
		alternative_rent (int): Alternative rent buyer would be paying if they did 
			not buy the house.
		realtor_cost_rate (Decimal): Seller's costs of paying the buyer and seller 
			agents as a % of the house price.
		federal_tax_rate (Decimal): Top marginal federal tax rate paid by the buyer.
		state_tax_rate (Decimal): Top marginal state tax rate paid by the buyer.
	
	"""
	
	def __init__(self, house, mortgage, closing_cost_rate, alternative_rent, realtor_cost_rate, federal_tax_rate, state_tax_rate):
		self.house = house
		self.mortgage = mortgage
		self.closing_cost_rate = closing_cost_rate
		self.starting_equity = self.mortgage.down_payment_amount
		self.alternative_rent = alternative_rent
		self.realtor_cost_rate = realtor_cost_rate
		self.federal_tax_rate = federal_tax_rate
		self.state_tax_rate = state_tax_rate

	# Returns total cash costs for purchase	
	def _get_year_zero_cash_flow(self):
		equity_check = self.starting_equity * -1
		closing_cost = self.house.price * self.closing_cost_rate * -1
		return equity_check + closing_cost
	
	def _get_sale_proceeds(self, current_debt, current_equity):
		current_value = current_equity - current_debt
		realtor_cost = current_value * self.realtor_cost_rate
		net_sale_proceeds = current_equity - realtor_cost
		return net_sale_proceeds

	def _get_interest_tax_benefit(self, debt_value, interest_payment):
		debt_limit = settings.MORTGAGE_INTEREST_DEDUCTION_DEBT_LIMIT
		
		if debt_value * -1 > debt_limit:
			interest_multiplier = (debt_limit / debt_value) * -1
		else:
			interest_multiplier = 1
	
		total_tax_rate = self.federal_tax_rate + self.state_tax_rate
		
		interest_writeoff = total_tax_rate * interest_payment * interest_multiplier
		
		return interest_writeoff * -1

	def _get_property_tax_benefit(self, property_tax):
		salt_limit = settings.SALT_LIMIT
		
		if property_tax * -1 > salt_limit:
			property_tax_writeoff = salt_limit * self.federal_tax_rate
		else:
			property_tax_writeoff = property_tax * self.federal_tax_rate * -1
		
		return property_tax_writeoff

	
	def _get_future_rent(self, year):
		growth_rate = self.house.yearly_appreciation_rate
			
		return Decimal(self.alternative_rent * ((1 + growth_rate) ** year))
	
	@staticmethod
	def _convert_to_round_integer(number):
		round_integer = int(round(number))
		return round_integer
	
	def get_yearly_cash_flows_and_irr(self):
		"""Return array of cash flow dicts and IRRs.
			
		Returns:
			dict (string:any): Dictionary representing each year of the investment 
				year (string/int): 'Purchase' for year 0 and 
					int of years since investment for each of years 1-30.
				equity (int): Equity value of investment.
				debt (int): Mortgage debt balance.
				value (int): Value of the asset.
				principal_payment (int): Principal payment.
				interest_payment (int): Interest payment.
				total (int): Net cash flow.
				other_costs (int): Cost of maintenance, insurance, and pmi, 
					net of the tax shield
				saved_rent (int): Rent not paid in year.
				irr (string/Decimal): 'NA' for year 0- and IRR as Decimal 
					for each of years 1-30
			array (string/Decimal): 'NA' for year 0 and IRR as Decimal for each of 
				years 1-30
					
		
		"""
		
		irr = ['NA']
		cash_flows = []
		cash_stream = [self._get_year_zero_cash_flow()]
		
		# Calculate Year 0 conditions
		cash_flow_dict = {
			'year': 'Purchase',
			'equity': self._convert_to_round_integer(self.mortgage.down_payment_amount),
			'debt': self._convert_to_round_integer(self.mortgage.mortgage_amount * -1),
			'value': self._convert_to_round_integer(self.house.price),
			'principal_payment': 0,
			'interest_payment': 0,
			'total': self._convert_to_round_integer(cash_stream[0]),
			'other_costs': 0,
			'saved_rent': 0,
			'irr': irr[0]
		}
		
		cash_flows.append(cash_flow_dict)
		
		current_value = self.house.price
		debt = Decimal(self.mortgage.mortgage_amount * -1)
		alternative_rent = self.alternative_rent
		
		
		for year in range(1,31):
			# Balance sheet calculation
			principal_payment = self.mortgage.get_principal_payment(year)
			debt = debt - principal_payment
			current_value = self.house.get_future_value(year)
			equity = current_value + debt
			
			# Start cash flow dict with known balance sheet data
			cash_flow_dict = {
				'year': year,
				'equity': self._convert_to_round_integer(equity),
				'debt': self._convert_to_round_integer(debt),
				'value': self._convert_to_round_integer(current_value),
				'principal_payment': self._convert_to_round_integer(principal_payment)
			}
			
			# Update cash_flow_dict with calculated values 
			cash_flow_dict.update(self.get_calculated_values(year, debt))
			
			cash_stream.append(cash_flow_dict['total'])	
			sell_in_this_year_irr = self._get_irr(cash_stream, equity, debt, year)
			cash_flow_dict['irr'] = sell_in_this_year_irr
			
			irr.append(sell_in_this_year_irr)
			cash_flows.append(cash_flow_dict)
		
		return irr, cash_flows

	def get_calculated_values(self, year, debt):
		"""Return single year dict of additional calculated values.
			
		Returns:
			dict (string:int): Dictionary representing a given year of the investment 
				total (int): Net cash flow.
				other_costs (int): Cost of maintenance, insurance, and pmi, 
					net of the tax shield
				interest_payment (int): Interest payment.
				saved_rent (int): Rent not paid in year.			
		
		"""
		
		# Calculates in-year costs based on average value throughout year
		average_value = (self.house.get_future_value(year) + self.house.get_future_value(year-1)) / 2
		maintenance = self.house.yearly_maintenance_rate * average_value * -1
		property_tax = Decimal(self.house.yearly_property_tax_rate * average_value * -1)
		insurance = self.house.yearly_insurance_rate * average_value * -1
		rent_avoided = (self._get_future_rent(year) + self._get_future_rent(year-1)) / 2

		# Calculates tax benefits
		interest_payment = self.mortgage.get_interest_payment(year)
		interest_writeoff = self._get_interest_tax_benefit(debt, interest_payment)
		property_tax_writeoff = self._get_property_tax_benefit(property_tax)
		tax_shield = interest_writeoff + property_tax_writeoff

		pmi = self.mortgage.get_pmi_payment(debt)
		
		# Calculate cash stream
		cash_flow = self.mortgage.yearly_payment + maintenance + property_tax + rent_avoided + tax_shield + insurance + pmi

		other_costs = cash_flow - rent_avoided - self.mortgage.yearly_payment
		other_values_dict = {
			'total': self._convert_to_round_integer(cash_flow),
			'other_costs': self._convert_to_round_integer(other_costs),
			'interest_payment': self._convert_to_round_integer(interest_payment),
			'saved_rent': self._convert_to_round_integer(rent_avoided),
		}			
		
		return other_values_dict
	
	def _get_irr(self, cash_stream, equity, debt, year):

		# Calculates IRR with separate cash flow array
		cash_stream_with_sale = cash_stream[:]
		net_sale_proceeds = self._get_sale_proceeds(debt, equity)
		cash_stream_with_sale[year] = cash_stream[year] + net_sale_proceeds
		irr = numpy.irr(cash_stream_with_sale)
		
		# Sets cumulative to None for when cash flows are always negative
		if math.isnan(irr):
			irr = None
		else:
			irr = round(irr * 100,2)
		
		return irr