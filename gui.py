"""
For managing and responding to the graphical user interface (GUI)
Funtions to Initialize, Refresh, and Update the GUI
Also Contains "Updaters" that respond to button clicks and other various forms of user input
The RefreshGUI() function is called in a loop
"""
import algoHandler
import tkinter as tk
from tkinter.constants import BOTH, END, LEFT
import fileFunctions
from ast import literal_eval
from functools import partial

"""
Listed below are basic adjustable parameters for modifing the GUI's appearance
You may wish to change sizing or colors depending on your monitor size and color preference
"""
HEIGHT = 600
WIDTH = 1000
backingColor = '#424242'
backgroundColor = '#616161'



offsetgrey = "#cdd1d5"
whiteColor = '#F7F7FF'
orangeColor = '#FE4A49'
greenColor = '#1cfd32'

#Creating Main Window
root = tk.Tk()
root.title("CTrade")
root.geometry(str(WIDTH)+'x'+str(HEIGHT))
root.configure(bg='#232729')

#Creating Main Frame
mainFrame = tk.Frame(root, height=HEIGHT,width=WIDTH,bg=backgroundColor)
mainFrame.place(rely=0.21, relwidth=1,relheight=0.5)

dropdownEntries = []

def initialize():
    """Creates Initial Frames, Buttons, and Labels
    To Do: Font Variable?
    """
    #Top Bar Buttons
    settingFrame = tk.Frame(root, height=HEIGHT,width=WIDTH,bg=backgroundColor)
    settingFrame.place(relwidth=1,relheight=0.2)
    addStrategy = tk.Button(settingFrame, text="Add Strategy", bg=whiteColor, command=addStrategyCommand)
    addStrategy.pack(side=LEFT,fill=BOTH,padx=5)
    saveStrategies = tk.Button(settingFrame, text="Save Strategies", bg=whiteColor)
    saveStrategies.pack(side=LEFT,fill=BOTH,padx=5)
    clearStrategies = tk.Button(settingFrame, text="Clear Strategies", bg=whiteColor, command=clearStrategiesCommand)
    clearStrategies.pack(side=LEFT,fill=BOTH,padx=5)
    mainSettings = tk.Button(settingFrame, text="Main Settings", bg=whiteColor, command=settingsCommand)
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
    """Updateds labels and buttons in strategy section
    Updates the strategy section of the gui based on strategies.ini config settings and user input
    Deletes all widgets and then loops through all strategies / rows and displays the settings
    """
    for widget in mainFrame.winfo_children():
        widget.destroy()
    dropdownEntries.clear()
    settingsDictionary = fileFunctions.readSettings()
    for strategyNumber in range(len(settingsDictionary)):
        settingsList = literal_eval(settingsDictionary["strategy" + str(strategyNumber)])
        #Display Labels / Settings
        symbol = tk.Label(mainFrame, bg=offsetgrey, text=settingsList[0])
        symbol.grid(row=strategyNumber+1,column=0,padx= 5,pady=5)
        dataFeed = tk.Label(mainFrame, bg=offsetgrey, text=settingsList[1])
        dataFeed.grid(row=strategyNumber+1,column=1,padx= 5,pady=5)
        #Strategy Select Drop Down Option
        tkvar = tk.StringVar(root)
        tkvar.set(settingsList[2])
        strategy = tk.OptionMenu(mainFrame, tkvar, *fileFunctions.findStrategies(), command=dropdownUpdater)
        strategy.grid(row=strategyNumber+1,column=2,padx= 5,pady=5)
        dropdownEntries.append(tkvar)
        #Settings Button
        settingsbtn = tk.Button(mainFrame, bg=whiteColor, text="Settings")
        settingsbtn.grid(row=strategyNumber+1,column=3,padx= 5,pady=5)
        #Status Button
        if settingsList[3] == 0:
            isRunning = False
        else:
            isRunning = True
        statsbtn = tk.Button(mainFrame, bg=whiteColor, text="Running: " + str(isRunning))
        statsbtn.grid(row=strategyNumber+1,column=4,padx= 5,pady=5)
        #Activate / Pause Button
        if isRunning == True:
            activeButton = tk.Button(mainFrame, bg=greenColor, text="Activate", command=partial(activeButtonUpdater,strategyNumber))
            pauseButton = tk.Button(mainFrame, bg=whiteColor, text="Pause", command=partial(pauseButtonUpdater,strategyNumber))
        else:
            activeButton = tk.Button(mainFrame, bg=whiteColor, text="Activate", command=partial(activeButtonUpdater,strategyNumber))
            pauseButton = tk.Button(mainFrame, bg=orangeColor, text="Pause", command=partial(pauseButtonUpdater,strategyNumber))
        activeButton.grid(row=strategyNumber+1,column=5,padx= 5,pady=5)
        pauseButton.grid(row=strategyNumber+1,column=6,padx= 5,pady=5)
        #Remove button
        removebtn = tk.Button(mainFrame, bg=whiteColor, text="Remove", command=partial(removeButtonUpdater,strategyNumber))
        removebtn.grid(row=strategyNumber+1,column=7,padx= 5,pady=5)

