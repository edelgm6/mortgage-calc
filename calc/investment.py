import numpy
from decimal import Decimal
import math
	
class Investment:
	def __init__(self, house, mortgage, closing_cost_as_percent_of_value, alternative_rent, realtor_cost_as_percent_of_value, federal_tax_rate, state_tax_rate):
		self.house = house
		self.mortgage = mortgage
		self.closing_cost_as_percent_of_value = closing_cost_as_percent_of_value
		self.starting_equity = self.mortgage.down_payment_amount
		self.alternative_rent = alternative_rent
		self.realtor_cost = realtor_cost_as_percent_of_value
		self.federal_tax_rate = federal_tax_rate
		self.state_tax_rate = state_tax_rate
	
	# Gets value of home given current year
	def getValue(self, years_since_purchase):
		return self.house.price * (1+self.house.yearly_appreciation_rate)**years_since_purchase

	# Returns total cash costs for purchase	
	def getYearZeroCashFlow(self):
		equity_check = self.starting_equity * -1
		closing_cost = self.house.price * self.closing_cost_as_percent_of_value * -1
		return equity_check + closing_cost
	
	def getAverageValueInYear(self, current_value):
		beginning_of_year_value = current_value
		end_of_year_value = current_value * (1+self.house.yearly_appreciation_rate)
		average_value_in_year = (beginning_of_year_value + end_of_year_value) / 2
		return average_value_in_year
	
	def getSaleProceeds(self, current_debt, current_equity):
		current_value = current_equity - current_debt
		realtor_cost = current_value * self.realtor_cost
		net_sale_proceeds = current_equity - realtor_cost
		return net_sale_proceeds

	def getInterestTaxBenefit(self, debt_value, interest_payment):
		DEBT_LIMIT = 750000
		
		if debt_value * -1 > DEBT_LIMIT:
			interest_multiplier = (DEBT_LIMIT / debt_value) * -1
		else:
			interest_multiplier = 1
	
		total_tax_rate = self.federal_tax_rate + self.state_tax_rate
		
		interest_writeoff = total_tax_rate * interest_payment * interest_multiplier
		
		return interest_writeoff * -1

	def getPropertyTaxBenefit(self, property_tax):
		SALT_LIMIT = 10000
		
		if property_tax * -1 > SALT_LIMIT:
			property_tax_writeoff = SALT_LIMIT * self.federal_tax_rate
		else:
			property_tax_writeoff = property_tax * self.federal_tax_rate * -1
		
		return property_tax_writeoff

	
	def get_future_rent(self, year):
		growth_rate = self.house.yearly_appreciation_rate
			
		return Decimal(self.alternative_rent * ((1 + growth_rate) ** year))
	
	@staticmethod
	def _convert_to_round_integer(number):
		round_integer = int(round(number))
		return round_integer
	
	def getYearlyCashFlowsAndIRR(self):
		
		irr = ['NA']
		cash_flows = []
		
		# Calculate Year 0 conditions
		cash_flow_dict = {
			'year': 'Purchase',
			'equity': self._convert_to_round_integer(self.mortgage.down_payment_amount),
			'debt': self._convert_to_round_integer(self.mortgage.mortgage_amount * -1),
			'value': self._convert_to_round_integer(self.house.price),
			'principal_payment': 0,
			'total': self._convert_to_round_integer(self.getYearZeroCashFlow()),
			'other_costs': 0,
			'debt_payment': 0,
			'saved_rent': 0,
			'irr': irr[0]
		}
		
		cash_flows.append(cash_flow_dict)
		
		current_value = self.house.price
		debt = Decimal(self.mortgage.mortgage_amount * -1)
		alternative_rent = self.alternative_rent
		cash_stream = [self.getYearZeroCashFlow()]
		
		for year in range(1,31):
			# Balance sheet calculation
			principal_payment = self.mortgage.getPrincipalPayment(year)
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
			sell_in_this_year_irr = self.getIRR(cash_stream, equity, debt, year)
			cash_flow_dict['irr'] = sell_in_this_year_irr
			
			irr.append(sell_in_this_year_irr)
			cash_flows.append(cash_flow_dict)
		
		return irr, cash_flows

	def get_calculated_values(self, year, debt):

		# Calculates in-year costs based on average value throughout year
		average_value = (self.house.get_future_value(year) + self.house.get_future_value(year-1)) / 2
		maintenance = self.house.yearly_maintenance_as_percent_of_value * average_value * -1
		property_tax = Decimal(self.house.yearly_property_tax_rate * average_value * -1)
		insurance = self.house.yearly_insurance_as_percent_of_value * average_value * -1
		rent_avoided = (self.get_future_rent(year) + self.get_future_rent(year-1)) / 2

		# Calculates tax benefits
		interest_payment = self.mortgage.getInterestPayment(year)
		interest_writeoff = self.getInterestTaxBenefit(debt, interest_payment)
		property_tax_writeoff = self.getPropertyTaxBenefit(property_tax)
		tax_shield = interest_writeoff + property_tax_writeoff

		pmi = self.mortgage.getPMIPayment(debt)
		
		# Calculate cash stream
		cash_flow = self.mortgage.yearly_payment + maintenance + property_tax + rent_avoided + tax_shield + insurance + pmi

		other_costs = cash_flow - rent_avoided - self.mortgage.yearly_payment
		cash_flow_dict = {
			'total': self._convert_to_round_integer(cash_flow),
			'other_costs': self._convert_to_round_integer(other_costs),
			'debt_payment': self._convert_to_round_integer(interest_payment),
			'saved_rent': self._convert_to_round_integer(rent_avoided),
		}			
		
		return cash_flow_dict
	
	def getIRR(self, cash_stream, equity, debt, year):

		# Calculates IRR with separate cash flow array
		cash_stream_with_sale = cash_stream[:]
		net_sale_proceeds = self.getSaleProceeds(debt, equity)
		cash_stream_with_sale[year] = cash_stream[year] + net_sale_proceeds
		irr = numpy.irr(cash_stream_with_sale)
		
		# Sets cumulative to None for when cash flows are always negative
		if math.isnan(irr):
			irr = None
		else:
			irr = round(irr * 100,2)
		
		return irr