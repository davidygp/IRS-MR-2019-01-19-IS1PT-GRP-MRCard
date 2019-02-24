from django.db import models

# Create your models here.

class Person(models.Model):
    age = models.PositiveSmallIntegerField()
    citizenship_choices = [(1, 'Singaporean'), (2, 'PR'), (3,'Foreigner')]
    citizenship = models.CharField(max_length=12, choices=citizenship_choices)
    annual_income = models.PositiveIntegerField()
    total_spending_amount = models.PositiveIntegerField()

class CreditCards(models.Model):
    annual_income_singaporean_min = models.PositiveIntegerField()
    annual_income_pr_min = models.PositiveIntegerField()
    annual_income_foreigner_min = models.PositiveIntegerField()
    age_min = models.PositiveSmallIntegerField()
    age_max = models.PositiveSmallIntegerField()
    total_spending_amount_min = models.PositiveIntegerField()
    eligible = models.BooleanField(default=None) 
