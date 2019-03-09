import pandas as pd
from .models import CreditCards


filepath = "Recommender_creditcards.csv"

def FP_Add(f):
    upload = False
    df_fp = pd.read_csv(f)
    count = 0
    
    dict_fp = df_fp.to_dict('records')
    obj = CreditCards(**dict_fp)
    obj.save()

FP_Add(filepath)
