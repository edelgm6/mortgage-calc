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
	
	def getSaleProceeds(self, current_value, current_equity):
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

	def getPropertyTaxBenefit(self, federal_tax_rate, property_tax):
		SALT_LIMIT = 10000
		
		if property_tax * -1 > SALT_LIMIT:
			property_tax_writeoff = SALT_LIMIT * federal_tax_rate
		else:
			property_tax_writeoff = property_tax * federal_tax_rate * -1
		
		return property_tax_writeoff
	
	def getYearlyCashFlowsAndIRR(self, irr_only=False, tax_shield_included=True):
		irr = []
		irr.append('NA')
		
		if not irr_only:
			cash_flows = []
			cash_flow_dict = {
				'total': self.__convertToReadableString(self.getYearZeroCashFlow()),
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
			cash_flows.append(cash_flow_dict)
		
		mortgage_payment = self.mortgage.getYearlyPayment()
		current_value = self.house.price
		debt = self.mortgage.mortgage_amount * -1
		alternative_rent = self.alternative_rent
		
		base_rent = self.getAlternativeRentStreams()
		base_value = self.house.getHomeValueStreams()
		base_cash_stream = [self.getYearZeroCashFlow()]
		
		for year in range(1,31):

			interest_payment = self.mortgage.getInterestPayment(year)
			principal_payment = self.mortgage.getPrincipalPayment(year)
			debt = debt - principal_payment
			interest_writeoff = self.getInterestTaxBenefit(self.federal_tax_rate, self.state_tax_rate, debt, interest_payment)
			pmi = self.mortgage.getPMIPayment(debt)
			
			other_costs, rent_avoided = self.updateCashStream(base_cash_stream, base_value, base_rent, interest_writeoff, year, mortgage_payment, pmi, True, tax_shield_included)
			
			base_irr, equity = self.getIRR(base_cash_stream, base_value, debt, year, True)
			
			# Sets cumulative to None for when cash flows are always negative
			if math.isnan(base_irr):
				cumulative_irr = None
			else:
				cumulative_irr = round(base_irr * 100,2)

			irr.append(cumulative_irr)
			if not irr_only:
				cash_flow_dict = {
					'total': convert_number_to_readable_string(base_cash_stream[year]),
					'other_costs': convert_number_to_readable_string(other_costs),
					'value': convert_number_to_readable_string(base_value[year]),
					'equity': convert_number_to_readable_string(equity),
					'debt': convert_number_to_readable_string(debt),
					'year': year,
					'principal_payment': convert_number_to_readable_string(principal_payment),
					'debt_payment': convert_number_to_readable_string(interest_payment),
					'saved_rent': convert_number_to_readable_string(rent_avoided),
					'irr': cumulative_irr
				}			
				cash_flows.append(cash_flow_dict)
		
		if irr_only:
			return irr
		else:
			return irr, cash_flows

	def updateCashStream(self, cash_stream, value_stream, rent_stream, interest_writeoff, year, mortgage_payment, pmi, is_base=False, tax_shield_included=True):
		# Calculates in-year costs based on average value throughout year
		average_value = (value_stream[year] + value_stream[year-1]) / 2
		rent_avoided = (rent_stream[year] + rent_stream[year-1]) / 2
		maintenance = self.house.yearly_maintenance_as_percent_of_value * average_value * -1
		property_tax = self.house.yearly_property_tax_rate * average_value * -1
		insurance = self.house.yearly_insurance_as_percent_of_value * average_value * -1

		# Calculates tax benefits
		property_tax_writeoff = self.getPropertyTaxBenefit(self.federal_tax_rate, property_tax)
		if tax_shield_included:
			tax_shield = interest_writeoff + property_tax_writeoff
		else:
			tax_shield = 0
		cash_flow = mortgage_payment + maintenance + property_tax + rent_avoided + tax_shield + insurance + pmi
		cash_stream.append(cash_flow)	
		
		if is_base:
			"""
			print(year)
			print('property_tax')
			print(property_tax)
			print('insurance')
			print(insurance)
			print('maintenance')
			print(maintenance)
			print('pmi')
			print(pmi)
			print('interest_writeoff')
			print(interest_writeoff)
			print('property_tax_writeoff')
			print(property_tax_writeoff)
			"""
			other_costs = cash_flow - rent_avoided - mortgage_payment
			return other_costs, rent_avoided
		
	def getIRR(self, cash_stream, value_stream, debt, year, is_base=False):
			
		# Calculates balance sheet
		current_value = value_stream[year]
		equity = current_value + debt

		# Calculates IRR with separate cash flow array
		cash_stream_with_sale = cash_stream[:]
		net_sale_proceeds = self.getSaleProceeds(current_value, equity)
		cash_stream_with_sale[year] = cash_stream[year] + net_sale_proceeds
		irr = numpy.irr(cash_stream_with_sale)
		
		if is_base:
			return irr, equity
		else:
			return irr
	
	def getAlternativeRentStreams(self):
		base_case = [self.alternative_rent]
		BASE_GROWTH_RATE = self.house.yearly_appreciation_rate
		
		for year in range(1,31):
			base_case.append(base_case[year-1] * (1+BASE_GROWTH_RATE))
			
		return base_case#, high_case, low_case
		
