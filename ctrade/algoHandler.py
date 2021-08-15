"""
Provides an easy way to manage running algorithms
Funtions to Start, Stop, View, and modify algorithms
All algorithm are based on strategies and there settings stored in the strategies.ini config
"""
from ast import literal_eval
import importlib
from threading import Thread

algorithms = []

def startAlgo(pos, listOfSettings):
    """Start's an algorithm with a given position value
    Creates the algorithm based on strategies.ini config settings
    Does nothing if a algorithm is already running on given position value
    """
    for algo in algorithms:
        if algo.strategyNumber == pos:
            return
    #listOfSettings = literal_eval(fileFunctions.readSettings()["strategy"+str(pos)])
    tradedCrypto = listOfSettings[0]
    strategyName = listOfSettings[2]
    if ".py" and strategyName.endswith(".py"):
        strategyName = strategyName[:-len(".py")]
    strategy = importlib.import_module('.' + strategyName, 'strategies') #Import custom strategy
    algorithms.append(strategy.Strategy(pos, tradedCrypto))
    for algo in algorithms:
        if algo.strategyNumber == pos:
            t = Thread(target= algo.run)
            t.start()

def disableAlgo(pos):
    """Disables an algorithm
    First calls the custom algorithms terminate function
    Then removes algorithm from list
    """
    for algo in algorithms:
        if algo.strategyNumber == pos:
            algo.terminate()
            algorithms.remove(algo)

def changeAlgoPos(origional, new):
    """Changes algorithms position value
    Mainly used when strategies config file is rearanged
    """
    for algo in algorithms:
        if algo.strategyNumber == origional:
            algo.strategyNumber = new

def disableAllAlgos():
    """Disables all algorithms
    For when program is shutdown and emergencey use
    """
    for algo in algorithms:
        algo.terminate()
        algorithms.remove(algo)

def getRunningAlgos():
    """Outputs list with current running algorithms
    """
    return algorithms