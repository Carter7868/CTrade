#Creates, Updates and Refreshes the GUI
from os import read
import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, END, LEFT, X
from fileFunctions import cleanDictionary, writeSettings #Save Changes To File
from fileFunctions import readSettings #Import Strategies / settings
from fileFunctions import findStrategies #Returns list of .strategy files
from fileFunctions import cleanDictionary #Remakes strategy keys / cleans dictionary
from ast import literal_eval #String To List
from functools import partial #For passing Button Positions

#GUI Settings / Parameters
HEIGHT = 600
WIDTH = 1000
backgroundColor = '#32373B'
offsetgrey = "#cdd1d5"
whiteColor = '#F7F7FF'
orangeColor = '#FE4A49'
greenColor = '#1cfd32'

#Main Window
root = tk.Tk()
root.title("CTrade")
root.geometry(str(WIDTH)+'x'+str(HEIGHT))
root.configure(bg='#232729')

#Main Frame
mainFrame = tk.Frame(root, height=HEIGHT,width=WIDTH,bg=backgroundColor)
mainFrame.place(rely=0.21, relwidth=1,relheight=0.5)


#Global Variables
dropdownEntries = []

def initializeGUI():
    #Creates initial buttons and labels
    #Top Bar Buttons
    settingFrame = tk.Frame(root, height=HEIGHT,width=WIDTH,bg=backgroundColor)
    settingFrame.place(relwidth=1,relheight=0.2)
    addStrategy = tk.Button(settingFrame, text="Add Strategy", bg=whiteColor, command=addStrategyCommand)
    addStrategy.pack(side=LEFT,fill=BOTH,padx=5)
    saveStrategies = tk.Button(settingFrame, text="Save Strategies", bg=whiteColor)
    saveStrategies.pack(side=LEFT,fill=BOTH,padx=5)
    clearStrategies = tk.Button(settingFrame, text="Clear Strategies", bg=whiteColor, command=clearStrategiesCommand)
    clearStrategies.pack(side=LEFT,fill=BOTH,padx=5)
    mainSettings = tk.Button(settingFrame, text="Main Settings", bg=whiteColor)
    mainSettings.pack(side=LEFT,fill=BOTH,padx=5)
    backTest = tk.Button(settingFrame, text="Backtest Strategy's", bg=whiteColor)
    backTest.pack(side=LEFT,fill=BOTH,padx=5)

    #Main Labels
    symbol = tk.Label(mainFrame, bg=backgroundColor, text="Symbol", font=('Helvetica', 10, 'bold'))
    symbol.grid(row=0,column=0,padx= 5,pady=5)
    dataFeed = tk.Label(mainFrame, bg=backgroundColor, text="Data Source", font=('Helvetica', 10, 'bold'))
    dataFeed.grid(row=0,column=1,padx= 5,pady=5)
    stratagy = tk.Label(mainFrame, bg=backgroundColor, text="Select Stratagy", font=('Helvetica', 10, 'bold'))
    stratagy.grid(row=0,column=2,padx= 5,pady=5)
    stratagysettings = tk.Label(mainFrame, bg=backgroundColor, text="Strategy Setting's", font=('Helvetica', 10, 'bold'))
    stratagysettings.grid(row=0,column=3,padx= 5,pady=5)
    info = tk.Label(mainFrame, bg=backgroundColor, text="Strategy Info/Stats", font=('Helvetica', 10, 'bold'))
    info.grid(row=0,column=4,padx= 5,pady=5)
    activate = tk.Label(mainFrame, bg=backgroundColor, text="Activate", font=('Helvetica', 10, 'bold'))
    activate.grid(row=0,column=5,padx= 5,pady=5)
    pause = tk.Label(mainFrame, bg=backgroundColor, text="Pause", font=('Helvetica', 10, 'bold'))
    pause.grid(row=0,column=6,padx= 5,pady=5)
    remove = tk.Label(mainFrame, bg=backgroundColor, text="Remove", font=('Helvetica', 10, 'bold'))
    remove.grid(row=0,column=7,padx= 5,pady=5)

    #Trading Stats
    statsFrame = tk.Frame(root, height=HEIGHT,width=WIDTH,bg=backgroundColor)
    statsFrame.place(rely=0.72, relwidth=1,relheight=0.5)


    root.update()

def updateStrategiesGUI():
    #Updates Labels and Buttons Within Strategy Section
    for widget in mainFrame.winfo_children(): #Clear All Widgets
        widget.destroy()
        #Main Labels
    dropdownEntries.clear()
    strategies = readSettings() #Import Dictionary With Settings As List
    for i in range(len(strategies)): #Loop through all strategies
        settingsString = strategies["strategy" + str(i)] #Convert Strings to List
        settingslist = literal_eval(settingsString)
        #Display Labels / Settings
        symbol = tk.Label(mainFrame, bg=offsetgrey, text=settingslist[0])
        symbol.grid(row=i+1,column=0,padx= 5,pady=5)
        dataFeed = tk.Label(mainFrame, bg=offsetgrey, text=settingslist[1])
        dataFeed.grid(row=i+1,column=1,padx= 5,pady=5)
        #Strategy Select Drop Down Option
        tkvar = tk.StringVar(root)
        tkvar.set(settingslist[2])#Set Default Option To File Specified
        strategy = tk.OptionMenu(mainFrame, tkvar, *findStrategies(), command=dropdownUpdater)
        strategy.grid(row=i+1,column=2,padx= 5,pady=5)
        dropdownEntries.append(tkvar)
        #Settings Button
        settingsbtn = tk.Button(mainFrame, bg=whiteColor, text="Settings")
        settingsbtn.grid(row=i+1,column=3,padx= 5,pady=5)
        #Status Button
        if settingslist[3] == 0: #Convert 1,0 to true,false for display
            running = False
        else:
            running = True
        statsbtn = tk.Button(mainFrame, bg=whiteColor, text="Running: " + str(running))
        statsbtn.grid(row=i+1,column=4,padx= 5,pady=5)
        #Activate / Pause Button
        if running == True:
            activeButton = tk.Button(mainFrame, bg=greenColor, text="Activate", command=partial(activeButtonUpdater,i))
            pauseButton = tk.Button(mainFrame, bg=whiteColor, text="Pause", command=partial(pauseButtonUpdater,i))
        else:
            activeButton = tk.Button(mainFrame, bg=whiteColor, text="Activate", command=partial(activeButtonUpdater,i))
            pauseButton = tk.Button(mainFrame, bg=orangeColor, text="Pause", command=partial(pauseButtonUpdater,i))
        activeButton.grid(row=i+1,column=5,padx= 5,pady=5)
        pauseButton.grid(row=i+1,column=6,padx= 5,pady=5)
        #Remove button
        removebtn = tk.Button(mainFrame, bg=whiteColor, text="Remove", command=partial(removeButtonUpdater,i))
        removebtn.grid(row=i+1,column=7,padx= 5,pady=5)

