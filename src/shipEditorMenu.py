from functools import partial
from tkinter import *
import configparser
from functools import partial
import sys,os
from decimal import *
from pathlib import Path
import math
import tkinter.ttk as ttk
import tkinter as tk

import src.settings as settings
from src.rootCommands import placeMenuUi,hideMenuUi,placeShipEditorUi


def systemChoiceCommand(systemChoice,uiElements,label,info,slot):
    a = systemChoice.get()
    newSystem = (settings.systemStats)[a]
    oldSystemName = (info.ship).systemSlots[slot]
    oldSystem = (settings.systemStats)[oldSystemName]
    tmpText = "Mass: " + str(newSystem.mass)
    tmpText += ", Cost: " + str(newSystem.cost)
    label.config(text = tmpText)
    (oldSystem).onRemoving(info.ship)
    (info.ship).systemSlots[slot] = a
    newSystem.onAdding(info.ship)
    updateShipStats(uiElements,info)
    updateSystemStats(uiElements,newSystem)

def subsystemChoiceCommand(subsystemChoice,uiElements,label,info,slot):
    a = subsystemChoice.get()
    newSubsystem = (settings.subsystemStats)[a]
    oldSubsystemName = (info.ship).subsystemSlots[slot]
    oldSubsystem = (settings.subsystemStats)[oldSubsystemName]
    tmpText = "Mass: " + str(newSubsystem.mass)
    tmpText += ", Cost: " + str(newSubsystem.cost)
    label.config(text = tmpText)
    (oldSubsystem).onRemoving(info.ship)
    (info.ship).subsystemSlots[slot] = a
    newSubsystem.onAdding(info.ship)
    updateShipStats(uiElements,info)
    updateSystemStats(uiElements,newSubsystem)

def sign(number):
    if(number==0):
        return ' '
    elif(number>0):
        return ' ▲ ' + str(number)
    else:
        return ' ▼ ' + str(number)

def updateShipStats(uiElements,info):
    ship = info.ship
    # insert some clever formula with mass speed rotation etc
    ship.maxSpeed = round((ship.mainThrust + ship.directionalThrust)/(ship.mass*0.01),2)
    ship.turnRate = math.ceil((ship.directionalThrust)/(ship.mass*0.012))/100

    (info.shipDiff).hp = ship.hp - info.oldShip.hp
    (info.shipDiff).ap  = ship.ap - info.oldShip.ap
    (info.shipDiff).shields = ship.shields - info.oldShip.shields
    (info.shipDiff).maxShields = ship.maxShields - info.oldShip.maxShields
    (info.shipDiff).mass = ship.mass - info.oldShip.mass
    (info.shipDiff).cost = ship.cost - info.oldShip.cost
    (info.shipDiff).detectionRange = ship.detectionRange - info.oldShip.detectionRange
    (info.shipDiff).maxSpeed  = ship.maxSpeed - info.oldShip.maxSpeed
    (info.shipDiff).turnRate = ship.turnRate - info.oldShip.turnRate
    (info.shipDiff).maxEnergy = (info.ship).maxEnergy - info.oldShip.maxEnergy
    (info.shipDiff).minEnergyConsumption = ship.minEnergyConsumption - info.oldShip.minEnergyConsumption
    (info.shipDiff).maxEnergyConsumption = ship.maxEnergyConsumption - info.oldShip.maxEnergyConsumption
    (info.shipDiff).mainThrust = ship.mainThrust - info.oldShip.mainThrust
    (info.shipDiff).directionalThrust = ship.directionalThrust - info.oldShip.directionalThrust

    getcontext().prec = 2  
    getcontext().rounding = ROUND_UP
    (uiElements.shipStatsL).config(text = "{}{}\n{}{}\n{}{}\n{}{}\n\
{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}".format(
("Hull: " + str(round(ship.hp, 2))).ljust(30), sign(round((info.shipDiff).hp, 2)),
("Armor: " + str(round(ship.ap, 2))).ljust(30), sign(round((info.shipDiff).ap, 2)),
("Shields: " + str(round(ship.shields, 2))).ljust(30), sign(round((info.shipDiff).shields, 2)),
("Maximum shields: " + str(round(ship.maxShields, 2))).ljust(30), sign(round((info.shipDiff).maxShields, 2)),
("Range: " + str(round(ship.detectionRange, 2))).ljust(30), sign(round((info.shipDiff).detectionRange, 2)),
("Mass: " + str(round(ship.mass, 2))).ljust(30), sign(round((info.shipDiff).mass, 2)),
("Forward Thrust: " + str(round(ship.mainThrust, 2))).ljust(30), sign(round((info.shipDiff).mainThrust, 2)),
("Directional Thrust: " + str(round(ship.directionalThrust, 2))).ljust(30), sign(round((info.shipDiff).directionalThrust, 2)),
("Turn Rate: " + str(round(ship.turnRate, 2))).ljust(30), sign(round((info.shipDiff).turnRate, 2)),
("Max Speed: " + str(round(ship.maxSpeed, 2))).ljust(30), sign(round((info.shipDiff).maxSpeed, 0)),
("Max Energy: " + str(round(ship.maxEnergy, 2))).ljust(30), sign(round((info.shipDiff).maxEnergy, 2)),
("Minimum Energy Consumption: " + str(round(ship.minEnergyConsumption, 2))).ljust(30), sign(round((info.shipDiff).minEnergyConsumption, 2)),
("Maximum Energy Consumption: " + str(round(ship.maxEnergyConsumption, 2))).ljust(30), sign(round((info.shipDiff).maxEnergyConsumption, 2)),
("Cost total: " + str(round(ship.cost, 2))).ljust(30), sign(round((info.shipDiff).cost, 2)),
))

    (info.oldShip).hp = ship.hp
    (info.oldShip).ap = ship.ap
    (info.oldShip).shields = ship.shields
    (info.oldShip).maxShields = ship.shields # change if needed
    (info.oldShip).mass = ship.mass
    (info.oldShip).cost = ship.cost
    (info.oldShip).detectionRange = ship.detectionRange
    (info.oldShip).maxSpeed = ship.maxSpeed
    (info.oldShip).turnRate = ship.turnRate
    (info.oldShip).maxEnergy = ship.maxEnergy
    (info.oldShip).minEnergyConsumption = ship.minEnergyConsumption
    (info.oldShip).maxEnergyConsumption = ship.maxEnergyConsumption
    (info.oldShip).mainThrust = ship.mainThrust
    (info.oldShip).directionalThrust = ship.directionalThrust

