import numpy

class House:
	def __init__(self, price, yearly_appreciation_rate, yearly_property_tax_rate, yearly_maintenance_as_percent_of_value):
		self.price = price
		self.yearly_appreciation_rate = yearly_appreciation_rate
		self.yearly_property_tax_rate = yearly_property_tax_rate
		self.yearly_maintenance_as_percent_of_value = yearly_maintenance_as_percent_of_value
	
	
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
	
class Investment:
	def __init__(self, house, mortgage, closing_cost_as_percent_of_value, alternative_rent):
		self.house = house
		self.mortgage = mortgage
		self.closing_cost_as_percent_of_value = closing_cost_as_percent_of_value
		self.starting_equity = self.mortgage.down_payment_amount
		self.alternative_rent = alternative_rent
		
	def getValue(self, years_since_purchase):
		return self.house.price * (1+self.house.yearly_appreciation_rate)**years_since_purchase
	
	def __convertToReadableString(self, number):
		string = int(round(number))
		return '{:0,.0f}'.format(number)
	
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
		
		yearly_payment = self.mortgage.getYearlyPayment()
		value = self.house.price
		debt = self.mortgage.mortgage_amount * -1
		cash_flow_stream = []
		cash_flow_stream.append(self.getYearZeroCashFlow())
		alternative_rent = self.alternative_rent
		for i in range(1,31):
			
			###Clean this shit up, especially this issue with averaging some things 
			##May need to average in the alternate rent.  Should be clustered to be cleaner
			
			mortgage_payment = yearly_payment
			debt = debt - self.mortgage.getPrincipalPayment(i)
			average_value = (value + value * (1+self.house.yearly_appreciation_rate)) / 2
			maintenance = self.house.yearly_maintenance_as_percent_of_value * average_value * -1
			property_tax = self.house.yearly_property_tax_rate * average_value * -1
			alternative_rent = alternative_rent * (1+self.house.yearly_appreciation_rate)
			
			cash_flow = mortgage_payment + maintenance + property_tax + alternative_rent
			cash_flow_stream.append(cash_flow)
	
			value = value * (1+self.house.yearly_appreciation_rate)
	
			equity = value + debt
			closing_cost = value * self.closing_cost_as_percent_of_value
			net_sale_proceeds = equity - closing_cost
			cash_flows_with_sale = cash_flow_stream[:]
			cash_flows_with_sale[i] = cash_flow_stream[i] + net_sale_proceeds
			irr = numpy.irr(cash_flows_with_sale)
			

			
			cash_flow_dict = {
				'total': self.__convertToReadableString(cash_flow),
				'mortgage': self.__convertToReadableString(mortgage_payment),
				'other_costs': self.__convertToReadableString(maintenance + property_tax),
				'value': self.__convertToReadableString(value),
				'equity': self.__convertToReadableString(equity),
				'debt': self.__convertToReadableString(debt),
				'closing_costs': self.__convertToReadableString(closing_cost),
				'net_proceeds': self.__convertToReadableString(net_sale_proceeds),
				'irr': str(round(irr * 100,2)) + '%',
				'year': i,
				'principal_payment': self.__convertToReadableString(self.mortgage.getPrincipalPayment(i)),
				'debt_payment': self.__convertToReadableString(mortgage_payment - self.mortgage.getPrincipalPayment(i)),
				'saved_rent': self.__convertToReadableString(alternative_rent)
			}
			
			cash_flows.append(cash_flow_dict)
			
		return cash_flows
			
		
	def getYearZeroCashFlow(self):
		equity_check = self.starting_equity * -1
		closing_costs = self.house.price * self.closing_cost_as_percent_of_value * -1
		return equity_check + closing_costs
		
