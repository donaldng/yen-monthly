import pandas as pd, requests, datetime, json, numpy as np, os
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import time

def fetchData():  

    yf.pdr_override()
    
    df = pdr.get_data_yahoo("BTC-USD", "2009-01-01", "2019-01-01")

    df["Date"] = df.index

    df.rename(columns={'Close': 'close'}, inplace=True)
    df.rename(columns={'Date': 'date'}, inplace=True)
    
    df.index = pd.to_datetime(df.date)
    
    df = df.resample('M').last()
    
    return df

df = fetchData()

mom = 1
yoy = 12
startFrom = 2011

df['chg'] = df.close.pct_change(mom).fillna(0) * 100
table = pd.DataFrame()

columns = ['month']
for year in range(startFrom, 2019):
    columns.append(year)

table_list = []    
for month in range(1,13):
    row = [month]
    for year in range(startFrom, 2019):
        try:
            v = round(df[(df.index.year == year) & (df.index.month == month)].chg.values.item(0), 2)
        except:
            v = 0

        row.append(v)
    
    table_list.append(row)

table = pd.DataFrame(table_list, columns=columns)
table.index = table.month
table.drop('month',axis=1, inplace=True)

print(table)
table.to_csv('performance.csv', sep=',', encoding='utf-8')