def refeshGUI():
    #Updates GUI
    root.update()
    root.update_idletasks()

def dropdownUpdater(object):
    #Loop Through All DropDowns and save all there values
    strategies = readSettings() #Import Dictionary With Settings As List
    i = 0
    for dropdown in dropdownEntries: #For Each Dropdown Menu
        settingsString = strategies["strategy"+str(i)]#Convert dictionary to list of settings
        settingsList = literal_eval(settingsString)#Covert list string to list type
        settingsList[2] = dropdown.get()
        strategies["strategy"+str(i)] = str(settingsList)
        i += 1
    writeSettings(strategies)
        
def activeButtonUpdater(position):
    print(position)
    strategies = readSettings() #Import Dictionary With Settings As List
    settingsString = strategies["strategy"+str(position)]#Convert dictionary to list of settings
    settingsList = literal_eval(settingsString)#Covert list string to list type
    if settingsList[3] == 0:
        settingsList[3] = 1
    strategies["strategy"+str(position)] = str(settingsList)
    writeSettings(strategies)
    updateStrategiesGUI()

def pauseButtonUpdater(position):
    strategies = readSettings() #Import Dictionary With Settings As List
    settingsString = strategies["strategy"+str(position)]#Convert dictionary to list of settings
    settingsList = literal_eval(settingsString)#Covert list string to list type
    if settingsList[3] == 1:
        settingsList[3] = 0
    strategies["strategy"+str(position)] = str(settingsList)
    writeSettings(strategies)
    updateStrategiesGUI()

def removeButtonUpdater(position):
    #Removes strategies that get there remove button clicked
    strategies = readSettings()
    del strategies["strategy"+str(position)]
    strategies = cleanDictionary(strategies)
    writeSettings(strategies)
    updateStrategiesGUI()

def clearStrategiesCommand():
    strategies = readSettings()
    strategies.clear()
    writeSettings(strategies)
    updateStrategiesGUI()

def addStrategyCommand():
    addStrategyWindow = tk.Toplevel(root,bg=backgroundColor)
    addStrategyWindow.title("CTrade - Add Strategy")
    addStrategyWindow.geometry("400x200")
    #Label's
    symbol = tk.Label(addStrategyWindow, bg=backgroundColor, text="Symbol", font=('Helvetica', 10, 'bold'))
    symbol.grid(row=0,column=0,padx= 5,pady=5)
    strategyLabel = tk.Label(addStrategyWindow, bg=backgroundColor, text="Strategy", font=('Helvetica', 10, 'bold'))
    strategyLabel.grid(row=0,column=1,padx= 5,pady=5)
    activeLabel = tk.Label(addStrategyWindow, bg=backgroundColor, text="Active", font=('Helvetica', 10, 'bold'))
    activeLabel.grid(row=0,column=2,padx= 5,pady=5)
    #Crypto Selection
    symbolVar = tk.StringVar()
    cryptoSymbol = tk.Entry(addStrategyWindow, textvariable=symbolVar)
    cryptoSymbol.grid(row=1,column=0,padx= 5,pady=5)
    cryptoSymbol.insert(END, "/USDT")
    #Active Button
    activeVar = tk.IntVar(value=0)
    activeBTN = tk.Checkbutton(addStrategyWindow, text='Start Active?',bg=backgroundColor, variable=activeVar)
    activeBTN.grid(row=1,column=2,padx= 5,pady=5)
    #Strategies selection tab
    tkvar = tk.StringVar(addStrategyWindow)
    tkvar.set(findStrategies()[0])#Set Default Option To File Specified
    strategy = tk.OptionMenu(addStrategyWindow, tkvar, *findStrategies())
    strategy.grid(row=1,column=1,padx= 5,pady=5)
    dropdownEntries.append(tkvar)
    #Cancel Button
    cancelBTN = tk.Button(addStrategyWindow, text='Close', command=addStrategyWindow.destroy)
    cancelBTN.grid(row=2,column=2,padx= 5,pady=75)
    #Add Button
    addBTN = tk.Button(addStrategyWindow, text='Add', command=partial(addStrategy,symbolVar, activeVar, tkvar))
    addBTN.grid(row=2,column=1,padx= 5,pady=75)

def addStrategy(symbol, active, strategy):
    dictionary = readSettings()
    settingsList = [str(symbol.get()), "Binance",  str(strategy.get()), active.get()]
    dictionary["strategy"] = str(settingsList)
    dictionary = cleanDictionary(dictionary)
    writeSettings(dictionary)
    updateStrategiesGUI()