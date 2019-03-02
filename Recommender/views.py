from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import CreditCards

def map_POST_to_session(request):
    key_list = list(request.POST.keys())
    print(key_list)
    key_list.remove('csrfmiddlewaretoken')
    for key in key_list:
        request.session[key] = request.POST[key] 
    
def eligibility(request):
    request.session['eligible_credit_card'] = 'eligible card'
    return render(request, 'Recommender/eligibility.html')

def preferences(request):
    return render(request, 'Recommender/preferences.html')

def spending_checkbox(request):
    return render(request, 'Recommender/spending_checkbox.html')

def spending_amount(request):
    return render(request, 'Recommender/spending_amount.html')

def spending(request):
    map_POST_to_session(request)
    request.session['selected_credit_card'] = 'selected credit card'
    def get_queryset(self):
        """Return all the credit cards"""
        return CreditCard.objects.all()
    return render(request, 'Recommender/spending.html')

def bank(request):
    map_POST_to_session(request)
    print(request.session['age'])
    request.session['selected_bank'] = 'selected bank'
    return render(request, 'Recommender/bank.html')

def end(request):
    print("SESSION 3", request.session)
    print("AGE", request.session['age'])
    print("BILL SPENDING", request.session['bill_spending'])
    context = {'selected_credit_card': request.session['selected_credit_card']}
    return render(request, 'Recommender/end.html', context)
