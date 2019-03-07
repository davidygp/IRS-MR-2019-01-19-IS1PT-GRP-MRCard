from pyknow import *
from Person_Eligibility import Eligibility
from Person_Eligibility import Person



test_data = {
	"annual_income": "29000",
	"age": 20,
	"citizenship": 'Singaporean',
	"total_spending_amount": 1000}

engine = Eligibility()
engine.reset()
engine.declare(Person(data=test_data))
engine.run()
engine.facts


