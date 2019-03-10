from random import choice
from pyknow import *
from .fuzzy_logic import *

def return_eligibile_credit_card_ids(dict_of_personal_info, list_of_dict_of_credit_card_eligibility_info, debug=False):

    eligible_card_ids = {'eligible_credit_card_ids':[]}

    for row in list_of_dict_of_credit_card_eligibility_info:
        class Person(Fact):
            age = Field(int)
            gender = Field(str)
            citizenship = Field(str)
            annual_income = Field(int)
            total_spending_amount = Field(int)
            pass

        class Eligibility(KnowledgeEngine):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.eligible_status = True

            # Applicant is too young
            @Rule(AS.v << Person(data__age = MATCH.data__age),
                TEST(lambda data__age: data__age < age__min), salience=1)
            def too_young(self):
                print("Cardid %s, Too young, less than %s" %(cardid, age__min))
                self.eligible_status = False
                self.halt()

            # Applicant is too old
            @Rule(AS.v << Person(data__age = MATCH.data__age),
                TEST(lambda data__age: data__age > age__max), salience=1)
            def too_old(self):
                print("Cardid %s, Too old, more than %s" %(cardid, age__max))
                self.eligible_status = False
                self.halt()   

            # Applicant is wrong gender
            @Rule(AS.v << Person(data__gender = MATCH.data__gender),
                TEST(lambda data__gender: (data__gender == 'male') & (gender__req == 'F' or gender__req == 'f')))
            def wrong_gender(self):
                print("Cardid %s, Wrong gender, this card is only for %s" %(cardid, gender__req))
                self.eligible_status = False
                self.halt()

            # Applicant is Singaporean and spends less than the minimum requirement
            @Rule(AND(
                    AS.v << Person(data__citizenship = MATCH.data__citizenship),
                    TEST(lambda data__citizenship: data__citizenship == 'singaporean'),
                    AS.v << Person(data__annual_income = MATCH.data__annual_income),
                    TEST(lambda data__annual_income: data__annual_income < annual_income_singaporean_min),    
                    ))
            def singaporean_too_poor(self):
                print("Cardid %s, Singaporean, does not meet min spending of %s" %(cardid, annual_income_singaporean_min))
                self.eligible_status = False
                self.halt()

            # Applicant is pr and spends less than the minimum requirement
            @Rule(AND(
                    AS.v << Person(data__citizenship = MATCH.data__citizenship),
                    TEST(lambda data__citizenship: data__citizenship == 'pr'),
                    AS.v << Person(data__annual_income = MATCH.data__annual_income),
                    TEST(lambda data__annual_income: data__annual_income < annual_income_pr_min),    
                    ))
            def pr_too_poor(self):
                print("Cardid %s, PR, does not meet min spending of %s" %(cardid, annual_income_pr_min))
                self.eligible_status = False
                self.halt()

            # Applicant is Foreigner and spends less than the minimum requirement
            @Rule(AND(
                    AS.v << Person(data__citizenship = MATCH.data__citizenship),
                    TEST(lambda data__citizenship: data__citizenship == 'foreigner'),
                    AS.v << Person(data__annual_income = MATCH.data__annual_income),
                    TEST(lambda data__annual_income: data__annual_income < annual_income_foreigner_min),    
                    ))
            def foreigner_too_poor(self):
                print("Cardid %s, Foreigner, does not meet min spending of %s" %(cardid, annual_income_foreigner_min))
                self.eligible_status = False
                self.halt()
        
        cardid = str(row['credit_card_id'][0])
        credit_card_name = str(row['credit_card_name'][0])
        age__min = row['age_min'][0]
        age__max = row['age_max'][0]
        gender__req = row['gender_req'][0]
        annual_income_singaporean_min = row['annual_income_singaporean_min'][0]
        annual_income_pr_min = row['annual_income_pr_min'][0]
        annual_income_foreigner_min = row['annual_income_foreigner_min'][0]
        if debug:
            print("Applicant Info:", dict_of_personal_info)
            print("Card Info: ID is %s, Name is %s, age_min is %f, age_max is %f, gender is %s, annual_income_singaporean_min is %f, annual_income_pr_min is %f, annual_income_foreigner_min is %f"
                  %(cardid, credit_card_name, age__min, age__max, gender__req, annual_income_singaporean_min, annual_income_pr_min, annual_income_foreigner_min))
        engine=Eligibility()
        engine.reset()
        engine.declare(Person(data=dict_of_personal_info))
        engine.run()
        engine.facts
        if debug:
            print(engine.eligible_status)
            print("\n")
        if engine.eligible_status:
            eligible_card_ids['eligible_credit_card_ids'].append(cardid)
    return eligible_card_ids

def return_preferred_credit_card_ids(dict_of_preference_info, list_of_dict_of_credit_card_preference_info, debug=False):
    preferred_credit_card_ids = {'preferred_credit_card_ids':[]}
    
    for row in list_of_dict_of_credit_card_preference_info:
        class PreferenceInput(Fact):
            preferred_bank = Field(str)
            preferred_card_type = Field(str)
            preferred_rewards_type = Field(str)
            pass

        class Preference(KnowledgeEngine):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.prefered = None
            # If any part of Credit Card's Bank is within preferred list (if sets intersect)
            # AND if any part of Credit Card's payment network is within preferred paymnent network (if sets intersect)
            # AND if any part of Credit Card reward type is within preferred reward card type (if sets intersect)
            @Rule(AND(AS.v << PreferenceInput(data__preferred_bank = MATCH.data__preferred_bank),
                      TEST(lambda data__preferred_bank: bool(set(data__preferred_bank) & set(bank_name))),
                      AS.v << PreferenceInput(data__preferred_card_type = MATCH.data__preferred_card_type),
                      TEST(lambda data__preferred_card_type: bool(set(data__preferred_card_type) & set(payment_networks))),
                      AS.v << PreferenceInput(data__preferred_rewards_type = MATCH.data__preferred_rewards_type),
                      TEST(lambda data__preferred_rewards_type: bool(set(data__preferred_rewards_type) & set(card_type))) ))
            def bank_within_preferred_and_in_payment_network(self, v):
                print("Cardid %s, %s is a preferred bank and %s payment network intersects and %s rewards type intersects" %(cardid, bank_name[0], ' '.join(payment_networks), ' '.join(card_type)))
                self.prefered = True
                self.halt()
                
            # Credit Card's Bank is NOT within preferred list
            @Rule(AS.v << PreferenceInput(data__preferred_bank = MATCH.data__preferred_bank),
                  TEST(lambda data__preferred_bank: bool(set(data__preferred_bank) & set(bank_name)) == False), salience=10)
            def bank_not_within_preferred(self, v):
                print("Cardid %s, %s is not a preferred bank" %(cardid, bank_name))
                self.prefered = False
                self.halt()
                
            # Credit Card's Bank is NOT within payment network
            @Rule(AS.v << PreferenceInput(data__preferred_card_type = MATCH.data__preferred_card_type),
                  TEST(lambda data__preferred_card_type: bool(set(payment_networks) & set(data__preferred_card_type)) == False), salience=10)
            def credit_card_not_in_payment_network(self, v):
                print("Cardid %s, %s not within preferred payment network " %(cardid,' '.join(payment_networks)))
                self.prefered = False
                self.halt()
            
            # Credit Card's Reward Type is NOT within preferred reward type
            @Rule(AS.v << PreferenceInput(data__preferred_rewards_type = MATCH.data__preferred_rewards_type),
                  TEST(lambda data__preferred_rewards_type: bool(set(card_type) & set(data__preferred_rewards_type)) == False), salience=10)
            def credit_card_not_in_rewards_type(self, v):
                print("Cardid %s, %s not within preferred rewards type " %(cardid,' '.join(card_type)))
                self.prefered = False
                self.halt()
                
        cardid = str(row['credit_card_id'][0])
        credit_card_name = str(row['credit_card_name'][0])
        bank_name = row['bank_name']
        payment_networks = row['payment_networks']
        card_type = row['card_type']
        
        engine = Preference()
        engine.reset()
        engine.declare(PreferenceInput(data=dict_of_preference_info))
        engine.run()
        if debug:       
            print(row)
            print(preference_info)
            print(engine.prefered)
            print("\n")
        if engine.prefered:
            preferred_credit_card_ids['preferred_credit_card_ids'].append(cardid)
    return preferred_credit_card_ids

