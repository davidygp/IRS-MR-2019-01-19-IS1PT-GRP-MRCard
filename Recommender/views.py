from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import CreditCards
from .config import *
from .rules import return_eligibile_credit_card_ids

debug = True

# Functions used below
def retrieve_data_or_set_to_default(input_dict, default_dict):
    '''
    Given a dictionary of data (e.g. from the HTML POST request) and a default dictionary.
    For fields that are not in the dictionary of data but in the default dictionary, assign the new fields as the default.
    '''
    output_dict = {}
    for key in default_dict.keys():
        try:
            val = input_dict[key] # Check if key exists
            if len(val) == 0: # If it is empty
                output_dict[key] = default_dict[key]
            else:
                output_dict[key] = convert_string_to_int_or_float(val) 
        except:
            output_dict[key] = default_dict[key] 
    return output_dict

def convert_string_to_int_or_float(string):
    '''
    Converts the string which can contain a string, int or float, into a string, int or float
    (I'm sure there's a better way to do this.)
    '''
    try:
        output = int(string)    
        return output
    except:
        try:
            output = float(string)
            return output
        except:
            return string
    return string
    
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
            item = query_set[i][key]
            try:
                processed_item = [convert_string_to_int_or_float(x) for x in item.split(',')]
            except:
                processed_item = [convert_string_to_int_or_float(item)]
            sub_dictionary[key] = processed_item
        subset_of_query_set.append(sub_dictionary)
    return subset_of_query_set

def map_POST_to_session(request):
    key_list = list(request.POST.keys())
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
    
    ### Process Data to determine eligibility ###
    ## Retrieve Personal eligibility info ##
    personal_info = retrieve_data_or_set_to_default(request.POST, personal_info_default_dict)
    ## Retrieve Credit Card eligibility related info ##
    all_credit_card_info = CreditCards.objects.values()
    credit_card_eligibility_info = retrieve_subset_out_of_query_set(all_credit_card_info, credit_card_eligibility_list)
    #print(credit_card_eligibility_info)
    if debug:
        print("---- Personal Info ----")
        print(personal_info)
        print("---- Credit Card Eligibility Info ----")
        print(credit_card_eligibility_info)
    ## Calculate the eligible Credit Cards here ##
    eligible_credit_card_ids = return_eligibile_credit_card_ids(personal_info, credit_card_eligibility_info) 
    if debug:
        print("---- Eligible Credit Cards ----")
        print(eligible_credit_card_ids)
    request.session['eligible_credit_card_ids'] = eligible_credit_card_ids['eligible_credit_card_ids']
    if len(eligible_credit_card_ids['eligible_credit_card_ids']) == 0:
        return render(request, 'Recommender/no_recommendation.html')
    else:
        return render(request, 'Recommender/preferences.html')


def spending_checkbox(request):
    # This is the third html page
    map_POST_to_session(request) # Save the POST data into the session
    print(request.POST)
    ## Retrieve Prefence info ##
    preference_info = retrieve_data_or_set_to_default(request.POST, preference_info_default_dict)
    ## Retrieve Credit Card preference related info ##
    all_credit_card_info = CreditCards.objects.values()
    credit_card_preference_info = retrieve_subset_out_of_query_set(all_credit_card_info, credit_card_preference_list)
    if debug:
        print("---- Preference Info ----")
        print(preference_info)
        print("---- Credit Card Preference Info ----")
        print(credit_card_preference_info)
    return render(request, 'Recommender/spending_checkbox.html')


def spending_amount(request):
    # This is the fourth html page
    map_POST_to_session(request) # Save the POST data into the session

    ## Retrieve Spending Checkbox info ##
    spending_checkbox_info = retrieve_data_or_set_to_default(request.POST, spending_checkbox_default_dict)
    print(spending_checkbox_info)
    ## Assign what data to show in the spending_amount.html ##
    #TODO# (LD/YZ)
    eligible_spending = {'eligible_spending':['bill','dining','groceries','transport']} # Get this from LD/YZ
    context = {
    'eligible_spending':eligible_spending['eligible_spending']
    }
    return render(request, 'Recommender/spending_amount.html', context)


def recommendation(request):
    # This is the last html page
    map_POST_to_session(request) # Save the POST data into the session
    
    ## Retrieve Preference info & process it ##
    #TODO# (DY)
    #preprocessed_preference_info = request.session[''] # Do after JH confirms format
    processed_preference_info = {'preferred_bank_rank':['dbs','ocbc','uob'],
                                    'preferred_card_type':['visa','mastercard'],
                                    'cashback_preference_rank':1,
                                    'miles_preference_rank':2,
                                    'points_preference_rank':3} # To-be changed #
    ## Retrieve Spending Amounts info ##
    spending_amounts_info = retrieve_data_or_set_to_default(request.POST, spending_amounts_default_dict)
    print(spending_amounts_info)
    ## Retrieve Credit Card cashback/miles/points info ##
    all_credit_card_info = CreditCards.objects.values()
    credit_card_spending_info = retrieve_subset_out_of_query_set(all_credit_card_info, credit_card_spending_list)
    #print(credit_card_spending_info)
    ## Calculate the Ideal & Preferred Credit Card ##
    #TODO# (LD/YZ)
    Recommendation = {'ideal_credit_card':'placeholder ideal credit card',
                        'preferred_credit_card':'placeholder preferred credit card',
                        'ideal_cashback_amount':1234,
                        'ideal_miles_amount':5678,
                        'ideal_points_amount':9012,
                        'preferred_cashback_amount':1234,
                        'preferred_miles_amount':5678,
                        'preferred_points_amount':9012} # Get from LD/YZ

    context = {
    'ideal_credit_card':Recommendation['ideal_credit_card'],
    'preferred_credit_card':Recommendation['preferred_credit_card'],
    'ideal_cashback_amount':Recommendation['ideal_cashback_amount'],
    'ideal_miles_amount':Recommendation['ideal_miles_amount'],
    'ideal_points_amount':Recommendation['ideal_points_amount'],
    'preferred_cashback_amount':Recommendation['preferred_cashback_amount'],
    'preferred_miles_amount':Recommendation['preferred_miles_amount'],
    'preferred_points_amount':Recommendation['preferred_points_amount']
    }
    return render(request, 'Recommender/recommendation.html', context)


def no_recommendation(requests):
    # This is also the last html page (if there are no eligible Credit Cards)
    return render(request, 'Recommender/no_recommendation.html')

