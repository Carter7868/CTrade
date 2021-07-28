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