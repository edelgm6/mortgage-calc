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
	
	def getYearlyCashFlowsAndIRR(self):
		cash_flows = []
		IRRs = []
		
		cash_flows.append(self.getYearZeroCashFlow())
		
		yearly_payment = self.mortgage.getYearlyPayment()
		
		value = self.house.price
		debt = self.mortgage.mortgage_amount
		for i in range(1,31):
			mortgage_payment = yearly_payment
			debt = debt + self.mortgage.getPrincipalPayment(i)
			average_value = (value + value * (1+self.house.yearly_appreciation_rate)) / 2
			maintenance = self.house.yearly_maintenance_as_percent_of_value * average_value * -1
			property_tax = self.house.yearly_property_tax_rate * average_value * -1
			cash_flows.append(mortgage_payment + maintenance + property_tax)
			value = value * (1+self.house.yearly_appreciation_rate)
			
			equity = value - debt
			net_sale_proceeds = equity - value * self.closing_cost_as_percent_of_value
			cash_flows_with_sale = cash_flows[:]
			cash_flows_with_sale[i] = cash_flows[i] + net_sale_proceeds
			IRRs.append(numpy.irr(cash_flows_with_sale))
			
		return cash_flows, IRRs
			
		
	def getYearZeroCashFlow(self):
		equity_check = self.starting_equity * -1
		closing_costs = self.house.price * self.closing_cost_as_percent_of_value * -1
		return equity_check + closing_costs
		
