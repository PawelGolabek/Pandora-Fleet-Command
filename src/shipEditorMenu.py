from functools import partial
from tkinter import *
import configparser
from functools import partial
import sys,os
from decimal import *
from pathlib import Path

import src.naglowek as naglowek
from src.rootCommands import *


def systemChoiceCommand(systemChoice,uiElements,label,info,slot):
    a = systemChoice.get()
    newSystem = (naglowek.systemStats)[a]
    oldSystemName = (info.ship).systemSlots[slot]
    oldSystem = (naglowek.systemStats)[oldSystemName]
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
    newSubsystem = (naglowek.subsystemStats)[a]
    oldSubsystemName = (info.ship).subsystemSlots[slot]
    oldSubsystem = (naglowek.subsystemStats)[oldSubsystemName]
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
    ship.maxSpeed = round((ship.mainThrust + ship.directionalThrust)/(ship.mass*0.005),2)

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
    (uiElements.shipStatsL).config(text = "Hull: {}{} \n Armor: {}{} \n Shields: {}{}\n Maximum shields: {}{}\n\
 Sensors Range: {}{} \n Mass: {}{}t  \n Forward Thrust: {}{}  \n Directional Thrust: {}{} \n RotationSpeed: {}{}/s \n Max Speed: {}{} \n Max Energy: {}{} \n Minimum Energy Consumption: {}{} \n Maximum Energy Consumption: {}{}\n Cost total: {}{}".format(
    round(ship.hp, 2), sign(round((info.shipDiff).hp, 2)),
    round(ship.ap, 2), sign(round((info.shipDiff).ap, 2)),
    round(ship.shields, 2), sign(round((info.shipDiff).shields, 2)),
    round(ship.maxShields, 2), sign(round((info.shipDiff).maxShields, 2)),
    round(ship.detectionRange, 2), sign(round((info.shipDiff).detectionRange, 2)),
    round(ship.mass, 2), sign(round((info.shipDiff).mass, 2)),
    round(ship.mainThrust, 2), sign(round((info.shipDiff).mainThrust, 2)),
    round(ship.directionalThrust, 2), sign(round((info.shipDiff).directionalThrust, 2)),
    round(ship.turnRate, 2), sign(round((info.shipDiff).turnRate, 2)),
    round(ship.maxSpeed, 2), sign(round((info.shipDiff).maxSpeed, 2)),
    round(ship.maxEnergy, 2), sign(round((info.shipDiff).maxEnergy, 2)),
    round(ship.minEnergyConsumption, 2), sign(round((info.shipDiff).minEnergyConsumption, 2)),
    round(ship.maxEnergyConsumption, 2), sign(round((info.shipDiff).maxEnergyConsumption, 2)),
    round(ship.cost, 2), sign(round((info.shipDiff).cost, 2)),
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
    oldEngine = (naglowek.engineStats)[oldEngineName]
    newEngine = (naglowek.engineStats)[a]
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
    oldThrusters = (naglowek.thrustersStats)[oldThrustersName]
    newThrusters = (naglowek.thrustersStats)[a]
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
    oldRadar = (naglowek.radarStats)[oldRadarName]
    newRadar = (naglowek.radarStats)[a]
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
    oldGenerator = (naglowek.generatorStats)[oldGeneratorName]
    newGenerator = (naglowek.generatorStats)[a]
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
    elif(not(len(shipName) == 0) and len(shipName) < 13):
        if(not cp.has_section(shipName)):
            cp.add_section(shipName)

        cp.set(shipName, "systemslots1",str((info.systemChoice0).get()))
        cp.set(shipName, "systemslots2",str((info.systemChoice1).get()))
        cp.set(shipName, "systemslots3",str((info.systemChoice2).get()))
        cp.set(shipName, "systemslots4",str((info.systemChoice3).get()))
        cp.set(shipName, "systemslots5",str((info.systemChoice4).get()))
        cp.set(shipName, "systemslots6",str((info.systemChoice5).get()))
        
        cp.set(shipName, "subsystemslots1",str((info.subsystemChoice0).get()))
        cp.set(shipName, "subsystemslots2",str((info.subsystemChoice1).get()))
        cp.set(shipName, "subsystemslots3",str((info.subsystemChoice2).get()))
        cp.set(shipName, "subsystemslots4",str((info.subsystemChoice3).get()))
        cp.set(shipName, "subsystemslots5",str((info.subsystemChoice4).get()))
        cp.set(shipName, "subsystemslots6",str((info.subsystemChoice5).get()))

        cp.set(shipName, "engine",str((info.engineChoice).get()))
        cp.set(shipName, "thrusters",str((info.thrustersChoice).get()))
        cp.set(shipName, "radar",str((info.radarChoice).get()))
        cp.set(shipName, "engine",str((info.generatorChoice).get()))
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
        window.config(bg="#202020")
        label = ttk.Label(window, style = 'Grey.TLabel', text=("'" + shipName + "' \n \n" + " saved successfully") )

        window.config(width = len(shipName) * 6 + 200,height = 200)
        closeWindowCommand = partial(closeWindow,window)
        button = ttk.Button(window,style = 'Grey.TButton', text = "Ok",command=closeWindowCommand)
        label.place(relx=0.5, rely=0.2,anchor=CENTER)
        button.place(relx=0.5, rely=0.5,anchor=CENTER)
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
    systemOptions = naglowek.allSystemsList
    subsystemOptions = naglowek.allSubsystemsList
    engineOptions = naglowek.allEnginesList
    thrustersOptions = naglowek.allThrustersList
    radarOptions = naglowek.allRadarsList
    generatorOptions = naglowek.allGeneratorsList

    info.engineChoice.set(engineOptions[0])
    info.thrustersChoice.set(thrustersOptions[0])
    info.radarChoice.set(radarOptions[0])
    info.generatorChoice.set(generatorOptions[0])

    info.subsystemChoice0.set(subsystemOptions[0])
    info.subsystemChoice1.set(subsystemOptions[0])
    info.subsystemChoice2.set(subsystemOptions[0])
    info.subsystemChoice3.set(subsystemOptions[0])
    info.subsystemChoice4.set(subsystemOptions[0])
    info.subsystemChoice5.set(subsystemOptions[0])
    info.subsystemChoice6.set(subsystemOptions[0])
    info.subsystemChoice7.set(subsystemOptions[0])

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
    (info.ship).hp = 100
    (info.ship).ap = 100
    (info.ship).shields = 0
    (info.ship).maxShields = 0
    (info.ship).detectionRange = 100
    (info.ship).maxSpeed = 0
    (info.ship).turnRate = 0.3
    (info.ship).maxEnergy = 10
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


def shipEditor(root,config,uiMenuElements,uiMetrics,menuUiElements):
    root.title("Ship Editor")
    if(not naglowek.editorUiReady):
        config = configparser.ConfigParser()
        cwd = Path(sys.argv[0])
        cwd = str(cwd.parent)
        filePath = os.path.join(cwd, "gameData/customShips.ini")
        config.read(filePath)
        
        shipOptions = config.sections()
        systemOptions = naglowek.allSystemsList
        subsystemOptions = naglowek.allSubsystemsList
        engineOptions = naglowek.allEnginesList
        thrustersOptions = naglowek.allThrustersList
        radarOptions = naglowek.allRadarsList
        generatorOptions = naglowek.allGeneratorsList

        uiElementsList = []
        uiElements = naglowek.dynamic_object()
        systemOptions = naglowek.allSystemsList
        uiElements.systemStatsLF = ttk.Labelframe(root, style = 'Grey.TLabelframe', text = "Recently changed element:",width = uiMetrics.shipStatsLFWidth,height = uiMetrics.shipStatsLFHeight)
        uiElements.systemStatsL = ttk.Label(uiElements.systemStatsLF, style = 'Grey.TLabel',justify = "left", text = "Choose any ship element")
        uiElements.shipStatsLF = ttk.Labelframe(root, style = 'Grey.TLabelframe', text = "Ship statistics:",width = uiMetrics.shipStatsLFWidth,height = uiMetrics.shipStatsLFHeight)
        uiElements.shipStatsL = ttk.Label(uiElements.shipStatsLF, style = 'Grey.TLabel', justify = "left", text = 
        "Hull: 100 \n \
        Armor: 100 \n \
        Mass: 200t \n \
        Cost: 0 \n \
        Sensors Range: 200 \n \
        Max Speed: 70 \n \
        RotationSpeed: 0.3/s \n \
        Max Energy: 20 \n \
        Minimum Energy Consumption: 5 \n \
        Maximum Energy Consumption: 35")
        uiElements.shipNameInput = tk.Entry(root,width = 50)

        uiElementsList.append(uiElements.shipNameInput)
        uiElementsList.append(uiElements.systemStatsLF)
        uiElementsList.append(uiElements.systemStatsL)
        uiElementsList.append(uiElements.shipStatsLF)
        uiElementsList.append(uiElements.shipStatsL)

        info = naglowek.shipEditorInfo

        (info.ship) = naglowek.dynamic_object()   
        info.shipDiff = naglowek.dynamic_object()
        info.oldShip = naglowek.dynamic_object()
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

        uiElements.engineChoiceMenuLF = ttk.Labelframe(root, style = 'Grey.TLabelframe', text = "Main Drive", width = uiMetrics.editorChoiceMenuLFWidth, height = uiMetrics.editorChoiceMenuLFHeight)
        uiElements.thrustersChoiceMenuLF = ttk.Labelframe(root, style = 'Grey.TLabelframe', text = "Thrusters", width = uiMetrics.editorChoiceMenuLFWidth, height = uiMetrics.editorChoiceMenuLFHeight)
        uiElements.radarChoiceMenuLF = ttk.Labelframe(root, style = 'Grey.TLabelframe', text = "Sensors", width = uiMetrics.editorChoiceMenuLFWidth, height = uiMetrics.editorChoiceMenuLFHeight)
        uiElements.generatorChoiceMenuLF = ttk.Labelframe(root,style = 'Grey.TLabelframe', text = "Power Generator", width = uiMetrics.editorChoiceMenuLFWidth, height = uiMetrics.editorChoiceMenuLFHeight)

        uiElements.engineChoiceMenuL = ttk.Label(uiElements.engineChoiceMenuLF, style = 'Grey.TLabel', text = "Mass: 0, Cost: 0",)
        uiElements.thrustersChoiceMenuL = ttk.Label(uiElements.thrustersChoiceMenuLF, style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.radarChoiceMenuL = ttk.Label(uiElements.radarChoiceMenuLF, style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.generatorChoiceMenuL = ttk.Label(uiElements.generatorChoiceMenuLF, style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")

        uiElementsList.append(uiElements.engineChoiceMenuLF)
        uiElementsList.append(uiElements.thrustersChoiceMenuLF)
        uiElementsList.append(uiElements.radarChoiceMenuLF)
        uiElementsList.append(uiElements.generatorChoiceMenuLF)


        info.engineChoice.set(engineOptions[0])
        info.thrustersChoice.set(thrustersOptions[0])
        info.radarChoice.set(radarOptions[0])
        info.generatorChoice.set(generatorOptions[0])

        uiElements.engineChoiceMenu =  ttk.OptionMenu(uiElements.engineChoiceMenuLF,info.engineChoice,engineOptions[0], *engineOptions, style = "TMenubutton", command=lambda _: engineChoiceCommand(info.engineChoice,uiElements,uiElements.engineChoiceMenuL,info))
        uiElements.thrustersChoiceMenu = ttk.OptionMenu(uiElements.thrustersChoiceMenuLF,info.thrustersChoice,thrustersOptions[0],*thrustersOptions, style = "TMenubutton", command=lambda _: thrustersChoiceCommand(info.thrustersChoice,uiElements,uiElements.thrustersChoiceMenuL,info))
        uiElements.radarChoiceMenu = ttk.OptionMenu(uiElements.radarChoiceMenuLF,info.radarChoice,radarOptions[0], *radarOptions, style = "TMenubutton",command=lambda _: radarChoiceCommand(info.radarChoice,uiElements,uiElements.radarChoiceMenuL,info))
        uiElements.generatorChoiceMenu = ttk.OptionMenu(uiElements.generatorChoiceMenuLF,info.generatorChoice,generatorOptions[0], *generatorOptions, style = "TMenubutton",command=lambda _: generatorChoiceCommand(info.generatorChoice,uiElements,uiElements.generatorChoiceMenuL,info))
    
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

        info.subsystemChoice0 = StringVar(root)
        info.subsystemChoice1 = StringVar(root)
        info.subsystemChoice2 = StringVar(root)
        info.subsystemChoice3 = StringVar(root)
        info.subsystemChoice4 = StringVar(root)
        info.subsystemChoice5 = StringVar(root)
        info.subsystemChoice6 = StringVar(root)
        info.subsystemChoice7 = StringVar(root)

        info.subsystemChoice0.set(subsystemOptions[0])
        info.subsystemChoice1.set(subsystemOptions[0])
        info.subsystemChoice2.set(subsystemOptions[0])
        info.subsystemChoice3.set(subsystemOptions[0])
        info.subsystemChoice4.set(subsystemOptions[0])
        info.subsystemChoice5.set(subsystemOptions[0])
        info.subsystemChoice6.set(subsystemOptions[0])
        info.subsystemChoice7.set(subsystemOptions[0])

        uiElements.systemChoiceLF = ttk.Labelframe(root, style = 'Grey.TLabelframe',width = uiMetrics.editorSystemsWidth,text = "Systems (optional)", height = 450)
        uiElementsList.append(uiElements.systemChoiceLF)


        uiElements.systemChoiceMenu0 = ttk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice0, systemOptions[0], *systemOptions, style = "TMenubutton",  command=lambda _: systemChoiceCommand(info.systemChoice0,uiElements,uiElements.systemChoiceL0,info,0))
        uiElements.systemChoiceMenu1 = ttk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice1, systemOptions[0], *systemOptions, style = "TMenubutton",  command=lambda _: systemChoiceCommand(info.systemChoice1,uiElements,uiElements.systemChoiceL1,info,1))
        uiElements.systemChoiceMenu2 = ttk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice2, systemOptions[0], *systemOptions, style = "TMenubutton",  command=lambda _: systemChoiceCommand(info.systemChoice2,uiElements,uiElements.systemChoiceL2,info,2))
        uiElements.systemChoiceMenu3 = ttk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice3, systemOptions[0], *systemOptions, style = "TMenubutton",  command=lambda _: systemChoiceCommand(info.systemChoice3,uiElements,uiElements.systemChoiceL3,info,3))
        uiElements.systemChoiceMenu4 = ttk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice4, systemOptions[0], *systemOptions, style = "TMenubutton",  command=lambda _: systemChoiceCommand(info.systemChoice4,uiElements,uiElements.systemChoiceL4,info,4))
        uiElements.systemChoiceMenu5 = ttk.OptionMenu(uiElements.systemChoiceLF, info.systemChoice5, systemOptions[0], *systemOptions, style = "TMenubutton",  command=lambda _: systemChoiceCommand(info.systemChoice5,uiElements,uiElements.systemChoiceL5,info,5))
 
        uiElements.systemChoiceL0 = ttk.Label(uiElements.systemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL1 = ttk.Label(uiElements.systemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL2 = ttk.Label(uiElements.systemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL3 = ttk.Label(uiElements.systemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL4 = ttk.Label(uiElements.systemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL5 = ttk.Label(uiElements.systemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL6 = ttk.Label(uiElements.systemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.systemChoiceL7 = ttk.Label(uiElements.systemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")

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

        uiElements.subsystemChoiceLF = ttk.Labelframe(root, style = 'Grey.TLabelframe',width = uiMetrics.editorSystemsWidth,text = "Subsystems (optional)", height = 450)
        uiElementsList.append(uiElements.subsystemChoiceLF)

        uiElements.subsystemChoiceL0 = ttk.Label(uiElements.subsystemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL1 = ttk.Label(uiElements.subsystemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL2 = ttk.Label(uiElements.subsystemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL3 = ttk.Label(uiElements.subsystemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL4 = ttk.Label(uiElements.subsystemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL5 = ttk.Label(uiElements.subsystemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL6 = ttk.Label(uiElements.subsystemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")
        uiElements.subsystemChoiceL7 = ttk.Label(uiElements.subsystemChoiceLF,style = 'Grey.TLabel', text = "Mass: 0, Cost: 0")

        subsystemChoiceCommand(info.subsystemChoice0,uiElements,uiElements.subsystemChoiceL0,info,0)
        subsystemChoiceCommand(info.subsystemChoice1,uiElements,uiElements.subsystemChoiceL1,info,1)
        subsystemChoiceCommand(info.subsystemChoice2,uiElements,uiElements.subsystemChoiceL2,info,2)
        subsystemChoiceCommand(info.subsystemChoice3,uiElements,uiElements.subsystemChoiceL3,info,3)
        subsystemChoiceCommand(info.subsystemChoice4,uiElements,uiElements.subsystemChoiceL4,info,4)
        subsystemChoiceCommand(info.subsystemChoice5,uiElements,uiElements.subsystemChoiceL5,info,5)
        subsystemChoiceCommand(info.subsystemChoice6,uiElements,uiElements.subsystemChoiceL6,info,6)
        subsystemChoiceCommand(info.subsystemChoice7,uiElements,uiElements.subsystemChoiceL7,info,7)

        uiElements.subsystemChoiceMenu0 = ttk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice0, subsystemOptions[0], *subsystemOptions, style = "TMenubutton",  command=lambda _: subsystemChoiceCommand(info.subsystemChoice0,uiElements,uiElements.subsystemChoiceL0,info,0))
        uiElements.subsystemChoiceMenu1 = ttk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice1, subsystemOptions[0], *subsystemOptions, style = "TMenubutton",  command=lambda _: subsystemChoiceCommand(info.subsystemChoice1,uiElements,uiElements.subsystemChoiceL1,info,1))
        uiElements.subsystemChoiceMenu2 = ttk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice2, subsystemOptions[0], *subsystemOptions, style = "TMenubutton",  command=lambda _: subsystemChoiceCommand(info.subsystemChoice2,uiElements,uiElements.subsystemChoiceL2,info,2))
        uiElements.subsystemChoiceMenu3 = ttk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice3, subsystemOptions[0], *subsystemOptions, style = "TMenubutton",  command=lambda _: subsystemChoiceCommand(info.subsystemChoice3,uiElements,uiElements.subsystemChoiceL3,info,3))
        uiElements.subsystemChoiceMenu4 = ttk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice4, subsystemOptions[0], *subsystemOptions, style = "TMenubutton",  command=lambda _: subsystemChoiceCommand(info.subsystemChoice4,uiElements,uiElements.subsystemChoiceL4,info,4))
        uiElements.subsystemChoiceMenu5 = ttk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice5, subsystemOptions[0], *subsystemOptions, style = "TMenubutton",  command=lambda _: subsystemChoiceCommand(info.subsystemChoice5,uiElements,uiElements.subsystemChoiceL5,info,5))
        uiElements.subsystemChoiceMenu6 = ttk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice6, subsystemOptions[0], *subsystemOptions, style = "TMenubutton",  command=lambda _: subsystemChoiceCommand(info.subsystemChoice6,uiElements,uiElements.subsystemChoiceL6,info,6))
        uiElements.subsystemChoiceMenu7 = ttk.OptionMenu(uiElements.subsystemChoiceLF, info.subsystemChoice7, subsystemOptions[0], *subsystemOptions, style = "TMenubutton",  command=lambda _: subsystemChoiceCommand(info.subsystemChoice7,uiElements,uiElements.subsystemChoiceL7,info,7))

        uiElementsList.append(uiElements.subsystemChoiceMenu0)
        uiElementsList.append(uiElements.subsystemChoiceMenu1)
        uiElementsList.append(uiElements.subsystemChoiceMenu2)
        uiElementsList.append(uiElements.subsystemChoiceMenu3)
        uiElementsList.append(uiElements.subsystemChoiceMenu4)
        uiElementsList.append(uiElements.subsystemChoiceMenu5)
        uiElementsList.append(uiElements.subsystemChoiceMenu6)
        uiElementsList.append(uiElements.subsystemChoiceMenu7)

        uiElementsList.append(uiElements.subsystemChoiceL0)
        uiElementsList.append(uiElements.subsystemChoiceL1)
        uiElementsList.append(uiElements.subsystemChoiceL2)
        uiElementsList.append(uiElements.subsystemChoiceL3)
        uiElementsList.append(uiElements.subsystemChoiceL4)
        uiElementsList.append(uiElements.subsystemChoiceL5)
        uiElementsList.append(uiElements.subsystemChoiceL6)
        uiElementsList.append(uiElements.subsystemChoiceL7)


        uiElements.saveShipButton = tk.Button(root, width = 20, height = 3, text="Save ship design", command = lambda: [saveShip(info,uiElements,filePath,config)])
        uiElements.completeButton = tk.Button(root, width = 20, height = 3, text="Auto-complete ship", command = lambda: [completeShip(uiElements)], state = DISABLED)
        uiElements.clearButton = tk.Button(root, width = 20, height = 3,  text="Clear Design", command = lambda: [clearShip(info,uiElements)])
        uiElements.exitToMenuButton = tk.Button(root, width = 20, height = 3, text="Exit to menu", command=lambda:[placeMenuUi(root,menuUiElements,uiMetrics), hideMenuUi(uiElementsList)])

        uiElementsList.append(uiElements.saveShipButton)
        uiElementsList.append(uiElements.completeButton)
        uiElementsList.append(uiElements.clearButton)
        uiElementsList.append(uiElements.exitToMenuButton)
        (naglowek.shipEditorInfo).uiElements = uiElements
        (naglowek.shipEditorInfo).uiElementsList = uiElementsList
        clearShip(info,uiElements)
        naglowek.editorUiReady = True

    placeShipEditorUi((naglowek.shipEditorInfo).uiElements,uiMetrics)
    mainloop()