import pandas as pd
from pandasai import SmartDataframe

from chains.utils import get_llm

def get_df():
    df = pd.DataFrame({
        "expense_type": ["Hotel","Meals","Transportation - Taxi","Transportation - Air","Transportation - Train"],
        "invoice_id": ["1","2","3","4","5"],
        "invoice_date":["2023-04-02","2023-04-03","2023-04-04","2023-04-06","2023-04-06"],
        "vendor": ["vender1","vender2","vender3","vender4","vender5"],
        "customer":["customer1","customer1","customer1","customer1","customer1"],
        "city":["西安","成都","上海","上海","北京"],
        "currency":["CNY","CNY","CNY","CNY","CNY"],
        "amount": [100,200,300,2130,670]
    })
    return df




def get_df_chatbot(df):
    df_bot = SmartDataframe(df, config={
        "llm": get_llm(),
        "custom_whitelisted_dependencies": [],
        "conversational": True,
        "verbose": True
    })
    return df_bot