def updateSystemStats(uiElements,subsystem):
    (uiElements.systemStatsL).config(text = subsystem.description)

def engineChoiceCommand(engineChoice,uiElements,label,info):
    a = engineChoice.get()
    oldEngineName = ((info.ship).engine)
    oldEngine = (settings.engineStats)[oldEngineName]
    newEngine = (settings.engineStats)[a]
    tmpText = "Mass: " + str(newEngine.mass)
    tmpText += " Cost: " + str(newEngine.cost)
    label.config(text = tmpText)
    (info.ship).engine = newEngine.name
    (oldEngine).onRemoving(info.ship)
    (info.ship).engine = a
    newEngine.onAdding(info.ship)
    updateShipStats(uiElements,info)
    updateSystemStats(uiElements,newEngine)

def thrustersChoiceCommand(thrustersChoice,uiElements,label,info):
    a = thrustersChoice.get()
    oldThrustersName = ((info.ship).thrusters)
    oldThrusters = (settings.thrustersStats)[oldThrustersName]
    newThrusters = (settings.thrustersStats)[a]
    tmpText = "Mass: " + str(newThrusters.mass)
    tmpText += ", Cost: " + str(newThrusters.cost)
    label.config(text = tmpText)
    (info.ship).thrusters = newThrusters.name
    (oldThrusters).onRemoving(info.ship)
    (info.ship).thrusters = a
    newThrusters.onAdding(info.ship)
    updateShipStats(uiElements,info)
    updateSystemStats(uiElements,newThrusters)

def radarChoiceCommand(radarChoice,uiElements,label,info):
    a = radarChoice.get()
    oldRadarName = ((info.ship).radar)
    oldRadar = (settings.radarStats)[oldRadarName]
    newRadar = (settings.radarStats)[a]
    tmpText = "Mass: " + str(newRadar.mass)
    tmpText += ", Cost: " + str(newRadar.cost)
    label.config(text = tmpText)
    (info.ship).radar = newRadar.name
    (oldRadar).onRemoving(info.ship)
    (info.ship).radar = a
    newRadar.onAdding(info.ship)
    updateShipStats(uiElements,info)
    updateSystemStats(uiElements,newRadar)

def generatorChoiceCommand(generatorChoice,uiElements,label,info):
    a = generatorChoice.get()
    oldGeneratorName = ((info.ship).generator)
    oldGenerator = (settings.generatorStats)[oldGeneratorName]
    newGenerator = (settings.generatorStats)[a]
    tmpText = "Mass: " + str(newGenerator.mass)
    tmpText += ", Cost: " + str(newGenerator.cost)
    label.config(text = tmpText)
    (info.ship).generator = newGenerator.name
    (oldGenerator).onRemoving(info.ship)
    (info.ship).generator = a
    newGenerator.onAdding(info.ship)
    updateShipStats(uiElements,info)
    updateSystemStats(uiElements,newGenerator)

def closeWindow(window):
    window.destroy()

