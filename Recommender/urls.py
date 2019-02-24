from django.urls import path

from . import views

app_name = 'Recommender'
urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process, name='process')
]
