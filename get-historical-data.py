#!/usr/bin/env python3


import csv
import requests
import pickle
from apikey import API_KEY

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=15min&slice=year1month1&apikey=demo'


BASE_URL = 'https://www.alphavantage.co/query'

def createURL(base, **kwargs):
    argStr = '&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
    urlStr = base + '?' + argStr
    return urlStr

def qryDaSngl(symbol='IBM', function='TIME_SERIES_DAILY', outputsize='compact'):
    with requests.Session() as s:
        download = s.get(createURL(BASE_URL, function=function, symbol=symbol,
                         datatype='csv', outputsize=outputsize, apikey=API_KEY))
    contentStr = download.content.decode('utf-8')
    cr = csv.reader(contentStr.splitlines(), delimiter=',')
    tsList = list(cr)
    print(tsList)
    return (tsList[0], tsList[1:])

def ts2dict(ts):
    return ({ts[0][0]: ts[0][1:]}, {e[0]: e[1:] for e in ts[1]})

def qryData(symbols, function='TIME_SERIES_DAILY', outputsize='compact'): 
    dvs = {}
    for symbol in symbols:
        dk, dv = ts2dict(qryDaSngl(symbol, function, outputsize))
        for k, v in dv.items():
            if k not in dvs:
                dvs[k] = {}
            dvs[k][symbol] = v
    return dvs
    

#print(ts2dict(qryDaSngl()))
with open("stockdata.pickle", "wb") as f:
    #obj = qryData(['NVDA', 'MSFT', 'AMD', 'INTL', 'LSCC', 'IBM', 'XLNX'], 'TIME_SERIES_DAILY_ADJUSTED', 'full')
    obj = qryData(['NVDA', 'MSFT', 'AMD', 'LSCC', 'XLNX'], 'TIME_SERIES_DAILY_ADJUSTED', 'full')
    pickle.dump(obj, f)




