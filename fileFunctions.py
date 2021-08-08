#For Reading, Writing, and Duplicating Strategies
#All Strategies are stored in files and accessable through these functions
from configparser import ConfigParser
import glob, os
import re
from tkinter.constants import FALSE
from ast import literal_eval
import algoHandler

#Get the configparser object
config_object = ConfigParser()

def writeSettings(dictToWrite):
    #Write dictionary with settings to file
    config_object["Strategy's"] = dictToWrite
    with open('strategies.ini', 'w') as conf:
        config_object.write(conf)

def readSettings():
    #Read and return dictionary with settings to file
    config_object.read("strategies.ini")
    return config_object["Strategy's"]

def findStrategies():
    #Finds .strategy files and returns them in a list
    strategieslist = []
    os.chdir(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'strategies')
    for file in glob.glob("*-strategy.py"):
        strategieslist.append(file)
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    return strategieslist

def cleanDictionary(dictionary):
    #Cleans Dictionary key values
    i = 0
    newDictionary = {}
    for parts in dictionary:
        #---Rearange Running Algoritms ---
        algorithms = algoHandler.getRunningAlgos()
        for algo in algorithms:
            number = re.sub('\D', '', str(parts))
            if algo.strategyNumber == int(number):
                algoHandler.changeAlgoPos(algo.strategyNumber, i)
        #Rearange File / Dictionary
        newDictionary["strategy" + str(i)] = dictionary[parts]
        i += 1
    return newDictionary

    #Check All Strategies, Cryptos, and Providers.

#Add Function to disable all strategies
def disableStrategies():
    strategies = readSettings() #Import Dictionary With Settings As List
    position = 0
    for strategy in strategies:
        settingsString = strategies["strategy"+str(position)]#Convert dictionary to list of settings
        settingsList = literal_eval(settingsString)#Covert list string to list type
        if settingsList[3] == 1:
            settingsList[3] = 0
        strategies["strategy"+str(position)] = str(settingsList)
        algoHandler.disableAlgo(position)
        position+=1
    strategies = cleanDictionary(strategies)
    writeSettings(strategies)