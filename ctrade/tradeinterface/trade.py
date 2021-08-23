"""
Interface to connect codded strategies to binance
Simple funtions for buying and selling
Strategies handle all the thinking and these funtions act on it
"""
import os, sys
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import fileFunctions

try:
    settings = fileFunctions.getMainSettings()
    api_key = settings["apikey"]
    api_secret = settings["apisecretkey"]
    client = Client(api_key, api_secret, testnet=True)
except:
    print("Your API Key is Invalid! Please enter it correctly in settings")