def saveShip(info,uiElements,filePath, cp):
    shipName = str((uiElements.shipNameInput).get())
    if(info.engineChoice.get() == "none"):
        (uiElements.shipNameInput).delete(0, END)
        (uiElements.shipNameInput).insert(0, "Ship must have a Main Drive") 
    elif(info.thrustersChoice.get() == "none"):
        (uiElements.shipNameInput).delete(0, END)
        (uiElements.shipNameInput).insert(0, "Ship must have Thrusters") 
    elif(info.radarChoice.get() == "none"):
        (uiElements.shipNameInput).delete(0, END)
        (uiElements.shipNameInput).insert(0, "Ship must have Sensors") 
    elif(info.generatorChoice.get() == "none"):
        (uiElements.shipNameInput).delete(0, END)
        (uiElements.shipNameInput).insert(0, "Ship must have a Generator")
    elif(info.ship.maxEnergy  < 0):
        (uiElements.shipNameInput).delete(0, END)
        (uiElements.shipNameInput).insert(0, "Ship must have a positive energy balance")
    elif(not(len(shipName) == 0) and len(shipName) < 13):
        if(not cp.has_section(shipName)):
            cp.add_section(shipName)

        cp.set(shipName, "systemslots1",str((info.systemChoice0).get()))
        cp.set(shipName, "systemslots2",str((info.systemChoice1).get()))
        cp.set(shipName, "systemslots3",str((info.systemChoice2).get()))
        cp.set(shipName, "systemslots4",str((info.systemChoice3).get()))
        cp.set(shipName, "systemslots5",str((info.systemChoice4).get()))
        cp.set(shipName, "systemslots6",str((info.systemChoice5).get()))

        cp.set(shipName, "hp",str(((info.ship).hp)))
        cp.set(shipName, "ap",str(((info.ship).ap)))

        cp.set(shipName, "maxHp",str(((info.ship).hp)))
        cp.set(shipName, "maxAp",str(((info.ship).ap)))

        cp.set(shipName, "cost",str(((info.ship).cost)))
        cp.set(shipName, "mass",str(((info.ship).mass)))
        
        cp.set(shipName, "subsystemslots1",str((info.subsystemChoice1).get()))
        cp.set(shipName, "subsystemslots2",str((info.subsystemChoice2).get()))
        cp.set(shipName, "subsystemslots3",str((info.subsystemChoice3).get()))
        cp.set(shipName, "subsystemslots4",str((info.subsystemChoice4).get()))
        cp.set(shipName, "subsystemslots5",str((info.subsystemChoice5).get()))
        cp.set(shipName, "subsystemslots6",str((info.subsystemChoice6).get()))
        cp.set(shipName, "subsystemslots7",str((info.subsystemChoice7).get()))
        cp.set(shipName, "subsystemslots8",str((info.subsystemChoice8).get()))

        cp.set(shipName, "engine",str((info.engineChoice).get()))
        cp.set(shipName, "thrusters",str((info.thrustersChoice).get()))
        cp.set(shipName, "radar",str((info.radarChoice).get()))
        cp.set(shipName, "generator",str((info.generatorChoice).get()))
        cp.set(shipName, "owner","player1")

        cp.set(shipName, "shields",str((info.ship).shields))
        cp.set(shipName, "maxShields",str((info.ship).maxShields))
        cp.set(shipName, "energyLimit",str((info.ship).maxEnergy))
        cp.set(shipName, "detectionRange",str((info.ship).detectionRange))
        cp.set(shipName, "turnRate",str((info.ship).turnRate))
        cp.set(shipName, "maxSpeed",str((info.ship).maxSpeed))
        cp.set(shipName, "speed",str((info.ship).maxSpeed))
        cp.set(shipName, "stance",'rush')                           ####### change if designing ai ships
        cp.set(shipName, "color",'green')   

    #engine = engine1
    #thrusters = thrusters1
    #radar = radar1
    #powergenerator = powerGenerator1
    #detectionrange = 100
        cp.set(shipName, "shipName",shipName)
        hd = open(filePath, "w")
        cp.write(hd)
        hd.close()
        window = tk.Toplevel()
        window.config(bg="#1e1e1e")
        label = ttk.Label(window, style = 'Grey.TLabel', text=("'" + shipName + "' \n \n" + " saved successfully") )

        window.config(width = len(shipName) * 6 + 200,height = 200)
        closeWindowCommand = partial(closeWindow,window)


        frame = tk.Frame(window)
        frame.config(bg="#4582ec", width=2, height=2,padx=1)
        button = tk.Button(frame, text = "Ok",command=closeWindowCommand)
        button.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
    
        label.place(relx=0.5, rely=0.2,anchor=CENTER)
        frame.place(relx=0.5, rely=0.5,anchor=CENTER)
        button.pack()

    elif(len(shipName) < 13):
        (uiElements.shipNameInput).delete(0, END)
        (uiElements.shipNameInput).insert(0, "Ship must have a name. Insert the name to continue.") 
    else:
        (uiElements.shipNameInput).delete(0, END)
        (uiElements.shipNameInput).insert(0, "Ship name must be shorter than 13 characters") 


    """
    file = open(filePath)
    config.set(shipName, "playerName",shipName)
    config.write(file)
    file.close()"""

def completeShip(uiElements):
    x=10

def clearShip(info,uiElements):
    systemOptions = settings.allSystemsList
    subsystemOptions = settings.allSubsystemsList
    engineOptions = settings.allEnginesList
    thrustersOptions = settings.allThrustersList
    radarOptions = settings.allRadarsList
    generatorOptions = settings.allGeneratorsList

    info.engineChoice.set(engineOptions[0])
    info.thrustersChoice.set(thrustersOptions[0])
    info.radarChoice.set(radarOptions[0])
    info.generatorChoice.set(generatorOptions[0])

    info.subsystemChoice1.set(subsystemOptions[0])
    info.subsystemChoice2.set(subsystemOptions[0])
    info.subsystemChoice3.set(subsystemOptions[0])
    info.subsystemChoice4.set(subsystemOptions[0])
    info.subsystemChoice5.set(subsystemOptions[0])
    info.subsystemChoice6.set(subsystemOptions[0])
    info.subsystemChoice7.set(subsystemOptions[0])
    info.subsystemChoice8.set(subsystemOptions[0])

    info.systemChoice0.set(systemOptions[0])
    info.systemChoice1.set(systemOptions[0])
    info.systemChoice2.set(systemOptions[0])
    info.systemChoice3.set(systemOptions[0])
    info.systemChoice4.set(systemOptions[0])
    info.systemChoice5.set(systemOptions[0])
    zeroShip(info)
    updateShipStats(uiElements,info)

