from pyknow import *

class Person(Fact):
	annual_income = Field(int)
	age = Field(int)
	citizenship = Field(str)
	total_spending_amount = Field(str)
	pass

class Eligibility(KnowledgeEngine):

	@Rule(
		Person(
		data__age=MATCH.age,
		data__annual_income=MATCH.annual_income,
		data__citizenship=MATCH.citizenship,
		data__total_spending_amount=MATCH.total_spending_amount
		),
		Person(data__age=MATCH.data__age),		 
		TEST(lambda data__age: data__age <21))

	def age_eligibility(self,age,annual_income,citizenship,total_spending_amount):
		
		p1 = Person()
		p1.age = age
		p1.annual_income = annual_income
		p1.citizenship = citizenship
		p1.total_spending_amount = total_spending_amount

		f = open("available.csv","a")
		f.write(str(p1.age)+","+"Not Available" + "\n")		
		f.close()



