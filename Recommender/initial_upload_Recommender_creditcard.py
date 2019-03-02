from django.db import models
from .models import CreditCards
import pandas as pd

settings.configure()

filepath = "Recommender_creditcard.csv"

print("Got here!")
credit_card_info = pd.read_csv(filepath, header=0, encoding='utf-8')
# print(credit_card_info[credit_card_info['multiple_levels'] == True]['transport_cashback_min_spend'])

# This only works assuming the CSV file is in the same column format as the Class #
for i in range(credit_card_info.shape[0]):
    print(i)
#p = CreditCard(
#                )


## THIS DOESN'T WORK ##
