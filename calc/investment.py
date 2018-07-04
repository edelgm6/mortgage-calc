import numpy
from decimal import Decimal
import math
from calc.utils import convert_number_to_readable_string
	
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
		
		#interest_writeoff = total_tax_rate * Decimal(interest_payment) * interest_multiplier
		interest_writeoff = total_tax_rate * interest_payment * interest_multiplier
		
		return interest_writeoff * -1

	def getPropertyTaxBenefit(self, property_tax):
		SALT_LIMIT = 10000
		
		if property_tax * -1 > SALT_LIMIT:
			property_tax_writeoff = SALT_LIMIT * self.federal_tax_rate
		else:
			property_tax_writeoff = property_tax * self.federal_tax_rate * -1
		
		return property_tax_writeoff

	
	def getAlternativeRentStreams(self):
		alternative_rent_stream = [self.alternative_rent]
		growth_rate = self.house.yearly_appreciation_rate
		
		for year in range(1,31):
			alternative_rent_stream.append(alternative_rent_stream[year-1] * Decimal((1 + growth_rate)))
			
		return alternative_rent_stream
	
	
	def getYearlyCashFlowsAndIRR(self):
		
		# Calculate Year 0 conditions
		irr = ['NA']
		cash_flow_dict = {
			'total': convert_number_to_readable_string(self.getYearZeroCashFlow()),
			'mortgage': 0,
			'taxes': 0,
			'maintenance': 0,
			'value': convert_number_to_readable_string(self.house.price),
			'equity': convert_number_to_readable_string(self.mortgage.down_payment_amount),
			'debt': convert_number_to_readable_string(self.mortgage.mortgage_amount * -1),
			'closing_costs': 0,
			'net_proceeds': 0,
			'year': 'Purchase',
			'irr': 'N/A'
		}
		cash_flows = [cash_flow_dict]
		
		current_value = self.house.price
		debt = Decimal(self.mortgage.mortgage_amount * -1)
		mortgage_payment = self.mortgage.getYearlyPayment()
		alternative_rent = self.alternative_rent
		cash_stream = [self.getYearZeroCashFlow()]
		
		# Calculate Years 0-30 rent and home values
		rent_stream = self.getAlternativeRentStreams()
		value_stream = self.house.getHomeValueStreams()
		
		
		for year in range(1,31):
			principal_payment = self.mortgage.getPrincipalPayment(year)
			debt = debt - principal_payment
			current_value = value_stream[year]
			equity = current_value + debt
		
			pmi = self.mortgage.getPMIPayment(debt)

			# Calculates in-year costs based on average value throughout year
			average_value = (value_stream[year] + value_stream[year-1]) / 2
			maintenance = self.house.yearly_maintenance_as_percent_of_value * average_value * -1
			property_tax = Decimal(self.house.yearly_property_tax_rate * average_value * -1)
			insurance = self.house.yearly_insurance_as_percent_of_value * average_value * -1
			rent_avoided = (rent_stream[year] + rent_stream[year-1]) / 2
			
			# Calculates tax benefits
			interest_payment = self.mortgage.getInterestPayment(year)
			interest_writeoff = self.getInterestTaxBenefit(debt, interest_payment)
			property_tax_writeoff = self.getPropertyTaxBenefit(property_tax)
			tax_shield = interest_writeoff + property_tax_writeoff
			
			# Calculate cash stream
			cash_flow = mortgage_payment + maintenance + property_tax + rent_avoided + tax_shield + insurance + pmi
			cash_stream.append(cash_flow)	
			
			sell_in_this_year_irr = self.getIRR(cash_stream, equity, debt, year)
			irr.append(sell_in_this_year_irr)
			
			other_costs = cash_flow - rent_avoided - mortgage_payment
			cash_flow_dict = {
				'total': convert_number_to_readable_string(cash_stream[year]),
				'other_costs': convert_number_to_readable_string(other_costs),
				'value': convert_number_to_readable_string(current_value),
				'equity': convert_number_to_readable_string(equity),
				'debt': convert_number_to_readable_string(debt),
				'year': year,
				'principal_payment': convert_number_to_readable_string(principal_payment),
				'debt_payment': convert_number_to_readable_string(interest_payment),
				'saved_rent': convert_number_to_readable_string(rent_avoided),
				'irr': sell_in_this_year_irr
			}			
			cash_flows.append(cash_flow_dict)
		
		return irr, cash_flows

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