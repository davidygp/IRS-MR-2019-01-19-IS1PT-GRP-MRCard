from django.db import models

# Create your models here.

class Person(models.Model):
    age = models.PositiveSmallIntegerField()
    citizenship_choices = ['Singaporean', 'PR', 'Foreigner']
    citizenship = models.CharField(choices=citizenship_choices))
    annual_income = models.PositiveIntegerField()
    total_spending_amount = models.PositiveIntegerField()

class CreditCards(models.Model):
    annual_income_singaporean_min = PositiveSmallIntegerField()
    annual_income_pr_min = PositiveSmallIntegerField()
    annual_income_foreigner_min = PositiveSmallIntegerField()
    age_min = PositiveSmallIntegerField()
    age_max = PositiveSmallIntegerField()
    total_spending_amount_min = PositiveIntegerField() 
