from random import choice
from pyknow import *

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
            # Credit Card's Bank is within preferred list AND within paymnet network
            @Rule(AND(AS.v << PreferenceInput(data__preferred_bank = MATCH.data__preferred_bank),
                      TEST(lambda data__preferred_bank: bank_name in data__preferred_bank or bank_name == data__preferred_bank),
                      AS.v << PreferenceInput(data__preferred_card_type = MATCH.data__preferred_card_type),
                      TEST(lambda data__preferred_card_type: set(data__preferred_card_type).issubset(set(payment_networks)) or data__preferred_card_type in payment_networks))
                 )
            def bank_within_preferred_and_in_payment_network(self, v):
                print("Cardid %s, %s is a preferred bank and has the %s payment network desired" %(cardid, bank_name, ' '.join(payment_networks)))
                self.prefered = True
                self.halt()
            # Credit Card's Bank is NOT within preferred list
            @Rule(AS.v << PreferenceInput(data__preferred_bank = MATCH.data__preferred_bank),
                  TEST(lambda data__preferred_bank: bank_name not in data__preferred_bank))
            def bank_not_within_preferred(self, v):
                print("Cardid %s, %s is not a preferred bank" %(cardid, bank_name))
                self.prefered = False
                self.halt()
            # Credit Card's Bank is NOT within payment network
            @Rule(AS.v << PreferenceInput(data__preferred_card_type = MATCH.data__preferred_card_type),
                  TEST(lambda data__preferred_card_type: set(payment_networks).issubset(set(data__preferred_card_type)) == False))
            def credit_card_not_in_payment_network(self, v):
                print("Cardid %s, preferred payment network not within %s" %(cardid,' '.join(payment_networks)))
                self.prefered = False
                self.halt()
                
        cardid = str(row['credit_card_id'][0])
        credit_card_name = str(row['credit_card_name'][0])
        bank_name = row['bank_name'][0].lower()
        payment_networks = row['payment_networks']
        
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

