import pandas as pd
import numpy as np
from datetime import datetime
import itertools
# JSON API
import requests
import json

def get_items_data():
    base_url = 'https://python.zach.lol'
    response = requests.get('https://python.zach.lol/api/v1/items')
    data = response.json()
    df1 = pd.DataFrame(data['payload']['items'])
    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()
    df1 = pd.concat([df, pd.DataFrame(data['payload']['items'])]).reset_index()
    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()
    df1 = pd.concat([df, pd.DataFrame(data['payload']['items'])]).reset_index()
    df1.to_csv('items.csv')
    return df1

def get_stores_data():
    base_url = 'https://python.zach.lol'
    response = requests.get('https://python.zach.lol/api/v1/stores')
    data = response.json()
    df2 = pd.DataFrame(data['payload']['stores'])
    df2.to_csv('stores.csv')
    return df2

def get_sales_data():
    base_url = 'https://python.zach.lol'
    response = requests.get(base_url + '/api/v1/sales')
    data = response.json()
    sales = data['payload']['sales']
    while data['payload']['page'] < 184:
        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        sales += data['payload']['sales']
        if data['payload']['next_page'] == None:
            break
    df = pd.DataFrame(sales)
    df.to_csv('sales.csv')
    return df

def merge_dataframes():
    df = pd.read_csv('sales.csv')
    df1 = pd.read_csv('items.csv')
    df2 = pd.read_csv('stores.csv')
    df = df.rename(index=str, columns={"store": "store_id"})
    df_store_sales = df.merge(df2, left_on='store_id', right_on='store_id')
    df_store_sales = df_store_sales.rename(index=str, columns={'item':'item_id'})
    df_final = df_store_sales.merge(df1, left_on='item_id', right_on='item_id')
    df_final = df_final.drop(['Unnamed: 0_x','Unnamed: 0_y','Unnamed: 0','level_0','index'],axis=1)
    df.to_csv('df_final')
    return df_final

