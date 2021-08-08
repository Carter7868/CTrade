from gui import initializeGUI
from gui import updateStrategiesGUI
from gui import refeshGUI
from fileFunctions import disableStrategies

def initialize():
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
        #Deactivate all strategies
        disableStrategies()


#Start
initialize()
main()
