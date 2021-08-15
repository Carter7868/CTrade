"""
For managing strategies.ini config file and other local files
Funtions to Read, Write, and Clean strategies.ini Dictionary
Also has funtion to find custom user strategy files
"""
from configparser import ConfigParser
import glob
import os
import re
from tkinter.constants import FALSE
from ast import literal_eval
import algoHandler

config_object = ConfigParser()

def writeSettings(dictToWrite):
    """Writes a dictionary to the strategies.ini
    Stores as a config object
    Dictionary contains Strategy + num as key. Eg: "Strategy1"
    The value is a list that contains strategy settings Eg. [ETH/USDT, Binance, Example-Strategy.py, 1]
    """
    config_object["Strategy's"] = dictToWrite
    with open('FileStorage.ini', 'w') as conf:
        config_object.write(conf)

def readSettings():
    """Reads and returns a dictionary of settings from strategies.ini
    Dictionary contains Strategy + num as key. Eg: "Strategy1"
    The value is a list that contains strategy settings Eg. [ETH/USDT, Binance, Example-Strategy.py, 1]
    Note: List must be converted from a string to a list after it is pulled from the dictionary
    """
    config_object.read("FileStorage.ini")
    return config_object["Strategy's"]

def findStrategies():
    """Locates strategy files in the "Strategies" file and returns them
    Returns a list cointaining the full name of all files
    Strategy files must contain -strategy.py on the end
    """
    listOfStrategyFiles = []
    print(os.path.normpath(os.path.realpath(__file__) + os.sep + os.pardir + os.sep + os.pardir + os.sep + 'strategies'))

    #os.chdir(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'strategies')
    os.chdir(os.path.normpath(os.path.realpath(__file__) + os.sep + os.pardir + os.sep + os.pardir + os.sep + 'strategies'))
    for strategyFile in glob.glob("*-strategy.py"):
        test = "rwst"
        listOfStrategyFiles.append(strategyFile)
    #os.chdir()
    os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
    return listOfStrategyFiles

def cleanDictionary(OldDictionary):
    """Cleans provided dictionary and reorganizes running algorithms accordingly
    To Do:
        -Automatically write the dictionary after cleaning it
        -Back test listed cryptos to make sure they are treadable on binance
    """
    newPositionNumber = 0
    cleanedDictionary = {}
    for strategy in OldDictionary:
        #Rearange Running Algoritms
        listOfRunningAlgos = algoHandler.getRunningAlgos()
        for algorithm in listOfRunningAlgos:
            oldStrategyNumber = re.sub('\D', '', str(strategy))
            if algorithm.strategyNumber == int(oldStrategyNumber):
                algoHandler.changeAlgoPos(algorithm.strategyNumber, newPositionNumber)
        #Rearange File / Dictionary
        cleanedDictionary["strategy" + str(newPositionNumber)] = OldDictionary[strategy]
        newPositionNumber += 1
    return cleanedDictionary

def disableStrategies():
    """Disables all current strategies and runnin algorithms
    Called when the program shuts down (and in configurable emergencys - to do)
    """
    stratDictionary = readSettings()
    position = 0
    for strategy in stratDictionary:
        listOfSettings = literal_eval(stratDictionary["strategy"+str(position)])
        if listOfSettings[3] == 1:
            listOfSettings[3] = 0
        stratDictionary["strategy"+str(position)] = str(listOfSettings)
        algoHandler.disableAlgo(position) #Temporary fix
        position+=1
    algoHandler.disableAllAlgos()
    writeSettings(cleanDictionary(stratDictionary))

def saveMainSettings(dictionary):
    config_object["Main Settings"] = dictionary
    with open('FileStorage.ini', 'w') as conf:
        config_object.write(conf)

def getMainSettings():
    #Check if file exists otherwise use defaults
    try:
        config_object.read("FileStorage.ini")
        return config_object["Main Settings"]
    except:
        config_object["Main Settings"] = {}
        with open('FileStorage.ini', 'w') as conf:
            config_object.write(conf)