def refesh():
    """Refreshes / Updates GUI
    Should be repetivly called in main loop
    """
    root.update()
    root.update_idletasks()

def dropdownUpdater(object):
    """Loop through all strategy drop downs and save values to strategies.ini
    To Do: Change this to only save specific drop down that called it similar to buttons
    """
    settingsDictionary = fileFunctions.readSettings()
    strategyNumber = 0
    for dropdown in dropdownEntries: #For Each Dropdown Menu
        settingsList = literal_eval(settingsDictionary["strategy"+str(strategyNumber)])#Covert list string to list type
        settingsList[2] = dropdown.get()
        settingsDictionary["strategy"+str(strategyNumber)] = str(settingsList)
        strategyNumber += 1
    fileFunctions.writeSettings(fileFunctions.cleanDictionary(settingsDictionary))
        
def activeButtonUpdater(position):
    """Activates strategy when "Activate" button is pressed
    Activates the file system and algortithm
    To Do: Check if algo is already active
    """
    settingsDictionary = fileFunctions.readSettings()
    settingsList = literal_eval(settingsDictionary["strategy"+str(position)])
    if settingsList[3] == 0:
        settingsList[3] = 1
    settingsDictionary["strategy"+str(position)] = str(settingsList)
    fileFunctions.writeSettings(fileFunctions.cleanDictionary(settingsDictionary))
    updateStrategiesGUI()
    algoHandler.startAlgo(position, literal_eval(fileFunctions.readSettings()["strategy"+str(position)]))

def pauseButtonUpdater(position):
    """Deactivates strategy when "Pause" button is pressed
    Deactivates the file system and algortithm
    """
    settingsDictionary = fileFunctions.readSettings()
    settingsList = literal_eval(settingsDictionary["strategy"+str(position)])
    if settingsList[3] == 1:
        settingsList[3] = 0
    settingsDictionary["strategy"+str(position)] = str(settingsList)
    fileFunctions.writeSettings(fileFunctions.cleanDictionary(settingsDictionary))
    updateStrategiesGUI()
    algoHandler.disableAlgo(position)

def removeButtonUpdater(position):
    """Removes strategies when remove button is clicked
    if strategy is running when remove is pressed it is disabled before deleted
    """
    settingsDictionary = fileFunctions.readSettings()
    settingsList = literal_eval(settingsDictionary["strategy"+str(position)])
    if settingsList[3] == 1:
        pauseButtonUpdater(position)
    del settingsDictionary["strategy"+str(position)]
    fileFunctions.writeSettings(fileFunctions.cleanDictionary(settingsDictionary))
    updateStrategiesGUI()

