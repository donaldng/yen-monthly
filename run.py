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
startFrom = 2013

df['chg'] = df.close.pct_change(mom).fillna(0) * -100
table = pd.DataFrame()

columns = ['month']
for year in range(startFrom, 2018):
    columns.append(year)

table_list = []    
for month in range(1,13):
    row = [month]
    for year in range(startFrom, 2018):
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
