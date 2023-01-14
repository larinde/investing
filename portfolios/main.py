from cgitb import handler
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.openapi.utils import get_openapi
#from mangum import Mangum

import os
from datetime import datetime

import yfinance as yf
import pandas as pd

#stage = os.environ.get('STAGE', None)
#api_prefix = f"/{stage}" if stage else "/"

#api = FastAPI(title="investing-app", openapi_prefix=api_prefix)
api = FastAPI(title="investing-app")


class Position(BaseModel):
    isin: Optional[str] = None
    symbol: Optional[str] = None
    stockName: Optional[str] = None
    quantity: Optional[int] = None
    orderUnitPrice: Optional[float] = None
    orderCurrency: Optional[str] = None
    bookCost: Optional[float] = None
    orderDate: Optional[str] = None
    marketPrice: Optional[float] = None

class Portfolio(BaseModel):
    accountId: Optional[str] = None
    accountName: Optional[str] = None
    accountType: Optional[str] = None
    positions: list[Position]

class Portfolios(BaseModel):
    size: int = None
    portfolios: list[Portfolio]

class WatchStock(BaseModel):
    symbol: str
    marketPrice: Optional[float] = None
    watchPrice: float = None
    watchDate: str = None


position = Position(isin="US0231351067", symbol="AMZN", stockName="Amazon", quantity=40, orderUnitPrice=125.796, orderCurrency="USD", bookCost=4745.46, orderDate="04.05.2022", marketPrice=123.65 )

positionList = []
positionList.append(position)    

portfolio = Portfolio(accountId='1', accountName='Ing Diba', accountType='Trading', positions=positionList)

portfolioList = []
portfolioList.append(portfolio)

portfolios = Portfolios(size=1, portfolios=portfolioList)



dataStore = dict()
dataStore['AMRS'] =  WatchStock(symbol='AMRS', marketPrice=2.00, watchPrice=2.2634, watchDate='21-12-2018')
dataStore['GEVO'] =  WatchStock(symbol='GEVO', marketPrice=3.05, watchPrice=2.9243, watchDate='21-12-2018')
dataStore['AMZN'] =  WatchStock(symbol='AMZN', marketPrice=100.00, watchPrice=125.796, watchDate='21-01-2022')
dataStore['BNGO'] =  WatchStock(symbol='BNGO', marketPrice=3.43, watchPrice=6.2871, watchDate='21-12-2018')
dataStore['STNE'] =  WatchStock(symbol='STNE', marketPrice=3.43, watchPrice=14.291, watchDate='21-12-2018')
dataStore['NU'] =  WatchStock(symbol='NU', marketPrice=3.43, watchPrice=5.5541, watchDate='21-12-2018')
dataStore['LU'] =  WatchStock(symbol='LU', marketPrice=0.00, watchPrice=5.555, watchDate='04-04-2022')
#dataStore['TGA.L'] =  WatchStock(symbol='TGA.L', marketPrice=0.00, watchPrice=1829, watchDate='21-09-2022')

#watchStocks = {
#    "AMRS" : { "symbol" : "AMRS", "marketPrice": 2.00,   "watchPrice" : 2.2634, "watchDate" : "21-12-2018" },
#    "GEVO" : { "symbol" : "GEVO", "marketPrice" :3.05,   "watchPrice" :2.9243,  "watchDate" : "21-12-2018" },
#    "AMZN" : { "symbol" : "AMZN", "marketPrice" :100.00, "watchPrice" :125.796, "watchDate" : "21-01-2022" },
#    "BNGO" : { "symbol" : "BNGO", "marketPrice" :3.43,   "watchPrice" :6.2871,  "watchDate" : "21-12-2018" },
#      "NU" : { "symbol" : "NU",   "marketPrice" :3.43,   "watchPrice" :5.5541,  "watchDate" : "21-12-2018" },
#    "STNE" : { "symbol" : "STNE", "marketPrice" :3.43,   "watchPrice" :14.291,  "watchDate" : "21-12-2018" }
#}


def fetch_stock_data():
    stocks = " ".join(str(v.symbol) for k,v in dataStore.items())
    #stockData = yf.download(stocks, period="ytd")
    stockData = yf.download(stocks, start=datetime.today().strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d'))
    for k, v in dataStore.items():
        v.marketPrice = stockData['Close'][v.symbol][0]
        dataStore[v.symbol] = v
    
    
@api.get('/portfolios', include_in_schema=True)
async def getPortfolios():
    return portfolios

@api.post('/portfolios', include_in_schema=True)
async def addPortfolios(portfolios: Portfolios):
    return portfolios

@api.get('/portfolios/{accountId}', include_in_schema=True)
async def getPortfolioById(accountId: str):
    return portfolio


@api.get("/watchlists")
async def getWatchlists():
    fetch_stock_data()
    for k, v in dataStore.items():
        v.watchDate = datetime.today().strftime('%d-%m-%Y')
    return list(dataStore.values())


@api.get('/watchlists/{symbol}')
async def getWatchlists(symbol: str):
    return dataStore[symbol.upper()]


@api.post('/watchlists')
async def addWatchlists(stock: WatchStock):
    dataStore[stock.symbol] = stock
    return dataStore[stock.symbol]


#handler = Mangum(api)



def custom_openapi():
    if api.openapi_schema:
        return api.openapi_schema
    openapi_schema = get_openapi(
        title="Personal Investment Management",
        version="1.0.0",
        description="This API defines a specification for a personal investment management service.",
        routes=api.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    api.openapi_schema = openapi_schema
    return api.openapi_schema


api.openapi = custom_openapi
