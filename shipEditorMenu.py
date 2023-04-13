from functools import partial
from naglowek import dynamic_object
from rootCommands import *
from tkinter import *
import configparser
from functools import partial
import os

import systems 
import naglowek

def systemChoice(thrustersChoice,uiElements):
    x=10
def subsystemChoice(thrustersChoice,uiElements):
    x=10
def engineChoice(thrustersChoice,uiElements):
    x=10
def thrustersChoice(thrustersChoice,uiElements):
    x=10
def radarChoice(radarChoice,uiElements):
    x=10
def generatorChoice(radarChoice,uiElements):
    x=10
def closeWindow(window):
    window.destroy()

def saveShip(info,uiElements,filePath):

    cp = configparser.ConfigParser()
    cp.read(filePath)
    shipName = str((uiElements.shipNameInput).get())

    if(not(len(shipName) == 0 or shipName == "Ship must have a name. Insert the name to continue.")):
        print(shipName)
        if(not cp.has_section(shipName)):
            cp.add_section(shipName)

        cp.set(shipName, "systemslots1",str((info.systemChoice0).get()))
        cp.set(shipName, "systemslots2",str((info.systemChoice1).get()))
        cp.set(shipName, "systemslots3",str((info.systemChoice2).get()))
        cp.set(shipName, "systemslots4",str((info.systemChoice3).get()))
        cp.set(shipName, "systemslots5",str((info.systemChoice4).get()))
        cp.set(shipName, "systemslots6",str((info.systemChoice5).get()))
        cp.set(shipName, "systemslots7",str((info.systemChoice6).get()))
        cp.set(shipName, "systemslots8",str((info.systemChoice7).get()))
        
        cp.set(shipName, "subsystemslots1",str((info.subsystemChoice0).get()))
        cp.set(shipName, "subsystemslots2",str((info.subsystemChoice1).get()))
        cp.set(shipName, "subsystemslots3",str((info.subsystemChoice2).get()))
        cp.set(shipName, "subsystemslots4",str((info.subsystemChoice3).get()))
        cp.set(shipName, "subsystemslots5",str((info.subsystemChoice4).get()))
        cp.set(shipName, "subsystemslots6",str((info.subsystemChoice5).get()))
        cp.set(shipName, "subsystemslots7",str((info.subsystemChoice6).get()))
        cp.set(shipName, "subsystemslots8",str((info.subsystemChoice7).get()))

        cp.set(shipName, "engine",str((info.engineChoice).get()))
        cp.set(shipName, "thrusters",str((info.thrustersChoice).get()))
        cp.set(shipName, "radar",str((info.radarChoice).get()))
        cp.set(shipName, "engine",str((info.generatorChoice).get()))
        cp.set(shipName, "owner","player1")
        cp.set(shipName, "shipName",shipName)
        hd = open(filePath, "w")
        cp.write(hd)
        hd.close()
        window = tk.Toplevel()
        label = tk.Label(window, text=("'" + shipName + "' \n \n" + " saved successfully") )

        window.config(width = len(shipName) * 6 + 200,height = 200)
        closeWindowCommand = partial(closeWindow,window)
        button = tk.Button(window, text = "Ok", width = 5, height = 1,command=closeWindowCommand)
        label.place(relx=0.5, rely=0.2,anchor=CENTER)
        button.place(relx=0.5, rely=0.5,anchor=CENTER)
    else:
        (uiElements.shipNameInput).delete(0, END)
        (uiElements.shipNameInput).insert(0, "Ship must have a name. Insert the name to continue.") 
        print("aaa")
#engine = engine1
#thrusters = thrusters1
#radar = radar1
#powergenerator = powerGenerator1
#detectionrange = 100

    """
    file = open(filePath)
    config.set(shipName, "playerName",shipName)
    config.write(file)
    file.close()"""


def completeShip(uiElements):
    x=10
def clearShip(uiElements):
    x=10