def clearStrategiesCommand():
    """Clears all displayed strategies from GUI
    Loops through all strategies and calls the removeButtonUpdater()
    """
    settingsDictionary = fileFunctions.readSettings()
    for strategy in settingsDictionary:
        removeButtonUpdater(0)

def addStrategyCommand():
    """Opens new window that allows user to add strategy
    Strategies can be added until user presses the "Close" button
    """
    addStrategyWindow = tk.Toplevel(root,bg=backgroundColor)
    addStrategyWindow.title("CTrade - Add Strategy")
    addStrategyWindow.geometry("350x200")
    #Label's
    symbol = tk.Label(addStrategyWindow, bg=backgroundColor, text="Symbol", font=('Helvetica', 10, 'bold'))
    symbol.grid(row=0,column=0,padx= 5,pady=5)
    strategyLabel = tk.Label(addStrategyWindow, bg=backgroundColor, text="Strategy", font=('Helvetica', 10, 'bold'))
    strategyLabel.grid(row=0,column=1,padx= 5,pady=5)
    #Crypto Selection
    symbolVar = tk.StringVar()
    cryptoSymbol = tk.Entry(addStrategyWindow, textvariable=symbolVar)
    cryptoSymbol.grid(row=1,column=0,padx= 5,pady=5)
    cryptoSymbol.insert(END, "/USDT")
    #Strategies selection tab
    tkvar = tk.StringVar(addStrategyWindow)
    tkvar.set(fileFunctions.findStrategies()[0])
    strategy = tk.OptionMenu(addStrategyWindow, tkvar, *fileFunctions.findStrategies())
    strategy.grid(row=1,column=1,padx= 5,pady=5)
    dropdownEntries.append(tkvar)
    #Cancel Button
    cancelBTN = tk.Button(addStrategyWindow, text='Close', command=addStrategyWindow.destroy)
    cancelBTN.grid(row=2,column=1,padx= 5,pady=75)
    #Add Button
    addBTN = tk.Button(addStrategyWindow, text='Add', command=partial(addStrategy,symbolVar, tkvar))
    addBTN.grid(row=2,column=0,padx= 5,pady=75)

def addStrategy(symbol, strategy):
    """Adds a strategy to strategies.ini
    This function could potentially be added to fileFunctions along with delete Strategy function
    """
    settingsDictionary = fileFunctions.readSettings()
    settingsList = [str(symbol.get()), "Binance",  str(strategy.get()), 0]
    settingsDictionary["strategy"] = str(settingsList)
    fileFunctions.writeSettings(fileFunctions.cleanDictionary(settingsDictionary))
    updateStrategiesGUI()

