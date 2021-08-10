"""
Main program funtion to initialize and run program
Initialize is called first and run one time
Main is called afterwords and contains the main program loop
"""
import gui
import fileFunctions

def initialize():
    gui.initialize()
    #Load Settings
    #Collect Chart Data
    #Test Binance Connection

def main():
    gui.updateStrategiesGUI()
    try:
        while True:
            gui.refesh()
    except:
        print("Program Closing")
        #Deactivate all strategies
        fileFunctions.disableStrategies()


#Start
initialize()
main()