def shipEditor(root,config,uiMenuElements,uiMetrics,menuUiElements):
    if(not naglowek.editorUiReady):

        config = configparser.ConfigParser()
        cwd = os.getcwd()
        filePath = os.path.join(cwd, "game_data/custom_ships.ini")
        config.read(filePath)
        
        shipOptions = config.sections()
        systemOptions = naglowek.allSystemsList
        subsystemOptions = naglowek.allSubsystemsList

        engineOptions = naglowek.allEnginesList
        thrusterOptions = naglowek.allThrustersList
        radarOptions = naglowek.allRadarsList
        generatorOptions = naglowek.allGeneratorsList

        uiElementsList = []
        uiElements = dynamic_object()
        systemOptions = naglowek.allSystemsList    
        uiElements.systemStatsLabelFrame = tk.LabelFrame(root,text = "changed systems statiistics:")
        uiElements.shipStatsLabelFrame = tk.LabelFrame(root,text = "ship statiistics:")
        uiElements.shipNameInput = tk.Entry(root,width = 50)
        uiElementsList.append(uiElements.shipNameInput)

        info = naglowek.shipEditorInfo

        info.engineChoice = StringVar(root)
        info.thrustersChoice = StringVar(root)
        info.radarChoice = StringVar(root)
        info.generatorChoice = StringVar(root)

        uiElements.engineChoiceMenu =  OptionMenu(root, info.engineChoice, *engineOptions, command=lambda _: engineChoice(info.engineChoice,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.thrustersChoiceMenu = OptionMenu(root,info.thrustersChoice, *thrusterOptions, command=lambda _: thrustersChoice(info.thrusterChoice,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.radarChoiceMenu = OptionMenu(root,info.radarChoice, *radarOptions, command=lambda _: radarChoice(info.radarChoice,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.generatorChoiceMenu = OptionMenu(root,info.generatorChoice, *generatorOptions, command=lambda _: generatorChoice(info.thrusterChoice,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
    
        engineChoice(info.engineChoice,uiElements)
        thrustersChoice(info.thrustersChoice,uiElements)
        radarChoice(info.thrustersChoice,uiElements)
        generatorChoice(info.generatorChoice,uiElements)

        (info.engineChoice).set(engineOptions[0])
        (info.thrustersChoice).set(thrusterOptions[0])
        (info.radarChoice).set(radarOptions[0])
        (info.generatorChoice).set(generatorOptions[0])

        uiElementsList.append(uiElements.engineChoiceMenu)
        uiElementsList.append(uiElements.thrustersChoiceMenu)
        uiElementsList.append(uiElements.radarChoiceMenu)
        uiElementsList.append(uiElements.generatorChoiceMenu)


        info.systemChoice0 = StringVar(root)
        info.systemChoice1 = StringVar(root)
        info.systemChoice2 = StringVar(root)
        info.systemChoice2 = StringVar(root)
        info.systemChoice3 = StringVar(root)
        info.systemChoice4 = StringVar(root)
        info.systemChoice5 = StringVar(root)
        info.systemChoice6 = StringVar(root)
        info.systemChoice7 = StringVar(root)

        info.subsystemChoice0 = StringVar(root)
        info.subsystemChoice1 = StringVar(root)
        info.subsystemChoice2 = StringVar(root)
        info.subsystemChoice2 = StringVar(root)
        info.subsystemChoice3 = StringVar(root)
        info.subsystemChoice4 = StringVar(root)
        info.subsystemChoice5 = StringVar(root)
        info.subsystemChoice6 = StringVar(root)
        info.subsystemChoice7 = StringVar(root)

        uiElements.systemChoiceLabelFrame = tk.LabelFrame(root,width = uiMetrics.editorsystemsWidth,text = "Systems", height = 450)
        uiElementsList.append(uiElements.systemChoiceLabelFrame)

        uiElements.systemChoiceMenu0 = OptionMenu(uiElements.systemChoiceLabelFrame, info.systemChoice0, *systemOptions, command=lambda _: systemChoice(info.systemChoice0,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.systemChoiceMenu1 = OptionMenu(uiElements.systemChoiceLabelFrame, info.systemChoice1, *systemOptions, command=lambda _: systemChoice(info.systemChoice1,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.systemChoiceMenu2 = OptionMenu(uiElements.systemChoiceLabelFrame, info.systemChoice2, *systemOptions, command=lambda _: systemChoice(info.systemChoice2,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.systemChoiceMenu3 = OptionMenu(uiElements.systemChoiceLabelFrame, info.systemChoice3, *systemOptions, command=lambda _: systemChoice(info.systemChoice3,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.systemChoiceMenu4 = OptionMenu(uiElements.systemChoiceLabelFrame, info.systemChoice4, *systemOptions, command=lambda _: systemChoice(info.systemChoice4,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.systemChoiceMenu5 = OptionMenu(uiElements.systemChoiceLabelFrame, info.systemChoice5, *systemOptions, command=lambda _: systemChoice(info.systemChoice5,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.systemChoiceMenu6 = OptionMenu(uiElements.systemChoiceLabelFrame, info.systemChoice6, *systemOptions, command=lambda _: systemChoice(info.systemChoice6,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.systemChoiceMenu7 = OptionMenu(uiElements.systemChoiceLabelFrame, info.systemChoice7, *systemOptions, command=lambda _: systemChoice(info.systemChoice7,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
    
        systemChoice(info.systemChoice0,uiElements)
        systemChoice(info.systemChoice1,uiElements)
        systemChoice(info.systemChoice2,uiElements)
        systemChoice(info.systemChoice3,uiElements)
        systemChoice(info.systemChoice4,uiElements)
        systemChoice(info.systemChoice5,uiElements)
        systemChoice(info.systemChoice6,uiElements)
        systemChoice(info.systemChoice7,uiElements)

        (info.systemChoice0).set(systemOptions[0])
        (info.systemChoice1).set(systemOptions[0])
        (info.systemChoice2).set(systemOptions[0])
        (info.systemChoice2).set(systemOptions[0])
        (info.systemChoice3).set(systemOptions[0])
        (info.systemChoice4).set(systemOptions[0])
        (info.systemChoice5).set(systemOptions[0])
        (info.systemChoice6).set(systemOptions[0])
        (info.systemChoice7).set(systemOptions[0])
            
        uiElementsList.append(uiElements.systemChoiceMenu0)
        uiElementsList.append(uiElements.systemChoiceMenu1)
        uiElementsList.append(uiElements.systemChoiceMenu2)
        uiElementsList.append(uiElements.systemChoiceMenu3)
        uiElementsList.append(uiElements.systemChoiceMenu4)
        uiElementsList.append(uiElements.systemChoiceMenu5)
        uiElementsList.append(uiElements.systemChoiceMenu6)
        uiElementsList.append(uiElements.systemChoiceMenu7)

        uiElements.subsystemChoiceLabelFrame = tk.LabelFrame(root,width = uiMetrics.editorsystemsWidth,text = "Subsystems", height = 450)
        uiElementsList.append(uiElements.subsystemChoiceLabelFrame)

        uiElements.subsystemChoiceMenu0 = OptionMenu(uiElements.subsystemChoiceLabelFrame, info.subsystemChoice0, *subsystemOptions, command=lambda _: subsystemChoice(info.subsystemChoice0,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.subsystemChoiceMenu1 = OptionMenu(uiElements.subsystemChoiceLabelFrame, info.subsystemChoice1, *subsystemOptions, command=lambda _: subsystemChoice(info.subsystemChoice1,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.subsystemChoiceMenu2 = OptionMenu(uiElements.subsystemChoiceLabelFrame, info.subsystemChoice2, *subsystemOptions, command=lambda _: subsystemChoice(info.subsystemChoice2,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.subsystemChoiceMenu3 = OptionMenu(uiElements.subsystemChoiceLabelFrame, info.subsystemChoice3, *subsystemOptions, command=lambda _: subsystemChoice(info.subsystemChoice3,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.subsystemChoiceMenu4 = OptionMenu(uiElements.subsystemChoiceLabelFrame, info.subsystemChoice4, *subsystemOptions, command=lambda _: subsystemChoice(info.subsystemChoice4,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.subsystemChoiceMenu5 = OptionMenu(uiElements.subsystemChoiceLabelFrame, info.subsystemChoice5, *subsystemOptions, command=lambda _: subsystemChoice(info.subsystemChoice5,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.subsystemChoiceMenu6 = OptionMenu(uiElements.subsystemChoiceLabelFrame, info.subsystemChoice6, *subsystemOptions, command=lambda _: subsystemChoice(info.subsystemChoice6,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        uiElements.subsystemChoiceMenu7 = OptionMenu(uiElements.subsystemChoiceLabelFrame, info.subsystemChoice7, *subsystemOptions, command=lambda _: subsystemChoice(info.subsystemChoice7,uiElements.systemStatsLabelFrame,uiElements.shipStatsLabelFrame))
        
        subsystemChoice(info.subsystemChoice0,uiElements)
        subsystemChoice(info.subsystemChoice1,uiElements)
        subsystemChoice(info.subsystemChoice2,uiElements)
        subsystemChoice(info.subsystemChoice3,uiElements)
        subsystemChoice(info.subsystemChoice4,uiElements)
        subsystemChoice(info.subsystemChoice5,uiElements)
        subsystemChoice(info.subsystemChoice6,uiElements)
        subsystemChoice(info.subsystemChoice7,uiElements)

        (info.subsystemChoice0).set(subsystemOptions[0])
        (info.subsystemChoice1).set(subsystemOptions[0])
        (info.subsystemChoice2).set(subsystemOptions[0])
        (info.subsystemChoice2).set(subsystemOptions[0])
        (info.subsystemChoice3).set(subsystemOptions[0])
        (info.subsystemChoice4).set(subsystemOptions[0])
        (info.subsystemChoice5).set(subsystemOptions[0])
        (info.subsystemChoice6).set(subsystemOptions[0])
        (info.subsystemChoice7).set(subsystemOptions[0])

        uiElementsList.append(uiElements.subsystemChoiceMenu0)
        uiElementsList.append(uiElements.subsystemChoiceMenu1)
        uiElementsList.append(uiElements.subsystemChoiceMenu2)
        uiElementsList.append(uiElements.subsystemChoiceMenu3)
        uiElementsList.append(uiElements.subsystemChoiceMenu4)
        uiElementsList.append(uiElements.subsystemChoiceMenu5)
        uiElementsList.append(uiElements.subsystemChoiceMenu6)
        uiElementsList.append(uiElements.subsystemChoiceMenu7)


        uiElements.saveShipButton = Button(root, text="Save ship design", command = lambda: [saveShip(info,uiElements,filePath)],width=20,height=3)
        uiElements.completeButton = Button(root, text="Auto-complete ship", command = lambda: [completeShip(uiElements)],width=20,height=3)
        uiElements.clearButton = Button(root, text="Clear Design", command = lambda: [clearShip(uiElements)],width=20,height=3)
        uiElements.exitToMenuButton = tk.Button(root, text="Exit to menu", command=lambda:[placeMenuUi(menuUiElements,uiMetrics), hideEditorUi(uiElementsList)], width = 20, height= 7)

        uiElementsList.append(uiElements.saveShipButton)
        uiElementsList.append(uiElements.completeButton)
        uiElementsList.append(uiElements.clearButton)
        uiElementsList.append(uiElements.exitToMenuButton)
        (naglowek.shipEditorInfo).uiElements = uiElements
        (naglowek.shipEditorInfo).uiElementsList = uiElementsList
        naglowek.editorUiReady = True

    placeShipEditorUi((naglowek.shipEditorInfo).uiElements,uiMetrics)

    mainloop()