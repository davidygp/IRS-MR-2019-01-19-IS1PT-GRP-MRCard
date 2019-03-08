from random import choice
from pyknow import *

def return_cash_back_value(dict_of_personal_info, list_of_dict_of_credit_card_eligibility_info, debug=False):

	available_cards = {'available_cards':[],'cashback':[]}
				
	cashback = 0
	for row in list_of_dict_of_credit_card_eligibility_info:
	    cardid = str(row['credit_card_id'][0])
		contactless_cashback_rate = row['contactless_cashback_rate'][0]
		contactless_cashback_cap = row['contactless_cashback_cap'][0]
		contactless_cashback_min = row['contactless_cashback_min'][0]
		bill_cashback_rate = row['bill_cashback_rate'][0]
		bill_cashback_cap = row['bill_cashback_cap'][0]
		bill_cashback_min_spend = row['bill_cashback_min_spend'][0]
		dining_cashback_rate = row['dining_cashback_rate'][0]
		dining_cashback_cap = row['dining_cashback_cap'][0]
		dining_cashback_min_spend = row['dining_cashback_min_spend'][0]
		foreign_cashback_rate = row['foreign_cashback_rate'][0]
		foreign_cashback_cap = row['foreign_cashback_cap'][0]
		foreign_cashback_min_spend = row['foreign_cashback_min_spend'][0]
		retail_shopping_cashback_rate = row['retail_shopping_cashback_rate'][0]
		retail_shopping_cashback_cap = row['retail_shopping_cashback_cap'][0]
		retail_shopping_cashback_min_spend = row['retail_shopping_cashback_min_spend'][0]
		transport_cashback_rate = row['transport_cashback_rate'][0]
		transport_cashback_cap = row['transport_cashback_cap'][0]
		transport_cashback_min_spend = row['transport_cashback_min_spend'][0]
		groceries_overall_cashback_cap = row['groceries_overall_cashback_cap'][0]
		groceries_others_cashback_rate = row['groceries_others_cashback_rate'][0]
		groceries_others_cashback_cap = row['groceries_others_cashback_cap'][0]
		groceries_others_cashback_min_spend = row['groceries_others_cashback_min_spend'][0]
		groceries_ntuc_cashback_rate = row['groceries_ntuc_cashback_rate'][0]
		groceries_ntuc_cashback_cap = row['groceries_ntuc_cashback_cap'][0]
		groceries_ntuc_cashback_min_spend = row['groceries_ntuc_cashback_min_spend'][0]
		groceries_sheng_siong_cashback_rate = row['groceries_sheng_siong_cashback_rate'][0]
		groceries_sheng_siong_cashback_cap = row['groceries_sheng_siong_cashback_cap'][0]
		groceries_sheng_siong_cashback_min_spend = row['groceries_sheng_siong_cashback_min_spend'][0]
		groceries_cold_storage_cashback_rate = row['groceries_cold_storage_cashback_rate'][0]
		groceries_cold_storage_cashback_cap = row['groceries_cold_storage_cashback_cap'][0]
		groceries_cold_storage_cashback_min_spend = row['groceries_cold_storage_cashback_min_spend'][0]
		groceries_giant_cashback_rate = row['groceries_giant_cashback_rate'][0]
		groceries_giant_cashback_cap = row['groceries_giant_cashback_cap'][0]
		groceries_giant_cashback_min_spend = row['groceries_giant_cashback_min_spend'][0]
		online_shopping_overall_cashback_cap = row['online_shopping_overall_cashback_cap'][0]
		online_shopping_others_cashback_rate = row['online_shopping_others_cashback_rate'][0]
		online_shopping_others_cashback_cap = row['online_shopping_others_cashback_cap'][0]
		online_shopping_others_cashback_min_spend = row['online_shopping_others_cashback_min_spend'][0]
		online_shopping_hotels_and_flights_cashback_rate = row['online_shopping_hotels_and_flights_cashback_rate'][0]
		online_shopping_hotels_and_flights_cashback_cap = row['online_shopping_hotels_and_flights_cashback_cap'][0]
		online_shopping_hotels_and_flights_cashback_min_spend = row['online_shopping_hotels_and_flights_cashback_min_spend'][0]
		petrol_overall_cashback_cap = row['petrol_overall_cashback_cap'][0]
		petrol_others_cashback_rate = row['petrol_others_cashback_rate'][0]
		petrol_others_cashback_cap = row['petrol_others_cashback_cap'][0]
		petrol_others_cashback_min_spend = row['petrol_others_cashback_min_spend'][0]
		petrol_esso_cashback_rate = row['petrol_esso_cashback_rate'][0]
		petrol_esso_cashback_cap = row['petrol_esso_cashback_cap'][0]
		petrol_esso_cashback_min_spend = row['petrol_esso_cashback_min_spend'][0]
		petrol_caltex_cashback_rate = row['petrol_caltex_cashback_rate'][0]
		petrol_caltex_cashback_cap = row['petrol_caltex_cashback_cap'][0]
		petrol_caltex_cashback_min_spend = row['petrol_caltex_cashback_min_spend'][0]
		petrol_shell_cashback_rate = row['petrol_shell_cashback_rate'][0]
		petrol_shell_cashback_cap = row['petrol_shell_cashback_cap'][0]
		petrol_shell_cashback_min_spend = row['petrol_shell_cashback_min_spend'][0]
		
		class SpendingInput(Fact):
			bill_spending = Field(float)
			dining_spending = Field(float)
			foreign_spending = Field(float)
			retail_shopping_spending = Field(float)
			transport_spending = Field(float)
			groceries_others_spending = Field(float)
			groceries_ntuc_spending = Field(float)
			groceries_sheng_siong_spending = Field(float)
			groceries_cold_storage_spending = Field(float)
			groceries_giant_spending = Field(float)
			online_shopping_others_spending = Field(float)
			online_shopping_hotels_and_flight_spending = Field(float)
			petrol_others_spending = Field(float)
			petrol_esso_spending = Field(float)
			petrol_shell_spending = Field(float)
			petrol_caltex_spending = Field(float)
			pass 
		
		class Cashback(KnowledgeEngine):
			def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)
				self.cashback = 0
				self.bill_cashback = 0
				self.cashback_dining = 0
				self.cashback_foreign = 0
				self.cashback_foreign = 0
				self.cashback_retail = 0
				self.cashback_transport = 0
				self.cashback_groceries_others = 0
				self.cashback_groceries_ntuc = 0
				self.cashback_groceries_sheng_siong = 0
				self.cashback_groceries_cold_storage = 0
				self.cashback_groceries_giant = 0
				self.cashback_online_others = 0
				self.cashback_online_hotels_flights = 0
				self.cashback_petrol_others = 0
				self.cashback_petrol_esso = 0
				self.cashback_petrol_shell = 0
				self.cashback_petrol_caltex = 0
					
			#Bill Spending Cashback
			@Rule(AND(
                AS.v << SpendingInput(data__bill_spending = MATCH.data__bill_spending),
                TEST(lambda data__bill_spending: data__bill_spending >= bill_cashback_min_spend),
                AS.v << SpendingInput(data__bill_spending = MATCH.data__bill_spending),
                TEST(lambda data__bill_spending: data__bill_spending * bill_cashback_rate <= bill_cashback_cap)
                )
             )
			def cashback_bill_1(self, v):
				print("bill cashback within cap amount")
				self.bill_cashback = MATCH.data__bill_spending * bill_cashback_rate
				self.halt()
				
			@Rule(AND(
                AS.v << SpendingInput(data__bill_spending = MATCH.data__bill_spending),
                TEST(lambda data__bill_spending: data__bill_spending >= bill_cashback_min_spend),
                AS.v << SpendingInput(data__bill_spending = MATCH.data__bill_spending),
                TEST(lambda data__bill_spending: data__bill_spending * bill_cashback_rate > bill_cashback_cap)
                )
             )
			def cashback_bill_2(self, v):
				print("bill cashback exceed cap amount")
				self.bill_cashback = bill_cashback_cap
				self.halt()
				
			#Dining Spending Cashback
			@Rule(AND(
                AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
                TEST(lambda data__dining_spending: data__dining_spending >= dining_cashback_min_spend),
                AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
                TEST(lambda data__dining_spending: data__dining_spending * dining_cashback_rate <= dining_cashback_cap)
                )
             )
			def cashback_dining_1(self, v):
				print("dining cashback within cap amount")
				self.cashback_dining = MATCH.data__dining_spending * dining_cashback_rate)
				self.halt()
            
			@Rule(AND(
                AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
                TEST(lambda data__dining_spending: data__dining_spending >= dining_cashback_min_spend),
                AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
                TEST(lambda data__dining_spending: data__dining_spending * dining_cashback_rate > dining_cashback_cap)
                )
             )
			def cashback_dining_2(self, v):
				print("dining cashback exceed cap amount")
				self.cashback_dining = dining_cashback_cap
				self.halt()
			
			#foreign spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
                TEST(lambda data__foreign_spending: data__foreign_spending >= foreign_cashback_min_spend),
                AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
                TEST(lambda data__foreign_spending: data__foreign_spending * foreign_cashback_rate <= foreign_cashback_cap)
                )
             )
			def cashback_foreign_1(self, v):
				print("foreign cashback within cap amount")
				self.cashback_foreign = MATCH.data__foreign_spending * foreign_cashback_rate)
				self.halt()
				
			@Rule(AND(
                AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
                TEST(lambda data__foreign_spending: data__foreign_spending >= foreign_cashback_min_spend),
                AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
                TEST(lambda data__foreign_spending: data__foreign_spending * foreign_cashback_rate > foreign_cashback_cap)
                )
             )
			def cashback_foreign_2(self, v):
				print("foreign cashback exceed cap amount")
				self.cashback_foreign = foreign_cashback_cap
				self.halt()
				
			#retail spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__retail_spending = MATCH.data__retail_spending),
                TEST(lambda data__retail_spending: data__retail_spending >= retail_cashback_min_spend),
                AS.v << SpendingInput(data__retail_spending = MATCH.data__retail_spending),
                TEST(lambda data__retail_spending: data__retail_spending * retail_cashback_rate <= retail_cashback_cap)
                )
             )
			def cashback_retail_1(self, v):
				print("retail cashback within cap amount")
				self.cashback_retail = MATCH.data__retail_spending * retail_cashback_rate)
				self.halt()
            
			@Rule(AND(
                AS.v << SpendingInput(data__retail_spending = MATCH.data__retail_spending),
                TEST(lambda data__retail_spending: data__retail_spending >= retail_cashback_min_spend),
                AS.v << SpendingInput(data__retail_spending = MATCH.data__retail_spending),
                TEST(lambda data__retail_spending: data__retail_spending * retail_cashback_rate > retail_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				print("retail cashback exceed cap amount")
				self.cashback_retail = retail_cashback_cap
				self.halt()
            
			#transport spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__transport_spending = MATCH.data__transport_spending),
                TEST(lambda data__transport_spending: data__transport_spending >= transport_cashback_min_spend),
                AS.v << SpendingInput(data__transport_spending = MATCH.data__transport_spending),
                TEST(lambda data__transport_spending: data__transport_spending * transport_cashback_rate <= transport_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_transport = MATCH.data__transport_spending * transport_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__transport_spending = MATCH.data__transport_spending),
                TEST(lambda data__transport_spending: data__transport_spending >= transport_cashback_min_spend),
                AS.v << SpendingInput(data__transport_spending = MATCH.data__transport_spending),
                TEST(lambda data__transport_spending: data__transport_spending * transport_cashback_rate > transport_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_transport = trnasport_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()

				
				
			#groceries_others spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__groceries_others_spending = MATCH.data__groceries_others_spending),
                TEST(lambda data__groceries_others_spending: data__groceries_others_spending >= groceries_others_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_others_spending = MATCH.data__groceries_others_spending),
                TEST(lambda data__groceries_others_spending: data__groceries_others_spending * groceries_others_cashback_rate <= groceries_others_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_groceries_others = MATCH.data__groceries_others_spending * groceries_others_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__groceries_others_spending = MATCH.data__groceries_others_spending),
                TEST(lambda data__groceries_others_spending: data__groceries_others_spending >= groceries_others_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_others_spending = MATCH.data__groceries_others_spending),
                TEST(lambda data__groceries_others_spending: data__groceries_others_spending * groceries_others_cashback_rate > groceries_others_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_groceries_others = groceries_others_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
			
			#gorceries_ntuc spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__groceries_ntuc_spending = MATCH.data__groceries_ntuc_spending),
                TEST(lambda data__groceries_ntuc_spending: data__groceries_ntuc_spending >= groceries_ntuc_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_ntuc_spending = MATCH.data__groceries_ntuc_spending),
                TEST(lambda data__groceries_ntuc_spending: data__groceries_ntuc_spending * groceries_ntuc_cashback_rate <= groceries_ntuc_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_groceries_ntuc = MATCH.data__groceries_ntuc_spending * groceries_ntuc_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__groceries_ntuc_spending = MATCH.data__groceries_ntuc_spending),
                TEST(lambda data__groceries_ntuc_spending: data__groceries_ntuc_spending >= groceries_ntuc_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_ntuc_spending = MATCH.data__groceries_ntuc_spending),
                TEST(lambda data__groceries_ntuc_spending: data__groceries_ntuc_spending * groceries_ntuc_cashback_rate > groceries_ntuc_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_groceries_ntuc = groceries_ntuc_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
			
			
			#gorceries_sheng_siong spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__groceries_sheng_siong_spending = MATCH.data__groceries_sheng_siong_spending),
                TEST(lambda data__groceries_sheng_siong_spending: data__groceries_sheng_siong_spending >= groceries_sheng_siong_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_sheng_siong_spending = MATCH.data__groceries_sheng_siong_spending),
                TEST(lambda data__groceries_sheng_siong_spending: data__groceries_sheng_siong_spending * groceries_sheng_siong_cashback_rate <= groceries_sheng_siong_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_groceries_sheng_siong = MATCH.data__groceries_sheng_siong_spending * groceries_sheng_siong_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__groceries_sheng_siong_spending = MATCH.data__groceries_sheng_siong_spending),
                TEST(lambda data__groceries_sheng_siong_spending: data__groceries_sheng_siong_spending >= groceries_sheng_siong_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_sheng_siong_spending = MATCH.data__groceries_sheng_siong_spending),
                TEST(lambda data__groceries_sheng_siong_spending: data__groceries_sheng_siong_spending * groceries_sheng_siong_cashback_rate > groceries_sheng_siong_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_groceries_sheng_siong = groceries_sheng_siong_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
			
			#groceries_cold_storage spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__groceries_cold_storage_spending = MATCH.data__groceries_cold_storage_spending),
                TEST(lambda data__groceries_cold_storage_spending: data__groceries_cold_storage_spending >= groceries_cold_storage_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_cold_storage_spending = MATCH.data__groceries_cold_storage_spending),
                TEST(lambda data__groceries_cold_storage_spending: data__groceries_cold_storage_spending * groceries_cold_storage_cashback_rate <= groceries_cold_storage_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_groceries_cold_storage = MATCH.data__groceries_cold_storage_spending * groceries_cold_storage_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__groceries_cold_storage_spending = MATCH.data__groceries_cold_storage_spending),
                TEST(lambda data__groceries_cold_storage_spending: data__groceries_cold_storage_spending >= groceries_cold_storage_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_cold_storage_spending = MATCH.data__groceries_cold_storage_spending),
                TEST(lambda data__groceries_cold_storage_spending: data__groceries_cold_storage_spending * groceries_cold_storage_cashback_rate > groceries_cold_storage_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_groceries_cold_storage = groceries_cold_storage_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
			
			
			#groceries_giant spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__groceries_giant_spending = MATCH.data__groceries_giant_spending),
                TEST(lambda data__groceries_giant_spending: data__groceries_giant_spending >= groceries_giant_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_giant_spending = MATCH.data__groceries_giant_spending),
                TEST(lambda data__groceries_giant_spending: data__groceries_giant_spending * groceries_giant_cashback_rate <= groceries_giant_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_groceries_giant = MATCH.data__groceries_giant_spending * groceries_giant_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__groceries_giant_spending = MATCH.data__groceries_giant_spending),
                TEST(lambda data__groceries_giant_spending: data__groceries_giant_spending >= groceries_giant_cashback_min_spend),
                AS.v << SpendingInput(data__groceries_giant_spending = MATCH.data__groceries_giant_spending),
                TEST(lambda data__groceries_giant_spending: data__groceries_giant_spending * groceries_giant_cashback_rate > groceries_giant_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_groceries_giant = groceries_giant_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
			
			#online_others spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
                TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending >= online_shopping_others_cashback_min_spend),
                AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
                TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending * online_shopping_others_cashback_rate <= online_shopping_others_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_online_others = MATCH.data__online_shopping_others_spending * online_shopping_others_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
                TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending >= online_shopping_others_cashback_min_spend),
                AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
                TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending * online_shopping_others_cashback_rate > online_shopping_others_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_online_others = online_shopping_others_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
				
			#online_hotels_flights spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
                TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending >= online_shopping_hotels_and_flights_cashback_min_spend),
                AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
                TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending * online_shopping_hotels_and_flights_cashback_rate <= online_shopping_hotels_and_flights_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_online_hotels_flights = MATCH.data__online_shopping_hotels_and_flight_spending * online_shopping_hotels_and_flights_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
                TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending >= online_shopping_hotels_and_flights_cashback_min_spend),
                AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
                TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending * online_shopping_hotels_and_flights_cashback_rate > online_shopping_hotels_and_flights_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_online_hotels_flights = online_shopping_others_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
				
			#petrol_others spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__petrol_others_spending = MATCH.data__petrol_others_spending),
                TEST(lambda data__petrol_others_spending: data__petrol_others_spending >= petrol_others_cashback_min_spend),
                AS.v << SpendingInput(data__petrol_others_spending = MATCH.data__petrol_others_spending),
                TEST(lambda data__petrol_others_spending: data__petrol_others_spending * petrol_others_cashback_rate <= petrol_others_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_petrol_others = MATCH.data__petrol_others_spending * petrol_others_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__petrol_others_spending = MATCH.data__petrol_others_spending),
                TEST(lambda data__petrol_others_spending: data__petrol_others_spending >= petrol_others_cashback_min_spend),
                AS.v << SpendingInput(data__petrol_others_spending = MATCH.data__petrol_others_spending),
                TEST(lambda data__petrol_others_spending: data__petrol_others_spending * petrol_others_cashback_rate > petrol_others_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_petrol_others = petrol_others_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
			
			#petrol_esso spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__petrol_esso_spending = MATCH.data__petrol_esso_spending),
                TEST(lambda data__petrol_esso_spending: data__petrol_esso_spending >= petrol_esso_cashback_min_spend),
                AS.v << SpendingInput(data__petrol_esso_spending = MATCH.data__petrol_esso_spending),
                TEST(lambda data__petrol_esso_spending: data__petrol_esso_spending * petrol_esso_cashback_rate <= petrol_esso_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_petrol_esso = MATCH.data__petrol_esso_spending * petrol_esso_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__petrol_esso_spending = MATCH.data__petrol_esso_spending),
                TEST(lambda data__petrol_esso_spending: data__petrol_esso_spending >= petrol_esso_cashback_min_spend),
                AS.v << SpendingInput(data__petrol_esso_spending = MATCH.data__petrol_esso_spending),
                TEST(lambda data__petrol_esso_spending: data__petrol_esso_spending * petrol_esso_cashback_rate > petrol_esso_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_petrol_esso = petrol_esso_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
				
			#petrol_shell spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__petrol_shell_spending = MATCH.data__petrol_shell_spending),
                TEST(lambda data__petrol_shell_spending: data__petrol_shell_spending >= petrol_shell_cashback_min_spend),
                AS.v << SpendingInput(data__petrol_shell_spending = MATCH.data__petrol_shell_spending),
                TEST(lambda data__petrol_shell_spending: data__petrol_shell_spending * petrol_shell_cashback_rate <= petrol_shell_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_petrol_shell = MATCH.data__petrol_shell_spending * petrol_shell_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__petrol_shell_spending = MATCH.data__petrol_shell_spending),
                TEST(lambda data__petrol_shell_spending: data__petrol_shell_spending >= petrol_shell_cashback_min_spend),
                AS.v << SpendingInput(data__petrol_shell_spending = MATCH.data__petrol_shell_spending),
                TEST(lambda data__petrol_shell_spending: data__petrol_shell_spending * petrol_shell_cashback_rate > petrol_shell_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_petrol_shell = petrol_shell_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
				
			
			#petrol_caltex spending cashback
			@Rule(AND(
                AS.v << SpendingInput(data__petrol_caltex_spending = MATCH.data__petrol_caltex_spending),
                TEST(lambda data__petrol_caltex_spending: data__petrol_caltex_spending >= petrol_caltex_cashback_min_spend),
                AS.v << SpendingInput(data__petrol_caltex_spending = MATCH.data__petrol_caltex_spending),
                TEST(lambda data__petrol_caltex_spending: data__petrol_caltex_spending * petrol_caltex_cashback_rate <= petrol_caltex_cashback_cap)
                )
             )
			def cashback_transport_1(self, v):
				self.cashback_petrol_caltex = MATCH.data__petrol_caltex_spending * petrol_caltex_cashback_rate)
				print("transport cashback within cap amount")
				self.halt()

			@Rule(AND(
                AS.v << SpendingInput(data__petrol_caltex_spending = MATCH.data__petrol_caltex_spending),
                TEST(lambda data__petrol_caltex_spending: data__petrol_caltex_spending >= petrol_caltex_cashback_min_spend),
                AS.v << SpendingInput(data__petrol_caltex_spending = MATCH.data__petrol_caltex_spending),
                TEST(lambda data__petrol_caltex_spending: data__petrol_caltex_spending * petrol_caltex_cashback_rate > petrol_caltex_cashback_cap)
                )
             )
			def cashback_retail_2(self, v):
				self.cashback_petrol_caltex = petrol_caltex_cashback_cap
				print("transport cashback exceed cap amount")
				self.halt()
			
			
			##check for groceries overall
			groceries_overall = engine.cashback_groceries_others + engine.cashback_groceries_ntuc + engine.cashback_groceries_sheng_siong + engine.cashback_groceries_cold_storage + engine.cashback_groceries_giant
			if groceries_overall > groceries_overall_cashback_cap:
				groceries_overall = groceries_overall_cashback_cap
				
			##check for online overall
			online_overall = engine.cashback_online_others + engine.cashback_online_hotels_flights
			if online_overall > online_shopping_overall_cashback_cap
				online_overall = online_shopping_overall_cashback_cap
				
			##check for petrol overall
			petrol_overall = engine.cashback_petrol_others + engine.cashback_petrol_esso + engine.cashback_petrol_shell + engine.cashback_petrol_caltex
			if petrol_overall > petrol_overall_cashback_cap:
				petrol_overall = petrol_overall_cashback_cap
				
			##check contactless overall
			cashback_overall = groceries_overall + online_overall + petrol_overall + engine.bill_cashback + engine.cashback_dining + engine.cashback_foreign + engine.cashback_retail + engine.cashback_transport
			contactless_CF = 0.75
			if cashback_overall >= contactless_cashback_min:
				if cashback_overall * contactless_CF * contactless_cashback_rate <= contactless_cashback_cap:
					contactless_cashback = cashback_overall * contactless_CF * contactless_cashback_rate
				else:
					contactless_cashback = contactless_cashback_cap
			
			##cashback overall amount
			cashback = cashback_overall + contactless_cashback
			
			if debug:
				print("Applicant Info:", dict_of_personal_info)
				print("Card Info: ID is %s, Name is %s, age_min is %f, age_max is %f, gender is %s, annual_income_singaporean_min is %f, annual_income_pr_min is %f, annual_income_foreigner_min is %f"
                  %(cardid, credit_card_name, age__min, age__max, gender__req, annual_income_singaporean_min, annual_income_pr_min, annual_income_foreigner_min))
			engine=Eligibility()
			engine.reset()
			engine.declare(SpendingInput(data=dict_of_personal_info))
			engine.run()
			engine.facts
			available_cards = available_cards.append({'available_cards_id':cardid, 'cashback_amount':cashback}, ignore_index=True)
        
		return available_cards
			
			
			
			