def settingsCommand():
    """Opens new window that allows user to edit settings
    Strategies can be added until user presses the "Close" button
    To Do: Add All settings and save button that saves everything Also load settings from file and save when okay is pressed
    """
    mainSettingsWindow = tk.Toplevel(root,bg=backingColor)
    mainSettingsWindow.title("CTrade - Settings")
    mainSettingsWindow.geometry("800x400")

    #Top Bar
    settingsLabelFrame = tk.Frame(mainSettingsWindow, height=HEIGHT,width=WIDTH,bg=backgroundColor)
    settingsLabelFrame.place(relwidth=1,relheight=0.15)
    settingslabel = tk.Label(settingsLabelFrame, bg=backgroundColor, text="Settings:", font=('Helvetica', 15, 'bold'))
    settingslabel.grid(row=0,column=0,padx= 30,pady=5)

    #Settings Area
    mainSettingsDictionary = fileFunctions.getMainSettings()

    settingsFrame = tk.Frame(mainSettingsWindow, height=HEIGHT,width=WIDTH,bg=backingColor)
    settingsFrame.place(rely=0.15, relwidth=1,relheight=1)

    #Variables
    apiKey = tk.StringVar()
    apiSecretKey = tk.StringVar()
    testApiKey = tk.StringVar()
    testApiSecretKey = tk.StringVar()
    portfolioTradePercentage = tk.StringVar()
    try:
        portfolioTradePercentage.set(mainSettingsDictionary["portfolioTradePercentage"])
        testApiSecretKey.set(mainSettingsDictionary["testApiSecretKey"])
        testApiKey.set(mainSettingsDictionary["testApiKey"])
        apiSecretKey.set(mainSettingsDictionary["apiSecretKey"])
        apiKey.set(mainSettingsDictionary["apiKey"])
    except:
        print("Some Values 0")

    apiKeyLabel = tk.Label(settingsFrame, bg=backingColor, text="API Key:", font=('Helvetica', 8))
    apiKeyLabel.grid(row=0,column=0,padx= 30,pady=5)
    apiKeyEntry = tk.Entry(settingsFrame, bg=offsetgrey, textvariable=apiKey)
    apiKeyEntry.grid(row=0,column=1,padx= 30,pady=5)

    apiSecretKeyLabel = tk.Label(settingsFrame, bg=backingColor, text="API Secret Key:", font=('Helvetica', 8))
    apiSecretKeyLabel.grid(row=0,column=2,padx= 30,pady=5)
    apiSecretKeyEntry = tk.Entry(settingsFrame, bg=offsetgrey, textvariable=apiSecretKey)
    apiSecretKeyEntry.grid(row=0,column=3,padx= 30,pady=5)

    testApiKeyLabel = tk.Label(settingsFrame, bg=backingColor, text="Test API Key:", font=('Helvetica', 8))
    testApiKeyLabel.grid(row=1,column=0,padx= 30,pady=5)
    testApiKeyEntry = tk.Entry(settingsFrame, bg=offsetgrey, textvariable=testApiKey)
    testApiKeyEntry.grid(row=1,column=1,padx= 30,pady=5)

    testApiSecretKeyLabel = tk.Label(settingsFrame, bg=backingColor, text="Test API Secret Key:", font=('Helvetica', 8))
    testApiSecretKeyLabel.grid(row=1,column=2,padx= 30,pady=5)
    testApiSecretKeyEntry = tk.Entry(settingsFrame, bg=offsetgrey, textvariable=testApiSecretKey)
    testApiSecretKeyEntry.grid(row=1,column=3,padx= 30,pady=5)

    portfolioTradePercentageLabel = tk.Label(settingsFrame, bg=backingColor, text="Portfolio Trade %(0 - 100):", font=('Helvetica', 8))
    portfolioTradePercentageLabel.grid(row=2,column=0,padx= 30,pady=5)
    portfolioTradePercentEntry = tk.Entry(settingsFrame, bg=offsetgrey, textvariable=portfolioTradePercentage)
    portfolioTradePercentEntry.grid(row=2,column=1,padx= 30,pady=5)

    #Save / Cancel Buttons
    saveBTN = tk.Button(settingsFrame, text='Save', command=partial(saveMainSettings,apiKey,apiSecretKey,testApiKey,testApiSecretKey,portfolioTradePercentage))
    saveBTN.grid(row=5,column=0,padx= 5,pady=75)

    closeBTN = tk.Button(settingsFrame, text='Close', command=mainSettingsWindow.destroy)
    closeBTN.grid(row=5,column=1,padx= 5,pady=75)

def saveMainSettings(apiKey,apiSecretKey,testApiKey,testApiSecretKey,portfolioTradePercentage):
    """Takes various settings and sends to saveMainSettings() as a dictionary
    This is fairly inefficient as each new setting addition requires a slight rewrite
    Lots of work could be done to improve
    """
    mainSettingsDictionary = {"apiKey" : apiKey.get(), "apiSecretKey" : apiSecretKey.get(), "testApiKey" : testApiKey.get(), "testApiSecretKey" : testApiSecretKey.get(), "portfolioTradePercentage" : portfolioTradePercentage.get()}
    fileFunctions.saveMainSettings(mainSettingsDictionary)