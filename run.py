# coding: utf-8
import pandas as pd, requests, datetime, json, numpy as np, os

# Download csv file from html link
import urllib
import urllib.request

def fetchData():  

    url = 'http://www.global-view.com/forex-trading-tools/forex-history/exchange_csv_report.html?CLOSE_2=ON&start_date=01/01/2008&stop_date=10/22/2017&Submit=Get%20Monthly%20Stats'
    urllib.request.urlretrieve(url, 'tmp.csv')

    df = pd.read_csv('tmp.csv')
    os.remove('tmp.csv')

    df['date'] = pd.to_datetime(df['Month'])
    
    df.index = pd.to_datetime(df.date)
    df.drop('Month', axis=1, inplace=True)
    df.drop('date', axis=1, inplace=True)
    
    # drop all irrelevant column
    df.drop('USD/JPY High', axis=1, inplace=True)
    df.drop('USD/JPY Low', axis=1, inplace=True)
    df.drop('Unnamed: 4', axis=1, inplace=True)


    df = df.sort_index()
    
    df.rename(columns={'USD/JPY Close': 'close'}, inplace=True)


    return df


df = fetchData()

mom = 1
yoy = 12

df['chg'] = df.close.pct_change(mom).fillna(0) * -100
table = pd.DataFrame()

startFrom = 2013

m = ['month']
for x in range(startFrom, 2018):
    m.append(x)

f = []    
for x in range(1,13):
    l = [x]
    for y in range(startFrom, 2018):
        try:
            gg = df[(df.index.year == y) & (df.index.month == x)].chg.values.item(0)
        except:
            gg = 0

        l.append(gg)
    
    f.append(l)

table = pd.DataFrame(f, columns=m)
table.index = table.month
table.drop('month',axis=1, inplace=True)

print(table)
table.to_csv('performance.csv', sep='\t', encoding='utf-8')