def zeroShip(info):  
    (info.ship).mass = 100
    (info.ship).cost = 0
    (info.ship).hp = 300
    (info.ship).ap = 300
    (info.ship).shields = 0
    (info.ship).maxShields = 0
    (info.ship).detectionRange = 0
    (info.ship).maxSpeed = 0
    (info.ship).turnRate = 0
    (info.ship).maxEnergy = 0
    (info.ship).minEnergyConsumption = 0
    (info.ship).maxEnergyConsumption = 0
    (info.ship).engine = "none"
    (info.ship).radar = "none"
    (info.ship).thrusters = "none"
    (info.ship).generator = "none"
    (info.ship).mainThrust = 0
    (info.ship).directionalThrust = 0

    (info.oldShip).mass = (info.ship).mass
    (info.oldShip).cost = (info.ship).cost
    (info.oldShip).hp = (info.ship).hp
    (info.oldShip).ap = (info.ship).ap
    (info.oldShip).shields = (info.ship).shields
    (info.oldShip).maxShields = (info.ship).maxShields
    (info.oldShip).detectionRange = (info.ship).detectionRange
    (info.oldShip).maxSpeed = (info.ship).maxSpeed
    (info.oldShip).turnRate = (info.ship).turnRate
    (info.oldShip).maxEnergy = (info.ship).maxEnergy
    (info.oldShip).minEnergyConsumption = (info.ship).minEnergyConsumption
    (info.oldShip).maxEnergyConsumption = (info.ship).maxEnergyConsumption
    (info.oldShip).engine = (info.ship).engine
    (info.oldShip).radar = (info.ship).radar
    (info.oldShip).thrusters = (info.ship).thrusters
    (info.oldShip).generator = (info.ship).generator
    (info.oldShip).mainThrust = (info.ship).mainThrust
    (info.oldShip).directionalThrust = (info.ship).directionalThrust      


def refreshSections(config):
    return config.sections()

def writeShipOption(info,uiElements):
  #  zeroShip(info)
    configIn = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    filePath = os.path.join(cwd, "gameData/customShips.ini")
    configIn.read(filePath)

    ship1 = info.optionChosen.get()
    info.engineChoice.set(configIn.get(ship1,"engine"))
    info.thrustersChoice.set(configIn.get(ship1,"thrusters"))
    info.radarChoice.set(configIn.get(ship1,"radar"))
    info.generatorChoice.set(configIn.get(ship1,"generator"))

    engineChoiceCommand(info.engineChoice,uiElements,uiElements.engineChoiceMenuL,info)
    thrustersChoiceCommand(info.thrustersChoice,uiElements,uiElements.thrustersChoiceMenuL,info)
    radarChoiceCommand(info.radarChoice,uiElements,uiElements.radarChoiceMenuL,info)
    generatorChoiceCommand(info.generatorChoice,uiElements,uiElements.generatorChoiceMenuL,info)

    info.shipName.set(ship1)

    info.subsystemChoice1.set(configIn.get(ship1,"subsystemSlots1"))
    info.subsystemChoice2.set(configIn.get(ship1,"subsystemSlots2"))
    info.subsystemChoice3.set(configIn.get(ship1,"subsystemSlots3"))
    info.subsystemChoice4.set(configIn.get(ship1,"subsystemSlots4"))
    info.subsystemChoice5.set(configIn.get(ship1,"subsystemSlots5"))
    info.subsystemChoice6.set(configIn.get(ship1,"subsystemSlots6"))
    info.subsystemChoice7.set(configIn.get(ship1,"subsystemSlots7"))
    info.subsystemChoice8.set(configIn.get(ship1,"subsystemSlots8"))

    subsystemChoiceCommand(info.subsystemChoice1,uiElements,uiElements.subsystemChoiceL1,info,0)
    subsystemChoiceCommand(info.subsystemChoice2,uiElements,uiElements.subsystemChoiceL2,info,1)
    subsystemChoiceCommand(info.subsystemChoice3,uiElements,uiElements.subsystemChoiceL3,info,2)
    subsystemChoiceCommand(info.subsystemChoice4,uiElements,uiElements.subsystemChoiceL4,info,3)
    subsystemChoiceCommand(info.subsystemChoice5,uiElements,uiElements.subsystemChoiceL5,info,4)
    subsystemChoiceCommand(info.subsystemChoice6,uiElements,uiElements.subsystemChoiceL6,info,5)
    subsystemChoiceCommand(info.subsystemChoice7,uiElements,uiElements.subsystemChoiceL7,info,6)
    subsystemChoiceCommand(info.subsystemChoice8,uiElements,uiElements.subsystemChoiceL8,info,7)

    info.systemChoice0.set(configIn.get(ship1,"systemSlots1"))
    info.systemChoice1.set(configIn.get(ship1,"systemSlots2"))
    info.systemChoice2.set(configIn.get(ship1,"systemSlots3"))
    info.systemChoice3.set(configIn.get(ship1,"systemSlots4"))
    info.systemChoice4.set(configIn.get(ship1,"systemSlots5"))
    info.systemChoice5.set(configIn.get(ship1,"systemSlots6"))   
    
    
    systemChoiceCommand(info.systemChoice0,uiElements,uiElements.systemChoiceL0,info,0)
    systemChoiceCommand(info.systemChoice1,uiElements,uiElements.systemChoiceL1,info,1)
    systemChoiceCommand(info.systemChoice2,uiElements,uiElements.systemChoiceL2,info,2)
    systemChoiceCommand(info.systemChoice3,uiElements,uiElements.systemChoiceL3,info,3)
    systemChoiceCommand(info.systemChoice4,uiElements,uiElements.systemChoiceL4,info,4)
    systemChoiceCommand(info.systemChoice5,uiElements,uiElements.systemChoiceL5,info,5)
           

    updateShipStats(uiElements,info)

