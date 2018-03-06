import numpy
from decimal import Decimal

class House:
	def __init__(self, price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value, yearly_insurance_as_percent_of_value):
		self.price = price
		self.yearly_appreciation_rate = yearly_appreciation_rate
		self.yearly_property_tax_rate = yearly_property_tax_rate
		self.yearly_maintenance_as_percent_of_value = yearly_maintenance_as_percent_of_value
		self.yearly_insurance_as_percent_of_value = yearly_insurance_as_percent_of_value
		
	def getHomeValueStreams(self):
		base_case = [self.price]
		high_case = [self.price]
		low_case = [self.price]
		
		BASE_GROWTH_RATE = self.yearly_appreciation_rate
		HIGH_GROWTH_RATE = BASE_GROWTH_RATE + Decimal(.01)
		LOW_GROWTH_RATE = BASE_GROWTH_RATE - Decimal(.01)
		
		for year in range(1,31):
			base_case.append(base_case[year-1] * (1+BASE_GROWTH_RATE))
			high_case.append(high_case[year-1] * (1+HIGH_GROWTH_RATE))
			low_case.append(low_case[year-1] * (1+LOW_GROWTH_RATE))
			
		return base_case, high_case, low_case
	
	
class Mortgage:
	def __init__(self, house, yearly_interest_rate, term_in_years, down_payment_percent):
		self.house = house
		self.yearly_interest_rate = yearly_interest_rate
		self.term_in_years = term_in_years
		self.down_payment_percent = down_payment_percent
		self.down_payment_amount = self.house.price * self.down_payment_percent
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
		return numpy.pmt(yearly_rate, years, mortgage_amount)
	
	def getPrincipalPayment(self, years_since_investment):
		yearly_rate = self.yearly_interest_rate
		years = self.term_in_years
		year = years_since_investment
		mortgage_amount = self.mortgage_amount
		return numpy.ppmt(yearly_rate, year, years, mortgage_amount)
	
	def getInterestPayment(self, years_since_investment):
		yearly_rate = self.yearly_interest_rate
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
	
	def __convertToReadableString(self, number):
		string = int(round(number))
		return string
	
	def getYearlyCashFlowsAndIRR(self):
		cash_flows = []
		
		cash_flow_dict = {
			'total': self.__convertToReadableString(self.getYearZeroCashFlow()),
			'mortgage': 0,
			'taxes': 0,
			'maintenance': 0,
			'value': self.__convertToReadableString(self.house.price),
			'equity': self.__convertToReadableString(self.mortgage.down_payment_amount),
			'debt': self.__convertToReadableString(self.mortgage.mortgage_amount * -1),
			'closing_costs': 0,
			'net_proceeds': 0,
			'irr': 'NA',
			'year': 'Purchase'
		}
		cash_flows.append(cash_flow_dict)
		
		mortgage_payment = self.mortgage.getYearlyPayment()
		current_value = self.house.price
		debt = self.mortgage.mortgage_amount * -1
		alternative_rent = self.alternative_rent
		
		base_rent, high_rent, low_rent = self.getAlternativeRentStreams()
		base_value, high_value, low_value = self.house.getHomeValueStreams()
		base_cash_stream = [self.getYearZeroCashFlow()]
		high_cash_stream = [self.getYearZeroCashFlow()]
		low_cash_stream = [self.getYearZeroCashFlow()]
		
		for year in range(1,31):

			
			interest_payment = self.mortgage.getInterestPayment(year)
			principal_payment = self.mortgage.getPrincipalPayment(year)
			debt = debt - principal_payment
			interest_writeoff = self.getInterestTaxBenefit(self.federal_tax_rate, self.state_tax_rate, debt, interest_payment)
			pmi = self.mortgage.getPMIPayment(debt)
			
			other_costs, rent_avoided = self.updateCashStream(base_cash_stream, base_value, base_rent, interest_writeoff, year, mortgage_payment, pmi, True)
			self.updateCashStream(low_cash_stream, low_value, low_rent, interest_writeoff, year, mortgage_payment, pmi)
			self.updateCashStream(high_cash_stream, high_value, high_rent, interest_writeoff, year, mortgage_payment, pmi)
			
			base_irr, equity = self.getIRR(base_cash_stream, base_value, debt, year, True)
			low_irr = self.getIRR(low_cash_stream, low_value, debt, year)
			high_irr = self.getIRR(high_cash_stream, high_value, debt, year)
			
			# Calculates for base stream only
			cash_flow_dict = {
				'total': self.__convertToReadableString(base_cash_stream[year]),
				'other_costs': self.__convertToReadableString(other_costs),
				'value': self.__convertToReadableString(base_value[year]),
				'equity': self.__convertToReadableString(equity),
				'debt': self.__convertToReadableString(debt),
				'irr': round(base_irr * 100,2),
				'high_irr': round(high_irr * 100,2),
				'low_irr': round(low_irr * 100,2),
				'year': year,
				'principal_payment': self.__convertToReadableString(principal_payment),
				'debt_payment': self.__convertToReadableString(interest_payment),
				'saved_rent': self.__convertToReadableString(rent_avoided)
			}
			
			cash_flows.append(cash_flow_dict)
			
		return cash_flows

	def updateCashStream(self, cash_stream, value_stream, rent_stream, interest_writeoff, year, mortgage_payment, pmi, is_base=False):
		# Calculates in-year costs based on average value throughout year
		average_value = (value_stream[year] + value_stream[year-1]) / 2
		rent_avoided = (rent_stream[year] + rent_stream[year-1]) / 2
		maintenance = self.house.yearly_maintenance_as_percent_of_value * average_value * -1
		property_tax = self.house.yearly_property_tax_rate * average_value * -1
		insurance = self.house.yearly_insurance_as_percent_of_value * average_value * -1

		# Calculates tax benefits
		property_tax_writeoff = self.getPropertyTaxBenefit(self.federal_tax_rate, property_tax)
		tax_shield = interest_writeoff + property_tax_writeoff

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
		high_case = [self.alternative_rent]
		low_case = [self.alternative_rent]
		
		BASE_GROWTH_RATE = self.house.yearly_appreciation_rate
		HIGH_GROWTH_RATE = BASE_GROWTH_RATE + Decimal(.01)
		LOW_GROWTH_RATE = BASE_GROWTH_RATE - Decimal(.01)
		
		for year in range(1,31):
			base_case.append(base_case[year-1] * (1+BASE_GROWTH_RATE))
			high_case.append(high_case[year-1] * (1+HIGH_GROWTH_RATE))
			low_case.append(low_case[year-1] * (1+LOW_GROWTH_RATE))
			
		return base_case, high_case, low_case
	
	def getInterestTaxBenefit(self, federal_tax_rate, state_tax_rate, debt_value, interest_payment):
		DEBT_LIMIT = 750000
		
		if debt_value * -1 > DEBT_LIMIT:
			interest_multiplier = (DEBT_LIMIT / debt_value) * -1
		else:
			interest_multiplier = 1
		
		total_tax_rate = federal_tax_rate + state_tax_rate
		interest_writeoff = total_tax_rate * interest_payment * interest_multiplier
		
		return interest_writeoff * -1

	def getPropertyTaxBenefit(self, federal_tax_rate, property_tax):
		SALT_LIMIT = 10000
		
		if property_tax * -1 > SALT_LIMIT:
			property_tax_writeoff = SALT_LIMIT * federal_tax_rate
		else:
			property_tax_writeoff = property_tax * federal_tax_rate * -1
		
		return property_tax_writeoff
		
	
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
		
