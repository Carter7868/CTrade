#For Reading, Writing, and Duplicating Strategies
#All Strategies are stored in files and accessable through these functions
from configparser import ConfigParser
import glob, os
from tkinter.constants import FALSE

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
    os.chdir(r'C:\Users\Carte\Desktop\Other\CTrade\strategies')
    for file in glob.glob("*.strategy"):
        strategieslist.append(file)
    os.chdir(r'C:\Users\Carte\Desktop\Other\CTrade')
    return strategieslist

def cleanDictionary(dictionary):
    #Cleans Dictionary key values
    i = 0
    newDictionary = {}
    for parts in dictionary:
        newDictionary["strategy" + str(i)] = dictionary[parts]
        i += 1
    return newDictionary
    #Check All Strategies, Cryptos, and Providers.