from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .models import CreditCards

def index(request):
    return render(request, 'Recommender/index.html')

def process(request):
    print("abc")
    print(request.POST)
    print(request.POST['annual_income'])
    print(request.POST['age'])
    print(request.POST['citizenship'])
    print(request.POST['total_spending_amount'])

    def get_queryset(self):
        """Return all the credit cards"""
        return CreditCard.objects.all()

    return render(request, 'Recommender/process.html')
