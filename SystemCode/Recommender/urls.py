from django.urls import path

from . import views

app_name = 'Recommender'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('eligibility/', views.eligibility, name='eligibility'),
    path('preferences/', views.preferences, name='preferences'),
    path('spending_checkbox/', views.spending_checkbox, name='spending_checkbox'),
    path('spending_amount/', views.spending_amount, name='spending_amount'),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('no_recommendation/', views.no_recommendation, name='no_recommendation'),
    path('test/', views.test, name='test')
    #path('spending/', views.spending, name='spending'),
    #path('bank/', views.bank, name='bank'),
    #path('end/', views.end, name='end')
]