def return_eligible_spendings_for_breakdown(dict_of_spending_checkbox_info, debug=False):
    eligible_spending = {'eligible_spending':[]}
    for key in dict_of_spending_checkbox_info:
        val = dict_of_spending_checkbox_info[key]
        if  val == 1:
            eligible_spending['eligible_spending'].append('_'.join(key.split("_")[0:-1]))
    return eligible_spending


def return_cashback_value(dict_of_spending_amounts_info, dict_of_preferred_credit_card_spending_rewards_info, contactless_CF, debug=False):
    
    cashback_value = 0
    
    dictt = dict_of_spending_amounts_info
    row = dict_of_preferred_credit_card_spending_rewards_info
    total_spending = sum([dict_of_spending_amounts_info[key] for key in dict_of_spending_amounts_info.keys()])
    multiple_levels = row['multiple_levels'][0]
    overall_cashback_min_spend = row['overall_cashback_min_spend']
    if debug:
        print(dict_of_spending_amounts_info)
        print(dict_of_preferred_credit_card_spending_rewards_info)
        print("Overall Cashback Min Spend", overall_cashback_min_spend)
        print("Multiple Levels", multiple_levels)
    
    ## Get index if there are multiple levels ##
    if multiple_levels == 0:
        index = 0
        if total_spending < overall_cashback_min_spend[0]:
            print("Did not hit the overall minimum spending, no cashback given")
            cashback_value = 0
            return cashback_value
    elif multiple_levels == 1:
        if total_spending < overall_cashback_min_spend[0]:
            print("Did not hit the overall minimum spending, no cashback given")
            cashback_value = 0
            return cashback_value
        for i in range(len(overall_cashback_min_spend)):
            if total_spending >= overall_cashback_min_spend[i]:
                index = i
    else:
        print("ERROR")
    
    cardid = str(row['credit_card_id'][0])
    credit_card_name = str(row['credit_card_name'][0])
    overall_cashback_cap = row['overall_cashback_cap'][index]
    contactless_cashback_rate = row['contactless_cashback_rate'][index]
    contactless_cashback_cap = row['contactless_cashback_cap'][index]
    contactless_cashback_min = row['contactless_cashback_min_spend'][index]
    bill_cashback_rate = row['bill_cashback_rate'][index]
    bill_cashback_cap = row['bill_cashback_cap'][index]
    bill_cashback_min_spend = row['bill_cashback_min_spend'][index]
    dining_cashback_rate = row['dining_cashback_rate'][index]
    dining_cashback_cap = row['dining_cashback_cap'][index]
    dining_cashback_min_spend = row['dining_cashback_min_spend'][index]
    foreign_cashback_rate = row['foreign_cashback_rate'][index]
    foreign_cashback_cap = row['foreign_cashback_cap'][index]
    foreign_cashback_min_spend = row['foreign_cashback_min_spend'][index]
    retail_shopping_cashback_rate = row['retail_shopping_cashback_rate'][index]
    retail_shopping_cashback_cap = row['retail_shopping_cashback_cap'][index]
    retail_shopping_cashback_min_spend = row['retail_shopping_cashback_min_spend'][index]
    transport_cashback_rate = row['transport_cashback_rate'][index]
    transport_cashback_cap = row['transport_cashback_cap'][index]
    transport_cashback_min_spend = row['transport_cashback_min_spend'][index]
    groceries_overall_cashback_cap = row['groceries_overall_cashback_cap'][index]
    groceries_others_cashback_rate = row['groceries_others_cashback_rate'][index]
    groceries_others_cashback_cap = row['groceries_others_cashback_cap'][index]
    groceries_others_cashback_min_spend = row['groceries_others_cashback_min_spend'][index]
    groceries_ntuc_cashback_rate = row['groceries_ntuc_cashback_rate'][index]
    groceries_ntuc_cashback_cap = row['groceries_ntuc_cashback_cap'][index]
    groceries_ntuc_cashback_min_spend = row['groceries_ntuc_cashback_min_spend'][index]
    groceries_sheng_siong_cashback_rate = row['groceries_sheng_siong_cashback_rate'][index]
    groceries_sheng_siong_cashback_cap = row['groceries_sheng_siong_cashback_cap'][index]
    groceries_sheng_siong_cashback_min_spend = row['groceries_sheng_siong_cashback_min_spend'][index]
    groceries_cold_storage_cashback_rate = row['groceries_cold_storage_cashback_rate'][index]
    groceries_cold_storage_cashback_cap = row['groceries_cold_storage_cashback_cap'][index]
    groceries_cold_storage_cashback_min_spend = row['groceries_cold_storage_cashback_min_spend'][index]
    groceries_giant_cashback_rate = row['groceries_giant_cashback_rate'][index]
    groceries_giant_cashback_cap = row['groceries_giant_cashback_cap'][index]
    groceries_giant_cashback_min_spend = row['groceries_giant_cashback_min_spend'][index]
    online_shopping_overall_cashback_cap = row['online_shopping_overall_cashback_cap'][index]
    online_shopping_others_cashback_rate = row['online_shopping_others_cashback_rate'][index]
    online_shopping_others_cashback_cap = row['online_shopping_others_cashback_cap'][index]
    online_shopping_others_cashback_min_spend = row['online_shopping_others_cashback_min_spend'][index]
    online_shopping_hotels_and_flights_cashback_rate = row['online_shopping_hotels_and_flights_cashback_rate'][index]
    online_shopping_hotels_and_flights_cashback_cap = row['online_shopping_hotels_and_flights_cashback_cap'][index]
    online_shopping_hotels_and_flights_cashback_min_spend = row['online_shopping_hotels_and_flights_cashback_min_spend'][index]
    petrol_overal_cashback_cap = row['petrol_overal_cashback_cap'][index]
    petrol_others_cashback_rate = row['petrol_others_cashback_rate'][index]
    petrol_others_cashback_cap = row['petrol_others_cashback_cap'][index]
    petrol_others_cashback_min_spend = row['petrol_others_cashback_min_spend'][index]
    petrol_esso_cashback_rate = row['petrol_esso_cashback_rate'][index]
    petrol_esso_cashback_cap = row['petrol_esso_cashback_cap'][index]
    petrol_esso_cashback_min_spend = row['petrol_esso_cashback_min_spend'][index]
    petrol_caltex_cashback_rate = row['petrol_caltex_cashback_rate'][index]
    petrol_caltex_cashback_cap = row['petrol_caltex_cashback_cap'][index]
    petrol_caltex_cashback_min_spend = row['petrol_caltex_cashback_min_spend'][index]
    petrol_shell_cashback_rate = row['petrol_shell_cashback_rate'][index]
    petrol_shell_cashback_cap = row['petrol_shell_cashback_cap'][index]
    petrol_shell_cashback_min_spend = row['petrol_shell_cashback_min_spend'][index]
    
    bill_spending_ = dictt['bill_spending']
    dining_spending_ = dictt['dining_spending']
    foreign_spending_ = dictt['foreign_spending']
    retail_shopping_spending_ = dictt['retail_shopping_spending']
    transport_spending_ = dictt['transport_spending']
    groceries_others_spending_ = dictt['groceries_others_spending']
    groceries_ntuc_spending_ = dictt['groceries_ntuc_spending']
    groceries_sheng_siong_spending_ = dictt['groceries_sheng_siong_spending']
    groceries_cold_storage_spending_ = dictt['groceries_cold_storage_spending']
    groceries_giant_spending_ = dictt['groceries_giant_spending']
    online_shopping_others_spending_ = dictt['online_shopping_others_spending']
    online_shopping_hotels_and_flight_spending_ = dictt['online_shopping_hotels_and_flight_spending']
    petrol_others_spending_ = dictt['petrol_others_spending']
    petrol_esso_spending_ = dictt['petrol_esso_spending']
    petrol_shell_spending_ = dictt['petrol_shell_spending']
    petrol_caltex_spending_ = dictt['petrol_caltex_spending']

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
        @Rule(AND(AS.v << SpendingInput(data__bill_spending = MATCH.data__bill_spending),
                  TEST(lambda data__bill_spending: data__bill_spending >= bill_cashback_min_spend),
                  AS.v << SpendingInput(data__bill_spending = MATCH.data__bill_spending),
                  TEST(lambda data__bill_spending: data__bill_spending * bill_cashback_rate <= bill_cashback_cap)))
        def cashback_bill_1(self, v):
            self.bill_cashback = bill_spending_*bill_cashback_rate
            print("bill cashback within cap amount, %f earned" %(self.bill_cashback))
        @Rule(AND(AS.v << SpendingInput(data__bill_spending = MATCH.data__bill_spending),
                  TEST(lambda data__bill_spending: data__bill_spending >= bill_cashback_min_spend),
                  AS.v << SpendingInput(data__bill_spending = MATCH.data__bill_spending),
                  TEST(lambda data__bill_spending: data__bill_spending * bill_cashback_rate > bill_cashback_cap)))
        def cashback_bill_2(self, v):
            self.bill_cashback = bill_cashback_cap
            print("bill cashback exceed cap amount, %f earned" %(self.bill_cashback))
            
        #Dining Spending Cashback
        @Rule(AND(AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
                  TEST(lambda data__dining_spending: data__dining_spending >= dining_cashback_min_spend),
                  AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
                  TEST(lambda data__dining_spending: data__dining_spending * dining_cashback_rate <= dining_cashback_cap)))
        def cashback_dining_1(self, v):
            self.cashback_dining = dining_spending_*dining_cashback_rate
            print("dining cashback within cap amount, %f earned" %(self.cashback_dining))
        @Rule(AND(AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
                  TEST(lambda data__dining_spending: data__dining_spending >= dining_cashback_min_spend),
                  AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
                  TEST(lambda data__dining_spending: data__dining_spending * dining_cashback_rate > dining_cashback_cap)))
        def cashback_dining_2(self, v):
            self.cashback_dining = dining_cashback_cap
            print("dining cashback exceed cap amount, %f earned" %(self.cashback_dining))
            
        #foreign spending cashback
        @Rule(AND(AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
                 TEST(lambda data__foreign_spending: data__foreign_spending >= foreign_cashback_min_spend),
                 AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
                 TEST(lambda data__foreign_spending: data__foreign_spending * foreign_cashback_rate <= foreign_cashback_cap)))
        def cashback_foreign_1(self, v):
            self.cashback_foreign = foreign_spending_*foreign_cashback_rate
            print("foreign cashback within cap amount, %f earned" %(self.cashback_foreign))
        @Rule(AND(AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
                  TEST(lambda data__foreign_spending: data__foreign_spending >= foreign_cashback_min_spend),
                  AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
                  TEST(lambda data__foreign_spending: data__foreign_spending * foreign_cashback_rate > foreign_cashback_cap)))
        def cashback_foreign_2(self, v):
            self.cashback_foreign = foreign_cashback_cap
            print("foreign cashback exceed cap amount, %f earned" %(self.cashback_foreign))

        #retail spending cashback
        @Rule(AND( AS.v << SpendingInput(data__retail_spending = MATCH.data__retail_spending),
                  TEST(lambda data__retail_spending: data__retail_spending >= retail_cashback_min_spend),
                  AS.v << SpendingInput(data__retail_spending = MATCH.data__retail_spending),
                  TEST(lambda data__retail_spending: data__retail_spending * retail_cashback_rate <= retail_cashback_cap)))
        def cashback_retail_1(self, v):
            self.cashback_retail = retail_spending_*retail_cashback_rate
            print("retail cashback within cap amount, %f earned" %(self.cashback_retail))
        @Rule(AND(AS.v << SpendingInput(data__retail_spending = MATCH.cashback_retail),
                  TEST(lambda data__retail_spending: data__retail_spending >= retail_cashback_min_spend),
                  AS.v << SpendingInput(data__retail_spending = MATCH.data__retail_spending),
                  TEST(lambda data__retail_spending: data__retail_spending * retail_cashback_rate > retail_cashback_cap)))
        def cashback_retail_2(self, v):
            self.cashback_retail = retail_cashback_cap
            print("retail cashback exceed cap amount, %f earned" %(self.cashback_retail))

        #transport spending cashback
        @Rule(AND(AS.v << SpendingInput(data__transport_spending = MATCH.data__transport_spending),
                  TEST(lambda data__transport_spending: data__transport_spending >= transport_cashback_min_spend),
                  AS.v << SpendingInput(data__transport_spending = MATCH.data__transport_spending),
                  TEST(lambda data__transport_spending: data__transport_spending * transport_cashback_rate <= transport_cashback_cap)))
        def cashback_transport_1(self, v):
            self.cashback_transport = transport_spending_*transport_cashback_rate
            print("transport cashback within cap amount, %f earned" %(self.cashback_transport))
        @Rule(AND(AS.v << SpendingInput(data__transport_spending = MATCH.data__transport_spending),
                  TEST(lambda data__transport_spending: data__transport_spending >= transport_cashback_min_spend),
                  AS.v << SpendingInput(data__transport_spending = MATCH.data__transport_spending),
                  TEST(lambda data__transport_spending: data__transport_spending * transport_cashback_rate > transport_cashback_cap)))
        def cashback_transport_2(self, v):
            self.cashback_transport = transport_cashback_cap
            print("transport cashback exceed cap amount, %f earned" %(self.cashback_transport))
        
        #groceries_others spending cashback
        @Rule(AND(AS.v << SpendingInput(data__groceries_others_spending = MATCH.data__groceries_others_spending),
                  TEST(lambda data__groceries_others_spending: data__groceries_others_spending >= groceries_others_cashback_min_spend),
                  AS.v << SpendingInput(data__groceries_others_spending = MATCH.data__groceries_others_spending),
                  TEST(lambda data__groceries_others_spending: data__groceries_others_spending * groceries_others_cashback_rate <= groceries_others_cashback_cap)))
        def groceries_others_1(self, v):
            self.cashback_groceries_others = groceries_others_spending_*groceries_others_cashback_rate
            print("groceries_others cashback within cap amount, %f earned" %(self.cashback_groceries_others))
        @Rule(AND(AS.v << SpendingInput(data__groceries_others_spending = MATCH.data__groceries_others_spending),
                  TEST(lambda data__groceries_others_spending: data__groceries_others_spending >= groceries_others_cashback_min_spend),
                  AS.v << SpendingInput(data__groceries_others_spending = MATCH.data__groceries_others_spending),
                  TEST(lambda data__groceries_others_spending: data__groceries_others_spending * groceries_others_cashback_rate > groceries_others_cashback_cap)))
        def groceries_others_2(self, v):
            self.cashback_groceries_others = groceries_others_cashback_cap
            print("groceries_others cashback exceed cap amount, %f earned" %(self.cashback_groceries_others))
            
        #groceries_ntuc spending cashback
        @Rule(AND(AS.v << SpendingInput(data__groceries_ntuc_spending = MATCH.data__groceries_ntuc_spending),
                  TEST(lambda data__groceries_ntuc_spending: data__groceries_ntuc_spending >= groceries_ntuc_cashback_min_spend),
                  AS.v << SpendingInput(data__groceries_ntuc_spending = MATCH.data__groceries_ntuc_spending),
                  TEST(lambda data__groceries_ntuc_spending: data__groceries_ntuc_spending * groceries_ntuc_cashback_rate <= groceries_ntuc_cashback_cap)))
        def groceries_ntuc_1(self, v):
            self.cashback_groceries_ntuc = groceries_ntuc_spending_*groceries_ntuc_cashback_rate
            print("groceries_ntuc cashback within cap amount, %f earned" %(self.cashback_groceries_ntuc))
        @Rule(AND(AS.v << SpendingInput(data__groceries_ntuc_spending = MATCH.data__groceries_ntuc_spending),
                 TEST(lambda data__groceries_ntuc_spending: data__groceries_ntuc_spending >= groceries_ntuc_cashback_min_spend),
                 AS.v << SpendingInput(data__groceries_ntuc_spending = MATCH.data__groceries_ntuc_spending),
                 TEST(lambda data__groceries_ntuc_spending: data__groceries_ntuc_spending * groceries_ntuc_cashback_rate > groceries_ntuc_cashback_cap)))
        def groceries_ntuc_2(self, v):
            self.cashback_groceries_ntuc = groceries_ntuc_cashback_cap
            print("groceries_ntuc cashback exceed cap amount, %f earned" %(self.cashback_groceries_ntuc))

        #groceries_sheng_siong spending cashback
        @Rule(AND(AS.v << SpendingInput(data__groceries_sheng_siong_spending = MATCH.data__groceries_sheng_siong_spending),
                  TEST(lambda data__groceries_sheng_siong_spending: data__groceries_sheng_siong_spending >= groceries_sheng_siong_cashback_min_spend),
                  AS.v << SpendingInput(data__groceries_sheng_siong_spending = MATCH.data__groceries_sheng_siong_spending),
                  TEST(lambda data__groceries_sheng_siong_spending: data__groceries_sheng_siong_spending * groceries_sheng_siong_cashback_rate <= groceries_sheng_siong_cashback_cap)))
        def groceries_sheng_siong_1(self, v):
            self.cashback_groceries_sheng_siong = groceries_sheng_siong_spending_*groceries_sheng_siong_cashback_rate
            print("groceries_sheng_siong cashback within cap amount, %f earned" %(self.cashback_groceries_sheng_siong))
        @Rule(AND(AS.v << SpendingInput(data__groceries_sheng_siong_spending = MATCH.data__groceries_sheng_siong_spending),
                  TEST(lambda data__groceries_sheng_siong_spending: data__groceries_sheng_siong_spending >= groceries_sheng_siong_cashback_min_spend),
                  AS.v << SpendingInput(data__groceries_sheng_siong_spending = MATCH.data__groceries_sheng_siong_spending),
                  TEST(lambda data__groceries_sheng_siong_spending: data__groceries_sheng_siong_spending * groceries_sheng_siong_cashback_rate > groceries_sheng_siong_cashback_cap)))
        def groceries_sheng_siong_2(self, v):
            self.cashback_groceries_sheng_siong = groceries_sheng_siong_cashback_cap
            print("groceries_sheng_siong cashback exceed cap amount, %f earned" %(self.cashback_groceries_sheng_siong))

        #groceries_cold_storage spending cashback
        @Rule(AND(AS.v << SpendingInput(data__groceries_cold_storage_spending = MATCH.data__groceries_cold_storage_spending),
                  TEST(lambda data__groceries_cold_storage_spending: data__groceries_cold_storage_spending >= groceries_cold_storage_cashback_min_spend),
                  AS.v << SpendingInput(data__groceries_cold_storage_spending = MATCH.data__groceries_cold_storage_spending),
                  TEST(lambda data__groceries_cold_storage_spending: data__groceries_cold_storage_spending * groceries_cold_storage_cashback_rate <= groceries_cold_storage_cashback_cap)))
        def groceries_cold_storage_1(self, v):
            self.cashback_groceries_cold_storage = groceries_cold_storage_spending_*groceries_cold_storage_cashback_rate
            print("groceries_cold_storage cashback within cap amount, %f earned" %(self.cashback_groceries_cold_storage))
        @Rule(AND(AS.v << SpendingInput(data__groceries_cold_storage_spending = MATCH.data__groceries_cold_storage_spending),
                  TEST(lambda data__groceries_cold_storage_spending: data__groceries_cold_storage_spending >= groceries_cold_storage_cashback_min_spend),
                  AS.v << SpendingInput(data__groceries_cold_storage_spending = MATCH.data__groceries_cold_storage_spending),
                  TEST(lambda data__groceries_cold_storage_spending: data__groceries_cold_storage_spending * groceries_cold_storage_cashback_rate > groceries_cold_storage_cashback_cap)))
        def groceries_cold_storage_2(self, v):
            self.cashback_groceries_cold_storage = groceries_cold_storage_cashback_cap
            print("groceries_cold_storage cashback exceed cap amount, %f earned" %(self.cashback_groceries_cold_storage))


        #groceries_giant spending cashback
        @Rule(AND(AS.v << SpendingInput(data__groceries_giant_spending = MATCH.data__groceries_giant_spending),
            TEST(lambda data__groceries_giant_spending: data__groceries_giant_spending >= groceries_giant_cashback_min_spend),
            AS.v << SpendingInput(data__groceries_giant_spending = MATCH.data__groceries_giant_spending),
            TEST(lambda data__groceries_giant_spending: data__groceries_giant_spending * groceries_giant_cashback_rate <= groceries_giant_cashback_cap)))
        def groceries_giant_1(self, v):
            self.cashback_groceries_giant = groceries_giant_spending_*groceries_giant_cashback_rate
            print("groceries_giant cashback within cap amount, %f earned" %(self.cashback_groceries_giant))
        @Rule(AND(AS.v << SpendingInput(data__groceries_giant_spending = MATCH.data__groceries_giant_spending),
                  TEST(lambda data__groceries_giant_spending: data__groceries_giant_spending >= groceries_giant_cashback_min_spend),
                  AS.v << SpendingInput(data__groceries_giant_spending = MATCH.data__groceries_giant_spending),
                  TEST(lambda data__groceries_giant_spending: data__groceries_giant_spending * groceries_giant_cashback_rate > groceries_giant_cashback_cap)))
        def groceries_giant_2(self, v):
            self.cashback_groceries_giant = groceries_giant_cashback_cap
            print("groceries_giant cashback exceed cap amount, %f earned" %(self.cashback_groceries_giant))
                
        #online_others spending cashback
        @Rule(AND(AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
                  TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending >= online_shopping_others_cashback_min_spend),
                  AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
                  TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending * online_shopping_others_cashback_rate <= online_shopping_others_cashback_cap)))
        def online_others_1(self, v):
            self.cashback_online_others = online_shopping_others_spending_*online_shopping_others_cashback_rate
            print("online_others cashback within cap amount, %f earned" %(self.cashback_online_others))
        @Rule(AND(AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
                  TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending >= online_shopping_others_cashback_min_spend),
                  AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
                  TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending * online_shopping_others_cashback_rate > online_shopping_others_cashback_cap)))
        def online_others_2(self, v):
            self.cashback_online_others = online_shopping_others_cashback_cap
            print("online_others cashback exceed cap amount, %f earned" %(self.cashback_online_others))

        #online_hotels_flights spending cashback
        @Rule(AND(AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
                  TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending >= online_shopping_hotels_and_flights_cashback_min_spend),
                  AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
                  TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending * online_shopping_hotels_and_flights_cashback_rate <= online_shopping_hotels_and_flights_cashback_cap)))
        def online_hotels_flights_1(self, v):
            self.cashback_online_hotels_flights = online_shopping_hotels_and_flight_spending_*online_shopping_hotels_and_flights_cashback_rate
            print("online_hotels_flights cashback within cap amount, %f earned" %(self.cashback_online_hotels_flights))
        @Rule(AND(AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
                  TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending >= online_shopping_hotels_and_flights_cashback_min_spend),
                  AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
                  TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending * online_shopping_hotels_and_flights_cashback_rate > online_shopping_hotels_and_flights_cashback_cap)))
        def online_hotels_flights_2(self, v):
            self.cashback_online_hotels_flights = online_shopping_others_cashback_cap
            print("online_hotels_flights cashback exceed cap amount, %f earned" %(self.cashback_online_hotels_flights))
            
    
        #petrol_others spending cashback
        @Rule(AND(AS.v << SpendingInput(data__petrol_others_spending = MATCH.data__petrol_others_spending),
                  TEST(lambda data__petrol_others_spending: data__petrol_others_spending >= petrol_others_cashback_min_spend),
                  AS.v << SpendingInput(data__petrol_others_spending = MATCH.data__petrol_others_spending),
                  TEST(lambda data__petrol_others_spending: data__petrol_others_spending * petrol_others_cashback_rate <= petrol_others_cashback_cap)))
        def petrol_others_1(self, v):
            self.cashback_petrol_others = petrol_others_spending_*petrol_others_cashback_rate
            print("petrol_others cashback within cap amount, %f earned" %(self.cashback_petrol_others))
        @Rule(AND(AS.v << SpendingInput(data__petrol_others_spending = MATCH.data__petrol_others_spending),
                  TEST(lambda data__petrol_others_spending: data__petrol_others_spending >= petrol_others_cashback_min_spend),
                  AS.v << SpendingInput(data__petrol_others_spending = MATCH.data__petrol_others_spending),
                  TEST(lambda data__petrol_others_spending: data__petrol_others_spending * petrol_others_cashback_rate > petrol_others_cashback_cap)))
        def petrol_others_2(self, v):
            self.cashback_petrol_others = petrol_others_cashback_cap
            print("petrol_others cashback exceed cap amount, %f earned" %(self.cashback_petrol_others))

        #petrol_esso spending cashback
        @Rule(AND(AS.v << SpendingInput(data__petrol_esso_spending = MATCH.data__petrol_esso_spending),
                  TEST(lambda data__petrol_esso_spending: data__petrol_esso_spending >= petrol_esso_cashback_min_spend),
                  AS.v << SpendingInput(data__petrol_esso_spending = MATCH.data__petrol_esso_spending),
                  TEST(lambda data__petrol_esso_spending: data__petrol_esso_spending * petrol_esso_cashback_rate <= petrol_esso_cashback_cap)))
        def petrol_esso_1(self, v):
            self.cashback_petrol_esso = petrol_esso_spending_*petrol_esso_cashback_rate
            print("petrol_esso cashback within cap amount, %f earned" %(self.cashback_petrol_esso))
        @Rule(AND(AS.v << SpendingInput(data__petrol_esso_spending = MATCH.data__petrol_esso_spending),
                  TEST(lambda data__petrol_esso_spending: data__petrol_esso_spending >= petrol_esso_cashback_min_spend),
                  AS.v << SpendingInput(data__petrol_esso_spending = MATCH.data__petrol_esso_spending),
                  TEST(lambda data__petrol_esso_spending: data__petrol_esso_spending * petrol_esso_cashback_rate > petrol_esso_cashback_cap)))
        def petrol_esso_2(self, v):
            self.cashback_petrol_esso = petrol_esso_cashback_cap
            print("petrol_esso cashback exceed cap amount, %f earned" %(self.cashback_petrol_esso))

        #petrol_shell spending cashback
        @Rule(AND(AS.v << SpendingInput(data__petrol_shell_spending = MATCH.data__petrol_shell_spending),
                  TEST(lambda data__petrol_shell_spending: data__petrol_shell_spending >= petrol_shell_cashback_min_spend),
                  AS.v << SpendingInput(data__petrol_shell_spending = MATCH.data__petrol_shell_spending),
                  TEST(lambda data__petrol_shell_spending: data__petrol_shell_spending * petrol_shell_cashback_rate <= petrol_shell_cashback_cap)))
        def petrol_shell_1(self, v):
            self.cashback_petrol_shell = petrol_shell_spending_*petrol_shell_cashback_rate
            print("petrol_shell cashback within cap amount, %f earned" %(self.cashback_petrol_shell))
        @Rule(AND(AS.v << SpendingInput(data__petrol_shell_spending = MATCH.data__petrol_shell_spending),
                  TEST(lambda data__petrol_shell_spending: data__petrol_shell_spending >= petrol_shell_cashback_min_spend),
                  AS.v << SpendingInput(data__petrol_shell_spending = MATCH.data__petrol_shell_spending),
                  TEST(lambda data__petrol_shell_spending: data__petrol_shell_spending * petrol_shell_cashback_rate > petrol_shell_cashback_cap)))
        def petrol_shell_2(self, v):
            self.cashback_petrol_shell = petrol_shell_cashback_cap
            print("petrol_shell cashback exceed cap amount, %f earned" %(self.cashback_petrol_shell))

        #petrol_caltex spending cashback
        @Rule(AND(AS.v << SpendingInput(data__petrol_caltex_spending = MATCH.data__petrol_caltex_spending),
                  TEST(lambda data__petrol_caltex_spending: data__petrol_caltex_spending >= petrol_caltex_cashback_min_spend),
                  AS.v << SpendingInput(data__petrol_caltex_spending = MATCH.data__petrol_caltex_spending),
                  TEST(lambda data__petrol_caltex_spending: petrol_caltex_spending_*petrol_caltex_cashback_rate <= petrol_caltex_cashback_cap)))
        def petrol_caltex_1(self, v):
            self.cashback_petrol_caltex = petrol_caltex_spending_*petrol_caltex_cashback_rate
            print("petrol_caltex cashback within cap amount, %f earned" %(self.cashback_petrol_caltex))
        @Rule(AND(AS.v << SpendingInput(data__petrol_caltex_spending = MATCH.data__petrol_caltex_spending),
                  TEST(lambda data__petrol_caltex_spending: data__petrol_caltex_spending >= petrol_caltex_cashback_min_spend),
                  AS.v << SpendingInput(data__petrol_caltex_spending = MATCH.data__petrol_caltex_spending),
                  TEST(lambda data__petrol_caltex_spending: petrol_caltex_spending_*petrol_caltex_cashback_rate > petrol_caltex_cashback_cap)))
        def petrol_caltex_2(self, v):
            self.cashback_petrol_caltex = petrol_caltex_cashback_cap
            print("petrol_caltex cashback exceed cap amount, %f earned" %(self.cashback_petrol_caltex))
            
    engine=Cashback()
    engine.reset()
    engine.declare(SpendingInput(data=dict_of_spending_amounts_info))
    engine.run()
    engine.facts

    ##check for groceries overall
    groceries_overall = engine.cashback_groceries_others + engine.cashback_groceries_ntuc + engine.cashback_groceries_sheng_siong + engine.cashback_groceries_cold_storage + engine.cashback_groceries_giant
    if groceries_overall > groceries_overall_cashback_cap:
        groceries_overall = groceries_overall_cashback_cap

    ##check for online overall
    online_overall = engine.cashback_online_others + engine.cashback_online_hotels_flights
    if online_overall > online_shopping_overall_cashback_cap:
        online_overall = online_shopping_overall_cashback_cap

    ##check for petrol overall
    petrol_overal = engine.cashback_petrol_others + engine.cashback_petrol_esso + engine.cashback_petrol_shell + engine.cashback_petrol_caltex
    if petrol_overal > petrol_overal_cashback_cap:
        petrol_overal = petrol_overal_cashback_cap

    ##check contactless overall
    cashback_overall = groceries_overall + online_overall + petrol_overal + engine.bill_cashback + engine.cashback_dining + engine.cashback_foreign + engine.cashback_retail + engine.cashback_transport
    
    contactless_cashback = 0
    if cashback_overall >= contactless_cashback_min:
        potential_contactless_cashback = total_spending * contactless_CF * contactless_cashback_rate
        if potential_contactless_cashback <= contactless_cashback_cap:
            contactless_cashback = potential_contactless_cashback
            print("contactless cashback within cap amount, %f earned" %(contactless_cashback))
        else:
            contactless_cashback = contactless_cashback_cap
            print("contactless cashback exceed cap amount, %f earned" %(contactless_cashback))

    ##cashback overall amount
    cashback_value = cashback_overall + contactless_cashback
    
    return min(cashback_value, overall_cashback_cap)


