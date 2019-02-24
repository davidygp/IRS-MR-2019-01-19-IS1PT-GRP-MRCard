from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, 'Recommender/index.html')

def process(request):
    print("abc")
    print(request)
