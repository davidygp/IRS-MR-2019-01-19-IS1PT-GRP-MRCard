from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import CreditCards

# Some configurations, maybe it shouldn't be here, but meh
credit_card_eligibility_list = ['credit_card_id',
'credit_card_name',
'multiple_levels',
'bank_name',
'payment_networks',
'age_min',
'age_max',
'gender_req',
'annual_income_singaporean_min',
'annual_income_pr_min',
'annual_income_foreigner_min']


# Functions used below
def retrieve_subset_out_of_query_set(query_set, list_of_keys):
    '''
    Takes a QuerySet object from django in the format [{}], i.e. list of dictionaries &
    a list of keys that forms a subset of the keys of the dictionaries

    Returns a list of dictionaries of the format [{}], that is a smaller subset
    '''
    subset_of_query_set = []
    for i in range(len(query_set)):
        sub_dictionary = {}
        for key in list_of_keys:
            sub_dictionary[key] = query_set[i][key]
        subset_of_query_set.append(sub_dictionary)
    return subset_of_query_set

def map_POST_to_session(request):
    key_list = list(request.POST.keys())
    print(key_list)
    key_list.remove('csrfmiddlewaretoken')
    for key in key_list:
        request.session[key] = request.POST[key] 


# Views Proper #
def eligibility(request):
    # This is the first html page
    return render(request, 'Recommender/eligibility.html')

def test(request):
    # This is the first html page
    return render(request, 'Recommender/test.html')

def preferences(request):
    # This is the second html page
    map_POST_to_session(request) # Save the POST data into the session
    
    ## Retrieve Personal eligibility info ##
    personal_info=request.POST
    ## Retrieve Credit Card eligibility info ##
    all_credit_card_info = CreditCards.objects.values()
    #print(all_credit_card_info) 
    credit_card_eligibility_info = retrieve_subset_out_of_query_set(all_credit_card_info, credit_card_eligibility_list)
    #print(credit_card_eligibility_info)
    ## Calculate the eligible Credit Cards here ##
    #TODO# (LD/YZ)
    eligible_credit_card_ids = {'eligible_credit_card_ids':[1,2,3]} # Get this from LD/YZ
    if len(eligible_credit_card_ids['eligible_credit_card_ids']) == 0:
        return render(request, 'Recommender/no_recommendation.html')
    else:
        return render(request, 'Recommender/preferences.html')


def spending_checkbox(request):
    # This is the third html page
    map_POST_to_session(request) # Save the POST data into the session
    return render(request, 'Recommender/spending_checkbox.html')


def spending_amount(request):
    # This is the fourth html page
    map_POST_to_session(request) # Save the POST data into the session

    ## Retrieve Spending Checkbox info ##
    spending_checkbox_info=request.POST
    ## Assign what data to show in the spending_amount.html ##
    #TODO# (LD/YZ)
    eligible_spending = {'eligible_spending':['bill','dining','retail','transport']} # Get this from LD/YZ
    context = {
    'eligible_spending':eligible_spending['eligible_spending']
    }
    return render(request, 'Recommender/spending_amount.html', context)


def recommendation(requests):
    # This is the last html page
    map_POST_to_session(request) # Save the POST data into the session
    
    ## Retrieve Preference info & process it ##
    #TODO# (DY)
    preprocessed_preference_info = request.session[''] # Do after JH confirms format
    processed_preference_info = {'preferred_bank_rank':['dbs','ocbc','uob'],
                                    'preferred_card_type':['visa','mastercard'],
                                    'cashback_preference_rank':1,
                                    'miles_preference_rank':2,
                                    'points_preference_rank':3} # To-be changed #
    ## Retrieve Spending Amounts info ##
    spending_amounts_info=request.POST
    ## Retrieve Credit Card cashback/miles/points info ##
    #TODO# (DY) 
    credit_card_spending_info = {}
    ## Calculate the Ideal & Preferred Credit Card ##
    #TODO# (LD/YZ)
    Recommendation = {'ideal_credit_card':'placeholder ideal credit card',
                        'preferred_credit_card':'placeholder preferred credit card',
                        'cashback_amount':1234,
                        'miles_amount':5678,
                        'points_amount':9012} # Get from LD/YZ
    context = {
    'ideal_credit_card':Recommendation['ideal_credit_card'],
    'preferred_credit_card':Recommendation['preferred_credit_card'],
    'cashback_amount':Recommendation['cashback_amount'],
    'miles_amount':Recommendation['miles_amount'],
    'points_amount':Recommendation['points_amount']
    }
    return render(request, 'Recommender/recommendation.html', context)


def no_recommendation(requests):
    # This is also the last html page (if there are no eligible Credit Cards)
    return render(request, 'Recommender/no_recommendation.html')

#def spending(request):
#    map_POST_to_session(request)
#    request.session['selected_credit_card'] = 'selected credit card'
#    def get_queryset(self):
#        """Return all the credit cards"""
#        return CreditCard.objects.all()
#    return render(request, 'Recommender/spending.html')

#def bank(request):
#    map_POST_to_session(request)
#    print(request.session['age'])
#    request.session['selected_bank'] = 'selected bank'
#    return render(request, 'Recommender/bank.html')

#def end(request):
#    print("SESSION 3", request.session)
#    print("AGE", request.session['age'])
#    print("BILL SPENDING", request.session['bill_spending'])
#    context = {'selected_credit_card': request.session['selected_credit_card']}
#    return render(request, 'Recommender/end.html', context)