def return_reward_value(dict_of_spending_amounts_info, dict_of_preferred_credit_card_spending_rewards_info, contactless_CF, debug=False):
    
    reward_value = 0
    
    dictt = dict_of_spending_amounts_info
    row = dict_of_preferred_credit_card_spending_rewards_info
    
    if debug:
        print(dict_of_spending_amounts_info)
        print(dict_of_preferred_credit_card_spending_rewards_info)
    
    overall_points_min_spend = row['overall_points_min_spend'][0]
    total_spending = sum([dict_of_spending_amounts_info[key] for key in dict_of_spending_amounts_info.keys()])

    if total_spending < overall_points_min_spend:
        print("Did not hit the overall minimum spending, no points given")
        reward_value = 0
        return reward_value
    
    cardid = str(row['credit_card_id'][0])
    credit_card_name = str(row['credit_card_name'][0])
    overall_points_cap = row['overall_points_cap'][0]
    contactless_points_multiplier = row['contactless_points_multiplier'][0]
    contactless_points_cap = row['contactless_points_cap'][0]
    contactless_points_lot = row['contactless_points_lot'][0]
    dining_points_multiplier = row['dining_points_multiplier'][0]
    dining_points_cap = row['dining_points_cap'][0]
    dining_points_lot = row['dining_points_lot'][0]
    entertainment_points_multiplier = row['entertainment_points_multiplier'][0]
    entertainment_points_cap = row['entertainment_points_cap'][0]
    entertainment_points_lot = row['entertainment_points_lot'][0]
    foreign_points_multiplier = row['foreign_points_multiplier'][0]
    foreign_points_cap = row['foreign_points_cap'][0]
    foreign_points_lot = row['foreign_points_lot'][0]
    online_shopping_others_points_multiplier = row['online_shopping_others_points_multiplier'][0]
    online_shopping_others_points_cap = row['online_shopping_others_points_cap'][0]
    online_shopping_others_points_lot = row['online_shopping_others_points_lot'][0]
    online_shopping_hotels_and_flight_points_multiplier = row['online_shopping_hotels_and_flight_points_multiplier'][0]
    online_shopping_hotels_and_flights_points_cap = row['online_shopping_hotels_and_flights_points_cap'][0]
    online_shopping_hotels_and_flights_points_lot = row['online_shopping_hotels_and_flights_points_lot'][0]
    retail_shopping_points_multiplier = row['retail_shopping_points_multiplier'][0]
    retail_shopping_points_cap = row['retail_shopping_points_cap'][0]
    retail_shopping_points_lot = row['retail_shopping_points_lot'][0]
    points_to_miles_conversion = row['points_to_miles_conversion'][0]
    
    bill_spending_ = dictt['bill_spending']
    dining_spending_ = dictt['dining_spending']
    entertainment_spending_ = dictt['entertainment_spending']
    foreign_spending_ = dictt['foreign_spending']
    retail_shopping_spending_ = dictt['retail_shopping_spending']
    transport_spending_ = dictt['transport_spending']
    groceries_others_spending_ = dictt['groceries_others_spending']
    groceries_ntuc_spending_ = dictt['groceries_ntuc_spending']
    groceries_sheng_siong_spending_ = dictt['groceries_sheng_siong_spending']
    groceries_cold_storage_spending_ = dictt['groceries_cold_storage_spending']
    groceries_giant_spending_ = dictt['groceries_giant_spending']
    online_shopping_others_spending_ = dictt['online_shopping_others_spending']
    online_shopping_hotels_and_flight_spending_ = dictt['online_shopping_hotels_and_flight_spending']
    petrol_others_spending_ = dictt['petrol_others_spending']
    petrol_esso_spending_ = dictt['petrol_esso_spending']
    petrol_caltex_spending_ = dictt['petrol_caltex_spending']
    petrol_shell_spending_ = dictt['petrol_shell_spending']
    
    class SpendingInput(Fact):  
        bill_spending = Field(float)
        dining_spending = Field(float)
        foreign_spending = Field(float)
        retail_shopping_spending = Field(float)
        transport_spending = Field(float)
        groceries_others_spending = Field(int)
        groceries_ntuc_spending = Field(int)
        groceries_sheng_siong_spending = Field(int)
        groceries_cold_storage_spending = Field(int)
        groceries_giant_spending = Field(int)
        online_shopping_others_spending = Field(int)
        online_shopping_hotels_and_flight_spending = Field(int)
        petrol_others_spending = Field(int)
        petrol_esso_spending = Field(int)
        petrol_caltex_spending = Field(int)
        petrol_shell_spending = Field(int)
        pass 

    class Reward(KnowledgeEngine):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.reward_points = 0
            self.reward_dining = 0

        # Reward for dining
        @Rule(AS.v << SpendingInput(data__dining_spending = MATCH.data__dining_spending),
              TEST(lambda data__dining_spending: data__dining_spending >= 0))
        def reward_dining(self):
            self.reward_dining = dining_spending_ // dining_points_lot * dining_points_multiplier
            print("%f points were earned from dining" %(self.reward_dining))
    
        # Reward for entertainment
        @Rule(AS.v << SpendingInput(data__entertainment_spending = MATCH.data__entertainment_spending),
              TEST(lambda data__entertainment_spending: data__entertainment_spending >= 0))
        def reward_entertainment(self):
            self.reward_entertainment = entertainment_spending_ // entertainment_points_lot * entertainment_points_multiplier
            print("%f points were earned from entertainment" %(self.reward_entertainment))
            
        # Reward for foreign spending
        @Rule(AS.v << SpendingInput(data__foreign_spending = MATCH.data__foreign_spending),
              TEST(lambda data__foreign_spending: data__foreign_spending >= 0))
        def reward_foreign(self):
            self.reward_foreign = foreign_spending_ // foreign_points_lot * foreign_points_multiplier
            print("%f points were earned from foreign spending" %(self.reward_foreign))
        
        # Reward for online_shopping_others
        @Rule(AS.v << SpendingInput(data__online_shopping_others_spending = MATCH.data__online_shopping_others_spending),
              TEST(lambda data__online_shopping_others_spending: data__online_shopping_others_spending >= 0))
        def reward_online_shopping_others(self):
            self.reward_online_shopping_others = online_shopping_others_spending_ // online_shopping_others_points_lot * online_shopping_others_points_multiplier
            print("%f points were earned from online_shopping_others" %(self.reward_online_shopping_others))
            
        # Reward for online_shopping_hotels_and_flight
        @Rule(AS.v << SpendingInput(data__online_shopping_hotels_and_flight_spending = MATCH.data__online_shopping_hotels_and_flight_spending),
              TEST(lambda data__online_shopping_hotels_and_flight_spending: data__online_shopping_hotels_and_flight_spending >= 0))
        def reward_online_shopping_hotels_and_flight(self):
            self.reward_online_shopping_hotels_and_flight = online_shopping_hotels_and_flight_spending_ // online_shopping_hotels_and_flights_points_lot * online_shopping_hotels_and_flight_points_multiplier
            print("%f points were earned from online_shopping_hotels_and_flight" %(self.reward_online_shopping_hotels_and_flight))
            
        # Reward for retail_spending
        @Rule(AS.v << SpendingInput(data__retail_shopping_spending = MATCH.data__retail_shopping_spending),
              TEST(lambda data__retail_shopping_spending: data__retail_shopping_spending >= 0))
        def reward_retail(self, v):
            self.reward_retail = retail_shopping_spending_ // retail_shopping_points_lot * retail_shopping_points_multiplier
            print("%f points were earned from retail_spending" %(self.reward_retail))
            
    engine=Reward()
    engine.reset()
    engine.declare(SpendingInput(data=dict_of_spending_amounts_info))
    engine.run()
    engine.facts
    
    reward_value = engine.reward_dining \
                    + engine.reward_entertainment \
                    + engine.reward_foreign \
                    + engine.reward_online_shopping_others \
                    + engine.reward_online_shopping_hotels_and_flight \
                    + engine.reward_retail
    
    ##check contactless overall
    reward_contactless = 0
    potential_reward_contactless = total_spending//contactless_points_lot*contactless_CF
    if potential_reward_contactless <= contactless_points_cap:
        reward_contactless = potential_reward_contactless
    else:
        reward_contactless = contactless_points_cap
    print("%f points were earned from contactless spending" %(reward_contactless))

    reward_value = reward_value + reward_contactless
    
    return min(overall_points_cap, reward_value)

