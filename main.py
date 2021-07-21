#Started 06/19/21
#Last Edited 06/19/21
#Do Not Copy, Use, Distribute, or Edit

from gui import initializeGUI
from gui import updateStrategiesGUI
from gui import refeshGUI

def initialize():
    #Initialize Program
    print("Initializing...")
    #Load GUI
    initializeGUI()
    #Load Settings
    #Collect Chart Data
    #Test Binance Connection

def main():
    #Main Funtion
    updateStrategiesGUI()
    print("Program Started")
    try:
        while True:
            refeshGUI()
    except:
        print("Program Closing")


#Start
initialize()
main()

#1) Create Strategy Handler File with function that starts and stops strategies based on user input in a thread (Calls Strategy's Start / Stop Function)
#2) Create a strategy interface for buying / selling crypto easily and getting position / account updates
#3) Create a file that provides stock data to the algoritm and premade indicators
#4) Create a way to backtest strategys specific periods 

#Add New Pop Up Window for Save Stategies
#Create New Strategy Handler file that checks for active strategies and Runs them in a seperate thread
#Figure out previous data storage / make a file for all indicators that can easily be accessed. Ex: indicators.ema(1, 50) would return the 50 day ema at a 1 min time interval
#Add a new file that provides framework to buy and sell easily. Ex: buy(BTC, 0.001, $41030)
#Add file that constantly checks for errors (Oversold, High losses) and shuts down program
#When window is closed program should sell all current open positions / Make a sell all button (Red in top corner of window) and set file to inactivate strategy
#Test
