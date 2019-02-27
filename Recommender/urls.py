from django.urls import path

from . import views

app_name = 'Recommender'
urlpatterns = [
    path('', views.eligibility, name='eligibility'),
    path('spending/', views.spending, name='spending'),
    path('bank/', views.bank, name='bank'),
    path('end/', views.end, name='end')
]