def fuzzy_logic_convert_points_to_cashback_value(reward_value, bank_name):
    if bank_name == 'dbs':
        cashback_equivalent = DBS_points_to_cashback(reward_value)
    elif bank_name == 'citibank':
        cashback_equivalent = citibank_points_to_cashback(reward_value)
    elif bank_name == 'standard chartered':
        cashback_equivalent = standardchartered_points_to_cashback(reward_value)
    elif bank_name == 'uob':
        cashback_equivalent = uob_points_to_cashback(reward_value)
    elif bank_name == 'maybank':
        cashback_equivalent = maybank_points_to_cashback(reward_value)
    elif bank_name == 'hsbc':
        cashback_equivalent = HSBC_points_to_cashback(reward_value)
    elif bank_name == 'ocbc':
        cashback_equivalent = ocbc_points_to_cashback(reward_value)
    else:
        print("NONE OF THEM")
        cashback_equivalent = -1
    return cashback_equivalent

def fuzzy_logic_convert_miles_to_cashback_value(reward_value, points_to_miles_conversion, bank_name):
    if bank_name == 'dbs':
        cashback_equivalent = DBS_miles_to_cashback(reward_value*points_to_miles_conversion)
    elif bank_name == 'citibank':
        cashback_equivalent = citibank_miles_to_cashback(reward_value*points_to_miles_conversion)
    elif bank_name == 'standard chartered':
        cashback_equivalent = standardchartered_miles_to_cashback(reward_value*points_to_miles_conversion)
    elif bank_name == 'uob':
        cashback_equivalent = uob_miles_to_cashback(reward_value*points_to_miles_conversion)
    elif bank_name == 'maybank':
        cashback_equivalent = maybank_miles_to_cashback(reward_value*points_to_miles_conversion)
    elif bank_name == 'hsbc':
        cashback_equivalent = HSBC_miles_to_cashback(reward_value*points_to_miles_conversion)
    elif bank_name == 'ocbc':
        cashback_equivalent = ocbc_miles_to_cashback(reward_value*points_to_miles_conversion)
    else:
        print("NONE OF THEM")
        cashback_equivalent = -1
    return cashback_equivalent