def shipEditor(root,config,uiMenuElements,uiMetrics,menuUiElements):
    root.title("Ship Editor")
    if(not settings.editorUiReady):
        config = configparser.ConfigParser()
        cwd = Path(sys.argv[0])
        cwd = str(cwd.parent)
        filePath = os.path.join(cwd, "gameData/customShips.ini")
        config.read(filePath)
        
        shipOptions = config.sections()
        systemOptions = settings.allSystemsList
        subsystemOptions = settings.allSubsystemsList
        engineOptions = settings.allEnginesList
        thrustersOptions = settings.allThrustersList
        radarOptions = settings.allRadarsList
        generatorOptions = settings.allGeneratorsList

        uiElementsList = []
        uiElements = settings.dynamic_object()              # change colors and fonts accordingly
        systemOptions = settings.allSystemsList
        uiElements.systemStatsLF = ttk.Labelframe(root, style = 'NonSerifBlueConsolas.TLabelframe', text = "Recently changed element:",width = uiMetrics.shipStatsLFWidth,height = uiMetrics.shipStatsLFHeight)
        uiElements.systemStatsL = ttk.Label(uiElements.systemStatsLF, style = 'NonSerif.TLabel',justify = "left", text = "Choose any ship element")
       
        uiElements.shipStatsLF = ttk.Labelframe(root, style = 'NonSerifBlueConsolas.TLabelframe', text = "Ship statistics:",width = uiMetrics.shipStatsLFWidth,height = uiMetrics.shipStatsLFHeight)
        uiElements.shipStatsL = ttk.Label(uiElements.shipStatsLF, style = 'NonSerif.TLabel', justify = "left", text = 
        "Hull: 100 \n \
        Armor: 100 \n \
        Mass: 200t \n \
        Cost: 0 \n \
        Sensors Range: 0 \n \
        Max Speed: 0 \n \
        RotationSpeed: 0 \n \
        Max Energy: 0 \n \
        Minimum Energy Consumption: 0 \n \
        Maximum Energy Consumption: 0") 


        info = settings.shipEditorInfo
        info.shipName = StringVar()

        uiElements.shipNameInput = tk.Entry(root,width = 50, text = info.shipName)

        options = refreshSections(config)
        info.optionChosen = StringVar()
        info.optionChosen.set(options[0])
        uiElements.shipChoice = tk.OptionMenu(root,info.optionChosen,options[0], *options, command=lambda _: writeShipOption(info,uiElements))
        uiElements.shipChoice.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")

        uiElementsList.append(uiElements.shipChoice)
        uiElementsList.append(uiElements.shipNameInput)
        uiElementsList.append(uiElements.systemStatsLF)
        uiElementsList.append(uiElements.systemStatsL)
        uiElementsList.append(uiElements.shipStatsLF)
        uiElementsList.append(uiElements.shipStatsL)


        (info.ship) = settings.dynamic_object()   
        info.shipDiff = settings.dynamic_object()
        info.oldShip = settings.dynamic_object()
        tmp = 8     
        (info.ship).systemSlots = []     
        (info.ship).subsystemSlots = []   
        while(tmp > 0):
            ((info.ship).systemSlots).append("none")
            ((info.ship).subsystemSlots).append("none")
            tmp-=1     
        zeroShip(info)

        info.engineChoice = StringVar(root)
        info.thrustersChoice = StringVar(root)
        info.radarChoice = StringVar(root)
        info.generatorChoice = StringVar(root)

        uiElements.engineChoiceMenuLF = ttk.Labelframe(root, style = 'NonSerifBlue.TLabelframe', text = "Main Drive", width = uiMetrics.editorChoiceMenuLFWidth, height = uiMetrics.editorChoiceMenuLFHeight)
        uiElements.thrustersChoiceMenuLF = ttk.Labelframe(root, style = 'NonSerifBlue.TLabelframe', text = "Thrusters", width = uiMetrics.editorChoiceMenuLFWidth, height = uiMetrics.editorChoiceMenuLFHeight)
        uiElements.radarChoiceMenuLF = ttk.Labelframe(root, style = 'NonSerifBlue.TLabelframe', text = "Sensors", width = uiMetrics.editorChoiceMenuLFWidth, height = uiMetrics.editorChoiceMenuLFHeight)
        uiElements.generatorChoiceMenuLF = ttk.Labelframe(root,style = 'NonSerifBlue.TLabelframe', text = "Power Generator", width = uiMetrics.editorChoiceMenuLFWidth, height = uiMetrics.editorChoiceMenuLFHeight)

        uiElements.engineChoiceMenuL = tk.Label(uiElements.engineChoiceMenuLF, text = "Mass: 0, Cost: 0",)
        uiElements.thrustersChoiceMenuL = tk.Label(uiElements.thrustersChoiceMenuLF, text = "Mass: 0, Cost: 0")
        uiElements.radarChoiceMenuL = tk.Label(uiElements.radarChoiceMenuLF, text = "Mass: 0, Cost: 0")
        uiElements.generatorChoiceMenuL = tk.Label(uiElements.generatorChoiceMenuLF, text = "Mass: 0, Cost: 0")

        uiElementsList.append(uiElements.engineChoiceMenuLF)
        uiElementsList.append(uiElements.thrustersChoiceMenuLF)
        uiElementsList.append(uiElements.radarChoiceMenuLF)
        uiElementsList.append(uiElements.generatorChoiceMenuLF)


        info.engineChoice.set(engineOptions[0])
        info.thrustersChoice.set(thrustersOptions[0])
        info.radarChoice.set(radarOptions[0])
        info.generatorChoice.set(generatorOptions[0])

        uiElements.engineChoiceMenu =  tk.OptionMenu(uiElements.engineChoiceMenuLF,info.engineChoice,engineOptions[0], *engineOptions,  command=lambda _: engineChoiceCommand(info.engineChoice,uiElements,uiElements.engineChoiceMenuL,info))
        uiElements.thrustersChoiceMenu = tk.OptionMenu(uiElements.thrustersChoiceMenuLF,info.thrustersChoice,thrustersOptions[0],*thrustersOptions,  command=lambda _: thrustersChoiceCommand(info.thrustersChoice,uiElements,uiElements.thrustersChoiceMenuL,info))
        uiElements.radarChoiceMenu = tk.OptionMenu(uiElements.radarChoiceMenuLF,info.radarChoice,radarOptions[0], *radarOptions, command=lambda _: radarChoiceCommand(info.radarChoice,uiElements,uiElements.radarChoiceMenuL,info))
        uiElements.generatorChoiceMenu = tk.OptionMenu(uiElements.generatorChoiceMenuLF,info.generatorChoice,generatorOptions[0], *generatorOptions, command=lambda _: generatorChoiceCommand(info.generatorChoice,uiElements,uiElements.generatorChoiceMenuL,info))
    
        uiElements.engineChoiceMenu.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.thrustersChoiceMenu.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.radarChoiceMenu.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.generatorChoiceMenu.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        
        uiElements.engineChoiceMenuL.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.thrustersChoiceMenuL.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.radarChoiceMenuL.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.generatorChoiceMenuL.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        
        
        
        
        engineChoiceCommand(info.engineChoice,uiElements,uiElements.engineChoiceMenuL,info)
        thrustersChoiceCommand(info.thrustersChoice,uiElements,uiElements.thrustersChoiceMenuL,info)
        radarChoiceCommand(info.radarChoice,uiElements,uiElements.radarChoiceMenuL,info)
        generatorChoiceCommand(info.generatorChoice,uiElements,uiElements.generatorChoiceMenuL,info)

        uiElementsList.append(uiElements.engineChoiceMenu)
        uiElementsList.append(uiElements.thrustersChoiceMenu)
        uiElementsList.append(uiElements.radarChoiceMenu)
        uiElementsList.append(uiElements.generatorChoiceMenu)


        info.systemChoice0 = StringVar(root)
        info.systemChoice1 = StringVar(root)
        info.systemChoice2 = StringVar(root)
        info.systemChoice3 = StringVar(root)
        info.systemChoice4 = StringVar(root)
        info.systemChoice5 = StringVar(root)

        info.systemChoice0.set(systemOptions[0])
        info.systemChoice1.set(systemOptions[0])
        info.systemChoice2.set(systemOptions[0])
        info.systemChoice3.set(systemOptions[0])
        info.systemChoice4.set(systemOptions[0])
        info.systemChoice5.set(systemOptions[0])

        info.subsystemChoice1 = StringVar(root)
        info.subsystemChoice2 = StringVar(root)
        info.subsystemChoice3 = StringVar(root)
        info.subsystemChoice4 = StringVar(root)
        info.subsystemChoice5 = StringVar(root)
        info.subsystemChoice6 = StringVar(root)
        info.subsystemChoice7 = StringVar(root)
        info.subsystemChoice8 = StringVar(root)

        info.subsystemChoice1.set(subsystemOptions[0])
        info.subsystemChoice2.set(subsystemOptions[0])
        info.subsystemChoice3.set(subsystemOptions[0])
        info.subsystemChoice4.set(subsystemOptions[0])
        info.subsystemChoice5.set(subsystemOptions[0])
        info.subsystemChoice6.set(subsystemOptions[0])
        info.subsystemChoice7.set(subsystemOptions[0])
        info.subsystemChoice8.set(subsystemOptions[0])

        uiElements.systemChoiceLF = ttk.Labelframe(root, style = 'NonSerifBlue.TLabelframe',width = uiMetrics.editorSystemsWidth,text = "Systems (optional)", height = 450)
        uiElementsList.append(uiElements.systemChoiceLF)


        uiElements.systemChoiceMenu0 = tk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice0, systemOptions[0], *systemOptions,  command=lambda _: systemChoiceCommand(info.systemChoice0,uiElements,uiElements.systemChoiceL0,info,0))
        uiElements.systemChoiceMenu1 = tk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice1, systemOptions[0], *systemOptions,  command=lambda _: systemChoiceCommand(info.systemChoice1,uiElements,uiElements.systemChoiceL1,info,1))
        uiElements.systemChoiceMenu2 = tk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice2, systemOptions[0], *systemOptions,  command=lambda _: systemChoiceCommand(info.systemChoice2,uiElements,uiElements.systemChoiceL2,info,2))
        uiElements.systemChoiceMenu3 = tk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice3, systemOptions[0], *systemOptions,  command=lambda _: systemChoiceCommand(info.systemChoice3,uiElements,uiElements.systemChoiceL3,info,3))
        uiElements.systemChoiceMenu4 = tk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice4, systemOptions[0], *systemOptions,  command=lambda _: systemChoiceCommand(info.systemChoice4,uiElements,uiElements.systemChoiceL4,info,4))
        uiElements.systemChoiceMenu5 = tk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice5, systemOptions[0], *systemOptions,  command=lambda _: systemChoiceCommand(info.systemChoice5,uiElements,uiElements.systemChoiceL5,info,5))
 
        uiElements.systemChoiceMenu0.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.systemChoiceMenu1.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.systemChoiceMenu2.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.systemChoiceMenu3.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.systemChoiceMenu4.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.systemChoiceMenu5.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")

        uiElements.systemChoiceL0 = tk.Label(uiElements.systemChoiceLF, text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL1 = tk.Label(uiElements.systemChoiceLF, text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL2 = tk.Label(uiElements.systemChoiceLF, text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL3 = tk.Label(uiElements.systemChoiceLF, text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL4 = tk.Label(uiElements.systemChoiceLF, text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL5 = tk.Label(uiElements.systemChoiceLF, text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL6 = tk.Label(uiElements.systemChoiceLF, text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL7 = tk.Label(uiElements.systemChoiceLF, text = "Mass: 0, Cost: 0")

        uiElements.systemChoiceL0.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.systemChoiceL1.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.systemChoiceL2.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.systemChoiceL3.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.systemChoiceL4.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.systemChoiceL5.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.systemChoiceL6.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.systemChoiceL7.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        

        systemChoiceCommand(info.systemChoice0,uiElements,uiElements.systemChoiceL0,info,0) 
        systemChoiceCommand(info.systemChoice1,uiElements,uiElements.systemChoiceL1,info,1)
        systemChoiceCommand(info.systemChoice2,uiElements,uiElements.systemChoiceL2,info,2)
        systemChoiceCommand(info.systemChoice3,uiElements,uiElements.systemChoiceL3,info,3)
        systemChoiceCommand(info.systemChoice4,uiElements,uiElements.systemChoiceL4,info,4)
        systemChoiceCommand(info.systemChoice5,uiElements,uiElements.systemChoiceL5,info,5)
            
        uiElementsList.append(uiElements.systemChoiceMenu0)
        uiElementsList.append(uiElements.systemChoiceMenu1)
        uiElementsList.append(uiElements.systemChoiceMenu2)
        uiElementsList.append(uiElements.systemChoiceMenu3)
        uiElementsList.append(uiElements.systemChoiceMenu4)
        uiElementsList.append(uiElements.systemChoiceMenu5)

        uiElementsList.append(uiElements.systemChoiceL0)
        uiElementsList.append(uiElements.systemChoiceL1)
        uiElementsList.append(uiElements.systemChoiceL2)
        uiElementsList.append(uiElements.systemChoiceL3)
        uiElementsList.append(uiElements.systemChoiceL4)
        uiElementsList.append(uiElements.systemChoiceL5)

        uiElements.subsystemChoiceLF = ttk.Labelframe(root, style = 'NonSerifBlue.TLabelframe',width = uiMetrics.editorSystemsWidth,text = "Subsystems (optional)", height = 450)
        uiElementsList.append(uiElements.subsystemChoiceLF)

        uiElements.subsystemChoiceL1 = tk.Label(uiElements.subsystemChoiceLF,text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL2 = tk.Label(uiElements.subsystemChoiceLF,text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL3 = tk.Label(uiElements.subsystemChoiceLF,text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL4 = tk.Label(uiElements.subsystemChoiceLF,text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL5 = tk.Label(uiElements.subsystemChoiceLF,text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL6 = tk.Label(uiElements.subsystemChoiceLF,text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL7 = tk.Label(uiElements.subsystemChoiceLF,text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL8 = tk.Label(uiElements.subsystemChoiceLF,text = "Mass: 0, Cost: 0")

        uiElements.subsystemChoiceL1.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.subsystemChoiceL2.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.subsystemChoiceL3.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.subsystemChoiceL4.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.subsystemChoiceL5.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.subsystemChoiceL6.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.subsystemChoiceL7.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))
        uiElements.subsystemChoiceL8.config(background='#1e1e1e',fg="white", font=('Calibri 11 normal'))

        subsystemChoiceCommand(info.subsystemChoice1,uiElements,uiElements.subsystemChoiceL1,info,0)
        subsystemChoiceCommand(info.subsystemChoice2,uiElements,uiElements.subsystemChoiceL2,info,1)
        subsystemChoiceCommand(info.subsystemChoice3,uiElements,uiElements.subsystemChoiceL3,info,2)
        subsystemChoiceCommand(info.subsystemChoice4,uiElements,uiElements.subsystemChoiceL4,info,3)
        subsystemChoiceCommand(info.subsystemChoice5,uiElements,uiElements.subsystemChoiceL5,info,4)
        subsystemChoiceCommand(info.subsystemChoice6,uiElements,uiElements.subsystemChoiceL6,info,5)
        subsystemChoiceCommand(info.subsystemChoice7,uiElements,uiElements.subsystemChoiceL7,info,6)
        subsystemChoiceCommand(info.subsystemChoice8,uiElements,uiElements.subsystemChoiceL8,info,7)

        uiElements.subsystemChoiceMenu1 = tk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice1, subsystemOptions[0], *subsystemOptions, command=lambda _: subsystemChoiceCommand(info.subsystemChoice1,uiElements,uiElements.subsystemChoiceL1,info,0))
        uiElements.subsystemChoiceMenu2 = tk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice2, subsystemOptions[0], *subsystemOptions, command=lambda _: subsystemChoiceCommand(info.subsystemChoice2,uiElements,uiElements.subsystemChoiceL2,info,1))
        uiElements.subsystemChoiceMenu3 = tk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice3, subsystemOptions[0], *subsystemOptions, command=lambda _: subsystemChoiceCommand(info.subsystemChoice3,uiElements,uiElements.subsystemChoiceL3,info,2))
        uiElements.subsystemChoiceMenu4 = tk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice4, subsystemOptions[0], *subsystemOptions, command=lambda _: subsystemChoiceCommand(info.subsystemChoice4,uiElements,uiElements.subsystemChoiceL4,info,3))
        uiElements.subsystemChoiceMenu5 = tk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice5, subsystemOptions[0], *subsystemOptions, command=lambda _: subsystemChoiceCommand(info.subsystemChoice5,uiElements,uiElements.subsystemChoiceL5,info,4))
        uiElements.subsystemChoiceMenu6 = tk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice6, subsystemOptions[0], *subsystemOptions, command=lambda _: subsystemChoiceCommand(info.subsystemChoice6,uiElements,uiElements.subsystemChoiceL6,info,5))
        uiElements.subsystemChoiceMenu7 = tk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice7, subsystemOptions[0], *subsystemOptions, command=lambda _: subsystemChoiceCommand(info.subsystemChoice7,uiElements,uiElements.subsystemChoiceL7,info,6))
        uiElements.subsystemChoiceMenu8 = tk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice8, subsystemOptions[0], *subsystemOptions, command=lambda _: subsystemChoiceCommand(info.subsystemChoice8,uiElements,uiElements.subsystemChoiceL8,info,7))

        uiElements.subsystemChoiceMenu1.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.subsystemChoiceMenu2.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.subsystemChoiceMenu3.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.subsystemChoiceMenu4.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.subsystemChoiceMenu5.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.subsystemChoiceMenu6.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.subsystemChoiceMenu7.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.subsystemChoiceMenu8.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")

        uiElementsList.append(uiElements.subsystemChoiceMenu1)
        uiElementsList.append(uiElements.subsystemChoiceMenu2)
        uiElementsList.append(uiElements.subsystemChoiceMenu3)
        uiElementsList.append(uiElements.subsystemChoiceMenu4)
        uiElementsList.append(uiElements.subsystemChoiceMenu5)
        uiElementsList.append(uiElements.subsystemChoiceMenu6)
        uiElementsList.append(uiElements.subsystemChoiceMenu7)
        uiElementsList.append(uiElements.subsystemChoiceMenu8)

        uiElementsList.append(uiElements.subsystemChoiceL1)
        uiElementsList.append(uiElements.subsystemChoiceL2)
        uiElementsList.append(uiElements.subsystemChoiceL3)
        uiElementsList.append(uiElements.subsystemChoiceL4)
        uiElementsList.append(uiElements.subsystemChoiceL5)
        uiElementsList.append(uiElements.subsystemChoiceL6)
        uiElementsList.append(uiElements.subsystemChoiceL7)
        uiElementsList.append(uiElements.subsystemChoiceL8)

        uiElements.saveShipButtonF = tk.Frame(root)
        uiElements.completeButtonF = tk.Frame(root)
        uiElements.clearButtonF = tk.Frame(root)
        uiElements.exitToMenuButtonF = tk.Frame(root)
            
        uiElements.saveShipButtonF.config(bg="#4582ec", width=2, height=2,padx=1)
        uiElements.completeButtonF.config(bg="#4582ec", width=2, height=2,padx=1)
        uiElements.clearButtonF.config(bg="#4582ec", width=2, height=2,padx=1)
        uiElements.exitToMenuButtonF.config(bg="#4582ec", width=2, height=2,padx=1)

        uiElements.saveShipButton = tk.Button(uiElements.saveShipButtonF, width = 20, height = 2, text="Save ship design", command = lambda: [saveShip(info,uiElements,filePath,config)])
        uiElements.completeButton = tk.Button(uiElements.completeButtonF, width = 20, height = 2, text="Auto-complete ship", command = lambda: [completeShip(uiElements)], state = DISABLED)
        uiElements.clearButton = tk.Button(uiElements.clearButtonF, width = 20, height = 2,  text="Clear Design", command = lambda: [clearShip(info,uiElements)])
        uiElements.exitToMenuButton = tk.Button(uiElements.exitToMenuButtonF, width = 20, height = 2, text="Exit to menu", command=lambda:[placeMenuUi(root,menuUiElements,uiMetrics), hideMenuUi(uiElementsList)])
        
        uiElements.saveShipButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
        uiElements.completeButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
        uiElements.clearButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
        uiElements.exitToMenuButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
        
        uiElementsList.append(uiElements.saveShipButton)
        uiElementsList.append(uiElements.completeButton)
        uiElementsList.append(uiElements.clearButton)
        uiElementsList.append(uiElements.exitToMenuButton)
        uiElementsList.append(uiElements.saveShipButtonF)
        uiElementsList.append(uiElements.completeButtonF)
        uiElementsList.append(uiElements.clearButtonF)
        uiElementsList.append(uiElements.exitToMenuButtonF)

        (settings.shipEditorInfo).uiElements = uiElements
        (settings.shipEditorInfo).uiElementsList = uiElementsList
        clearShip(info,uiElements)
        settings.editorUiReady = True

    placeShipEditorUi((settings.shipEditorInfo).uiElements,uiMetrics)
    mainloop()