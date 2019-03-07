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
                TEST(lambda data__gender: (data__gender == 'male') & (gender__req == 'F')))
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