def return_compare_by_preference(points_to_miles_conversion, points_split_ratio, cashback_value, reward_value, bank_name, dict_of_cashback_points_miles_preference_info, debug=False):
    preferred_rewards_type = dict_of_cashback_points_miles_preference_info['preferred_rewards_type']
        
    ## Calculate for only ONE preference: cashback/ points/ miles ##
    if set(preferred_rewards_type) == set(['cashback']):
        if debug: print("Cashback Preference, %f" %(cashback_value))
        return cashback_value
    elif set(preferred_rewards_type) == set(['points']):
        if debug: print("Points Preference, %f" %(reward_value))
        return reward_value
    elif set(preferred_rewards_type) == set(['miles']):
        if debug: print("Miles Preference, %f" %(reward_value*points_to_miles_conversion))
        return reward_value*points_to_miles_conversion
    points_cashback_equivalent = fuzzy_logic_convert_points_to_cashback_value(reward_value, bank_name)
    miles_cashback_equivalent =  fuzzy_logic_convert_miles_to_cashback_value(reward_value*points_to_miles_conversion, points_to_miles_conversion, bank_name)

    ## Calculate for TWO preference: any 2 out of cashback/ points/ miles ##
    if set(preferred_rewards_type) == set(['cashback', 'points']):
        total_cash_val_equivalent = cashback_value + points_cashback_equivalent
        if debug: print("Cashback & Points Preference, %f" %(total_cash_val_equivalent))
        return total_cash_val_equivalent
    elif set(preferred_rewards_type) == set(['cashback', 'miles']):
        total_cash_val_equivalent = cashback_value + points_split_ratio*miles_cashback_equivalent
        if debug: print("Cashback & Miles Preference, %f" %(total_cash_val_equivalent))
        return total_cash_val_equivalent
    elif set(preferred_rewards_type) == set(['points', 'miles']):
        total_cash_val_equivalent = points_split_ratio*points_cashback_equivalent + (1 - points_split_ratio)*miles_cashback_equivalent
        if debug: print("Points & Miles Preference, %f" %(total_cash_val_equivalent))
        return total_cash_val_equivalent

    ## Calculate for THREE preference: all three of cashback/ points/ miles ##
    if set(preferred_rewards_type) == set(['cashback', 'points', 'miles']):
        total_cash_val_equivalent = cashback_value + points_split_ratio*points_cashback_equivalent + (1 - points_split_ratio)*miles_cashback_equivalent
        if debug: print("Cashback & Points & Miles Preference, %f" %(total_cash_val_equivalent))
        return total_cash_val_equivalent

