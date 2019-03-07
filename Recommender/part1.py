    
debug=True

eligible_card_ids = {'eligible_credit_card_ids':[]}

for row in credit_card_eligibility_info:
    cardid = str(row['credit_card_id'][0])
    credit_card_name = str(row['credit_card_name'][0])
    age__min = row['age_min'][0]
    age__max = row['age_max'][0]
    gender__req = row['gender_req'][0]
    annual_income_singaporean_min = row['annual_income_singaporean_min'][0]
    annual_income_pr_min = row['annual_income_pr_min'][0]
    annual_income_foreigner_min = row['annual_income_foreigner_min'][0]
    if debug:
        print("Applicant Info:", personal_info)
        print("Card Info: ID is %s, Name is %s, age_min is %f, age_max is %f, gender is %s, annual_income_singaporean_min is %f, annual_income_pr_min is %f, annual_income_foreigner_min is %f"
              %(cardid, credit_card_name, age__min, age__max, gender__req, annual_income_singaporean_min, annual_income_pr_min, annual_income_foreigner_min))
    engine = Eligibility()
    engine.reset()
    engine.declare(Person(data=personal_info))
    engine.run()
    engine.facts
    if debug:
        print(engine.eligible_status)
        print("\n")
    if engine.eligible_status:
        eligible_card_ids['eligible_credit_card_ids'].append(cardid)
        
#     return dict_of_eligible_card_ids
        
