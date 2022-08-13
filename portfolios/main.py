from cgitb import handler
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from mangum import Mangum

import os
from datetime import datetime

import yfinance as yf
import pandas as pd

stage = os.environ.get('STAGE', None)
api_prefix = f"/{stage}" if stage else "/"

api = FastAPI(title="investing-app", openapi_prefix=api_prefix)

class WatchStock(BaseModel):
    symbol: str
    marketPrice: Optional[float] = None
    watchPrice: Optional[float] = None
    watchDate: Optional[str] = None

dataStore = dict()
dataStore['AMRS'] =  WatchStock(symbol='AMRS', marketPrice=2.00, watchPrice=2.2634, watchDate='21-12-2018')
dataStore['GEVO'] =  WatchStock(symbol='GEVO', marketPrice=3.05, watchPrice=2.9243, watchDate='21-12-2018')
dataStore['AMZN'] =  WatchStock(symbol='AMZN', marketPrice=100.00, watchPrice=125.796, watchDate='21-01-2022')
dataStore['BNGO'] =  WatchStock(symbol='BNGO', marketPrice=3.43, watchPrice=6.2871, watchDate='21-12-2018')
dataStore['NU'] =  WatchStock(symbol='NU', marketPrice=3.43, watchPrice=5.5541, watchDate='21-12-2018')
dataStore['STNE'] =  WatchStock(symbol='STNE', marketPrice=3.43, watchPrice=14.291, watchDate='21-12-2018')

watchStocks = {
    "AMRS" : { "symbol" : "AMRS", "marketPrice": 2.00,   "watchPrice" : 2.2634, "watchDate" : "21-12-2018" },
    "GEVO" : { "symbol" : "GEVO", "marketPrice" :3.05,   "watchPrice" :2.9243,  "watchDate" : "21-12-2018" },
    "AMZN" : { "symbol" : "AMZN", "marketPrice" :100.00, "watchPrice" :125.796, "watchDate" : "21-01-2022" },
    "BNGO" : { "symbol" : "BNGO", "marketPrice" :3.43,   "watchPrice" :6.2871,  "watchDate" : "21-12-2018" },
      "NU" : { "symbol" : "NU",   "marketPrice" :3.43,   "watchPrice" :5.5541,  "watchDate" : "21-12-2018" },
    "STNE" : { "symbol" : "STNE", "marketPrice" :3.43,   "watchPrice" :14.291,  "watchDate" : "21-12-2018" }
}

def fetch_stock_data():
    stocks = " ".join(str(v.symbol) for k,v in dataStore.items())
    #stockData = yf.download(stocks, period="ytd")
    stockData = yf.download(stocks, start=datetime.today().strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d'))
    for k, v in dataStore.items():
        v.marketPrice = stockData['Close'][v.symbol][0]
        dataStore[v.symbol] = v


@api.get("/watchlist")
async def get_watchlist():
    fetch_stock_data()
    for k, v in dataStore.items():
        v.watchDate = datetime.today().strftime('%d-%m-%Y')
    return list(dataStore.values())


@api.get('/watchlist/{symbol}')
async def get_watchlist(symbol: str):
    return dataStore[symbol.upper()]


@api.post('/watchlist')
def add_watchlist(stock: WatchStock):
    dataStore[stock.symbol] = stock
    return dataStore[stock.symbol]


handler = Mangum(api)