def return_best_credit_card(dict_of_spending_amounts_info, dict_of_credit_card_spending_rewards_info, dict_of_cashback_points_miles_preference_info, debug=False):

    points_split_ratio = 0.5
    contactless_CF=0.75

    ## Get all the pertinent info from all the credit cards in this set ##
    credit_card_pertinent_info = []
    for row in dict_of_credit_card_spending_rewards_info:
        cardid = str(row['credit_card_id'][0])
        credit_card_name = str(row['credit_card_name'][0])
        official_link = str(row['official_link'][0])
        points_to_miles_conversion = row['points_to_miles_conversion'][0]
        annual_fee = row['annual_fee'][0]
        bank_name = row['bank_name'][0]
        card_type = row['card_type']
        print(card_type)
        print("\n\n")    
    
        cashback_value = return_cashback_value(dict_of_spending_amounts_info, row, contactless_CF, debug)
        reward_value =  return_reward_value(dict_of_spending_amounts_info, row, contactless_CF, debug)

        total_cash_val_equivalent = return_compare_by_preference(points_to_miles_conversion, points_split_ratio, cashback_value, reward_value, bank_name, dict_of_cashback_points_miles_preference_info, debug)

        if debug:
            print("cardid, credit_card_name, official_link, points_to_miles_conversion, points_split_ratio, cashback_value, reward_value, total_cash_val_equivalent")
            print(credit_card_name, official_link, points_to_miles_conversion, points_split_ratio, cashback_value, reward_value, total_cash_val_equivalent)
        
        credit_card_name = credit_card_name
        credit_card_official_link = official_link
        cashback_amount = 0
        points_amount = 0
        miles_amount = 0
        annual_fee = annual_fee
        total_cash_val_equivalent = total_cash_val_equivalent
        
        ## Calculate for only ONE preference: cashback/ points/ miles ##
        if set(card_type) == set(['cashback']):
            cashback_amount = cashback_value
        elif set(card_type) == set(['points']):
            if debug: print("Points Preference, %f" %(reward_value))
            points_amount = reward_value
        elif set(card_type) == set(['miles']):
            if debug: print("Miles Preference, %f" %(reward_value*points_to_miles_conversion))
            miles_amount = reward_value*points_to_miles_conversion

        ## Calculate for TWO preference: any 2 out of cashback/ points/ miles ##
        if set(card_type) == set(['cashback', 'points']):
            cashback_amount = cashback_value
            points_amount = reward_value
        elif set(card_type) == set(['cashback', 'miles']):
            cashback_amount = cashback_value
            miles_amount = reward_value
        elif set(card_type) == set(['points', 'miles']):
            points_amount = points_split_ratio*reward_value 
            miles_amount = (1 - points_split_ratio)*reward_value

        ## Calculate for THREE preference: all three of cashback/ points/ miles ##
        if set(card_type) == set(['cashback', 'points', 'miles']):
            cashback_amount = cashback_value
            points_amount = points_split_ratio*reward_value 
            miles_amount = (1 - points_split_ratio)*reward_value
        
        credit_card_pertinent_info.append([credit_card_name, official_link, cashback_amount, points_amount, miles_amount, annual_fee, total_cash_val_equivalent])
    
    ## Sort the best credit card in this set and return it in values ##
    best_total_cash_val_equivalent = max([x[-1] for x in credit_card_pertinent_info])
    best_credit_cards = [x for x in credit_card_pertinent_info if x[-1] == best_total_cash_val_equivalent]
    if debug:
        print(credit_card_pertinent_info)
        print("The best Cash Value equivalent is %f" %(best_total_cash_val_equivalent))
        print("The best Credit Cards are %r" %(best_credit_cards))
    if len(best_credit_cards) == 1: # If there is only one best Credit Card
        return best_credit_cards[0]
    return best_credit_cards[0]
