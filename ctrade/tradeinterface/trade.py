"""
Interface to connect codded strategies to binance
Simple funtions for buying and selling
Strategies handle all the thinking and these funtions act on it
"""
import os, sys
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import fileFunctions

testing = True

settings = fileFunctions.getMainSettings()
try:
    maxTradeSize = settings["maxTradeSize"]
    secCurrency = settings["tradeAgainsedSymbol"]
except:
    maxTradeSize = "0"
    secCurrency = "USDT"
    print("Please configure your settings and restart")
try:
    if testing:
        api_key = settings["testapikey"]
        api_secret = settings["testapisecretkey"]
    else:
        api_key = settings["apikey"]
        api_secret = settings["apisecretkey"]
    client = Client(api_key, api_secret, testnet=testing)
except:
    print("Your API Key is Invalid! Please enter it correctly in settings")


def buy(symbol, buyPrice, ammount):
    #Add feature that checks this againsed max trade price
    order = client.order_limit_buy(
        symbol=symbol+secCurrency, 
        quantity=ammount, 
        price=buyPrice)

def sell(symbol, sellPrice, ammount):
    order = client.order_limit_sell(
        symbol=symbol+secCurrency, 
        quantity=ammount, 
        price=sellPrice)

def orderCancelsOrder(symbol, buyPrice, sellPrice, ammount):
    order = client.create_oco_order(
        symbol=symbol+secCurrency,
        side=SIDE_SELL,
        stopLimitTimeInForce=TIME_IN_FORCE_GTC,
        quantity=ammount,
        stopPrice=sellPrice,
        price=buyPrice)