from distutils.command.config import config
from functools import partial
from tkinter import *
import tkinter.ttk as ttk
import configparser
import os
from decimal import *
from PIL import ImageTk
import PIL.Image
from pathlib import Path
import sys
import tkinter as tk


from src.settings import dynamic_object
from src.rootCommands import hideMenuUi,hideMultiplayerLabel,placeMenuUi,placeCustomGameUi
import src.settings as settings
from src.loadGame import run
from src.multiplayer.netCommands import disconnect
from src.multiplayer.otherCommands import statusWaitingForServer, statusWaitingForClient
from src.multiplayer.runCommands import  startGameAsServer, sendReadiness, readShip, writeShip


def shipChoiceCommand():
    x=10

def updateButton(info,button,variable,multiplayer,configIn,uiElements):
    chosenAtLeast1v1 = (((not (info.blueShip0).get() == "none" or not (info.blueShip1).get() == "none" or not (info.blueShip2).get() == "none" ))
        and
       (((not (info.redShip0).get() == "none" or not (info.redShip1).get() == "none" or not ( info.redShip2).get() == "none" )))
        and not (info.mapChoice).get() == "none" )
    if(chosenAtLeast1v1 or ((not (info.blueShip0).get() == "none" or not (info.blueShip1).get() == "none" or not (info.blueShip2).get() == "none" ))
        and multiplayer.multiplayerGame):
        button.config(state = NORMAL)
    else:
        button.config(state = DISABLED)
    info.blueMass = 0
    info.redMass = 0
    info.blueCost = 0
    info.redCost = 0
    shipNames = []
    shipNames.append((info.blueShip0).get())
    shipNames.append((info.blueShip1).get())
    shipNames.append((info.blueShip2).get())
    shipNames.append((info.redShip0).get())
    shipNames.append((info.redShip1).get())
    shipNames.append((info.redShip2).get())
    i = 0
    for name in shipNames:
        if(not name == "none"):   
            if(i < 3):
                info.blueMass += float(configIn.get(name,"mass"))
                info.blueCost += float(configIn.get(name,"cost"))
            else:
                info.redMass  += float(configIn.get(name,"mass"))
                info.redCost  += float(configIn.get(name,"cost"))
        i += 1
    i = 0

    if(info.blueMass > 1600):
        uiElements.massLBlue.config(style = 'Red.TLabel')
    elif(info.blueMass > 800):
        uiElements.massLBlue.config(style = 'Yellow.TLabel')
    elif(info.blueMass > 400):
        uiElements.massLBlue.config(style = 'Blue.TLabel')
    else:
        uiElements.massLBlue.config(style = 'Grey.TLabel')
        

    if(info.redMass > 1600):
        uiElements.massLRed.config(style = 'Red.TLabel')
    elif(info.redMass > 800):
        uiElements.massLRed.config(style = 'Yellow.TLabel')
    elif(info.redMass > 400):
        uiElements.massLRed.config(style = 'Blue.TLabel')
    else:        
        uiElements.massLRed.config(style = 'Grey.TLabel')
        
        
    if(info.blueCost > 16000):
        uiElements.costLBlue.config(style = 'Red.TLabel')
    elif(info.blueCost > 8000):
        uiElements.costLBlue.config(style = 'Yellow.TLabel')
    elif(info.blueCost > 4000):
        uiElements.costLBlue.config(style = 'Blue.TLabel')
    else:
        uiElements.costLBlue.config(style = 'Grey.TLabel')
        

    if(info.redCost > 16000):
        uiElements.costLRed.config(style = 'Red.TLabel')
    elif(info.redCost > 8000):
        uiElements.costLRed.config(style = 'Yellow.TLabel')
    elif(info.redCost > 4000):
        uiElements.costLRed.config(style = 'Blue.TLabel')
    else:
        uiElements.costLRed.config(style = 'Grey.TLabel')
        
    uiElements.costLBlue.config(text = "Team Blue Cost: " + str(info.blueCost))
    uiElements.costLRed.config(text = "Team Red Cost: " + str(info.redCost))
    uiElements.massLBlue.config(text = "Team Blue Mass: " + str(info.blueMass))
    uiElements.massLRed.config(text = "Team Red Mass: " + str(info.redMass))
    



    



def runGame(info,configIn,root,menuUiElements, multiplayerOptions):
    shipName0 = (info.blueShip0).get()
    shipName1 = (info.blueShip1).get()
    shipName2 = (info.blueShip2).get()
    shipName3 = (info.redShip0).get()
    shipName4 = (info.redShip1).get()
    shipName5 = (info.redShip2).get()

    configIn1 = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    a = ("maps\\" + info.mapChoice.get() +"\mapInfo.ini")
    filePath = os.path.join(cwd, a)
    configIn1.read(filePath)
      
    configOut = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    filePath = os.path.join(cwd, "gameData/customGame.ini")
    configOut.read(filePath)

    if(not (info.blueShip0).get() == "none"):
        if(not configOut.has_section('Player')):
            configOut.add_section('Player')
        ship0 = readShip(configIn,shipName0,x=configIn1.get("spawnLocations","teamBlue1X"), y=configIn1.get("spawnLocations","teamBlue1Y"),outline="white",owner="player1",id = "0", color = "white")
    else:
        if(configOut.has_section('Player')):
            configOut.remove_section('Player')


    if(not (info.blueShip1).get() == "none"):
        if(not configOut.has_section('Player2')):
            configOut.add_section('Player2')
        ship1 = readShip(configIn,shipName1,x=configIn1.get("spawnLocations","teamBlue2X"), y=configIn1.get("spawnLocations","teamBlue2Y"),outline="white",owner="player1",id = "1", color = "white")
    else:
        if(configOut.has_section('Player2')):
            configOut.remove_section('Player2')


    if(not (info.blueShip2).get() == "none"):
        ship2 = readShip(configIn,shipName2,x=configIn1.get("spawnLocations","teamBlue3X"), y=configIn1.get("spawnLocations","teamBlue3Y"),outline="white",owner="player1",id = "2", color = "white")
        if(not configOut.has_section('Player3')):
            configOut.add_section('Player3')
    else:
        if(configOut.has_section('Player3')):
            configOut.remove_section('Player3')


    if(not (info.redShip0).get() == "none"):
        ship3 = readShip(configIn,shipName3,x=configIn1.get("spawnLocations","teamRed1X"), y=configIn1.get("spawnLocations","teamRed1Y"),outline="red",owner = "ai1",id = "3",color = "red")
        if(not configOut.has_section('Enemy')):
            configOut.add_section('Enemy')
    else:
        if(configOut.has_section('Enemy')):
            configOut.remove_section('Enemy')


    if(not (info.redShip1).get() == "none"):
        ship4 = readShip(configIn,shipName4,x=configIn1.get("spawnLocations","teamRed2X"), y=configIn1.get("spawnLocations","teamRed2Y"),outline="red",owner = "ai1",id = "4",color = "red")
        if(not configOut.has_section('Enemy2')):
            configOut.add_section('Enemy2')
    else:
        if(configOut.has_section('Enemy2')):
            configOut.remove_section('Enemy2')


    if(not (info.redShip2).get() == "none"):
        ship5 = readShip(configIn,shipName5,x=configIn1.get("spawnLocations","teamRed3X"), y=configIn1.get("spawnLocations","teamRed3Y"),outline="red",owner = "ai1",id = "5",color = "red")
        if(not configOut.has_section('Enemy3')):
            configOut.add_section('Enemy3')
    else:
        if(configOut.has_section('Enemy3')):
            configOut.remove_section('Enemy3')


    if(not (info.blueShip0).get() == "none"):
        writeShip(ship0,"Player",configOut)
    if(not (info.blueShip1).get() == "none"):
        writeShip(ship1,"Player2",configOut)
    if(not (info.blueShip2).get() == "none"):
        writeShip(ship2,"Player3",configOut)
    if(not (info.redShip0).get() == "none"):
        writeShip(ship3,"Enemy",configOut)
    if(not (info.redShip1).get() == "none"):
        writeShip(ship4,"Enemy2",configOut)
    if(not (info.redShip2).get() == "none"):
        writeShip(ship5,"Enemy3",configOut)

    if(not configOut.has_section("Root")):
        configOut.add_section("Root")
    if(not configOut.has_section("Meta")):
        configOut.add_section("Meta")
    configOut.set("Meta", "winMessage","Blue Team Wins")
    configOut.set("Meta", "looseMessage","Red Team Wins")
    configOut.set("Root", "title","Custom Game")
    
    configOut.set("Meta", "winByEliminatingEnemy","1")
    configOut.set("Meta", "looseByEliminatingEnemy","0")
    configOut.set("Meta", "winByEliminatingPlayer","0")
    configOut.set("Meta", "looseByEliminatingPlayer","1")
    
    configOut.set("Meta", "winByDisablingEnemy","0")
    configOut.set("Meta", "looseByDisablingEnemy","0")
    configOut.set("Meta", "winByDisablingPlayer","0")
    configOut.set("Meta", "looseByDisablingPlayer","0")
    configOut.set("Meta", "objectives", ">_ Eliminate enemy presence\nin the area_")

    if(not configOut.has_section("Ships")):
        configOut.add_section("Ships")
    configOut.set("Ships", "playerName",shipName0)
    configOut.set("Ships", "playerName2",shipName1)
    configOut.set("Ships", "playerName3",shipName2)
    configOut.set("Ships", "enemyName",shipName3)
    configOut.set("Ships", "enemyName2",shipName4)
    configOut.set("Ships", "enemyName3",shipName5)

    if(not configOut.has_section("Options")):
        configOut.add_section("Options")
    configOut.set("Options", "fogOfWar",info.fogOfWar.get())

    if(not configOut.has_section("Images")):
        configOut.add_section("Images")
    configOut.set("Images", "map", info.mapChoice.get())
    configOut.set("Images", "img", cwd + "\maps\\" + info.mapChoice.get() + "\map.png")
    configOut.set("Images", "image", cwd + "\maps\\" + info.mapChoice.get() + "\map.png")
    configOut.set("Images", "imageMask", cwd + "\maps\\" + info.mapChoice.get() +"\mapMask.png")

    
    hd = open(filePath, "w")
    configOut.write(hd)

    run(configOut,root,menuUiElements,multiplayerOptions)


def writeShip(ship,target,configOut):
    configOut.set(target, "name",ship.name)
    configOut.set(target, "systemSlots1",ship.systemSlots1)
    configOut.set(target, "systemSlots2",ship.systemSlots2)
    configOut.set(target, "systemSlots3",ship.systemSlots3)
    configOut.set(target, "systemSlots4",ship.systemSlots4)
    configOut.set(target, "systemSlots5",ship.systemSlots5)
    configOut.set(target, "systemSlots6",ship.systemSlots6)
    configOut.set(target, "systemStatus1","0")
    configOut.set(target, "systemStatus2","0")
    configOut.set(target, "systemStatus3","0")
    configOut.set(target, "systemStatus4","0")
    configOut.set(target, "systemStatus5","0")
    configOut.set(target, "systemStatus6","0")
    configOut.set(target, "subsystemSlots1",ship.subsystemSlots1)
    configOut.set(target, "subsystemSlots2",ship.subsystemSlots2)
    configOut.set(target, "subsystemSlots3",ship.subsystemSlots3)
    configOut.set(target, "subsystemSlots4",ship.subsystemSlots4)
    configOut.set(target, "subsystemSlots5",ship.subsystemSlots5)
    configOut.set(target, "subsystemSlots6",ship.subsystemSlots6)
    configOut.set(target, "subsystemSlots7",ship.subsystemSlots7)
    configOut.set(target, "subsystemSlots8",ship.subsystemSlots8)
    configOut.set(target, "shields",ship.shields)
    configOut.set(target, "energyLimit",ship.energyLimit)
    configOut.set(target, "hp",ship.hp)
    configOut.set(target, "maxHp",ship.maxHp)
    configOut.set(target, "ap",ship.hp)
    configOut.set(target, "maxAp",ship.maxHp)
    configOut.set(target, "turnRate",ship.turnRate)
    configOut.set(target, "maxShields",ship.maxShields)
    configOut.set(target, "detectionRange",ship.detectionRange)
    configOut.set(target, "maxSpeed",ship.maxSpeed)
    configOut.set(target, "speed",ship.speed)
    configOut.set(target, "xPos",ship.xPos)
    configOut.set(target, "yPos",ship.yPos)
    configOut.set(target, "outline",ship.outline)
    configOut.set(target, "outlineColor",ship.outline)
    configOut.set(target, "owner",ship.owner)
    configOut.set(target, "id",ship.id)
    configOut.set(target, "stance",ship.stance)
    configOut.set(target, "color",ship.color)

    
def updateMissionCanvas(missionCanvas,info,msmVar):
    missionCanvas.delete("all")
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    c = os.path.join(cwd, "maps\\" + (info.mapChoice).get() +"\\mapMiniature.png")
    b = PIL.Image.open(c)
    b = b.resize((800, 500),)
    msmVar.img = ImageTk.PhotoImage(b)
    missionCanvas.create_image(0,0,image=msmVar.img,anchor=NW)
    return msmVar.img

def customGame(root,config,uiMenuElements,uiMetrics,multiplayerOptions):
    root.title("Custom Game Menu")
    if(not settings.cgGameUiReady):
        configIn = configparser.ConfigParser()
        cwd = Path(sys.argv[0])
        cwd = str(cwd.parent)
        filePath = os.path.join(cwd, "gameData/customShips.ini")
        configIn.read(filePath)

        uiElements = dynamic_object()        
        uiElementsList = []
        info = settings.cgGameInfo   
            
        cwd = str(sys.argv[0]).removesuffix("\main.py")
        cwd = str(sys.argv[0]).removesuffix("/main.py")

        mapOptions = settings.mapOptions
        info.mapChoice = StringVar(root)
        info.mapChoice.set(mapOptions[0])
        uiElements.missionCanvas = Canvas(root,width = uiMetrics.cgCanvasWidth, height = uiMetrics.cgCanvasHeight)
        (uiElements.missionCanvas).config(bg="green")
        msmVar = settings.dynamic_object()
        imageToAvoidTrashCollecting = updateMissionCanvas(uiElements.missionCanvas,info,msmVar)

        info.fogOfWar = StringVar(root)
        info.swapStartingPositions = StringVar(root)

        shipOptions = configIn.sections()
        shipOptions = ["none"] + shipOptions

        info.blueMass = 0
        info.blueCost = 0
        info.redMass = 0
        info.redCost = 0

        info.blueShip0 = StringVar(root)
        info.blueShip1 = StringVar(root)
        info.blueShip2 = StringVar(root)
        info.redShip0 = StringVar(root)
        info.redShip1 = StringVar(root)
        info.redShip2 = StringVar(root)

        info.blueShip0.set(shipOptions[0])
        info.blueShip1.set(shipOptions[0])
        info.blueShip2.set(shipOptions[0])
        info.redShip0.set(shipOptions[0])
        info.redShip1.set(shipOptions[0])
        info.redShip2.set(shipOptions[0])
        uiElements.startGameBF = tk.Frame(root)
        uiElements.startGameBF.config(bg="#4582ec", width=2, height=2,padx=1)
        if(not multiplayerOptions.multiplayerGame):
            buttonCommand = partial(
                runGame,info,configIn,root,uiMenuElements,multiplayerOptions
            )
            uiElements.startGameButton = tk.Button(uiElements.startGameBF, text="Start Game", 
            command = lambda:[buttonCommand(), 
            hideMenuUi(uiElementsList), hideMultiplayerLabel(multiplayerOptions,uiElements)],width=20,height=3,state = DISABLED)
            uiElements.startGameButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
        else:
            if(multiplayerOptions.side == 'server'):
                buttonCommand = partial(
                    startGameAsServer, info,configIn,root,uiMenuElements, multiplayerOptions
                )
                uiElements.startGameButton = tk.Button(uiElements.startGameBF, text="Start Game", 
                command = lambda:[buttonCommand(), statusWaitingForClient(multiplayerOptions), 
                hideMenuUi(uiElementsList), hideMultiplayerLabel(multiplayerOptions,uiElements),multiplayerOptions.statusLabel.place_forget()],width=20,height=3,state = DISABLED)          
                uiElements.startGameButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
  
            else:
                buttonCommand = partial(
                    sendReadiness, info,configIn,root,uiMenuElements,multiplayerOptions,uiMenuElements
                )
                uiElements.startGameButton = tk.Button(uiElements.startGameBF, text="Get Ready", 
                command = lambda:[buttonCommand(), statusWaitingForServer(multiplayerOptions), 
                hideMenuUi(uiElementsList), hideMultiplayerLabel(multiplayerOptions,uiElements),multiplayerOptions.statusLabel.place_forget()],width=20,height=3,state = DISABLED)
                uiElements.startGameButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
  
        uiElementsList.append(uiElements.startGameButton)
        uiElementsList.append(uiElements.startGameBF)

        uiElements.exitToMenuBF = tk.Frame(root)
        uiElements.exitToMenuBF.config(bg="#4582ec", width=2, height=2,padx=1)
        uiElements.exitToMenuButton = tk.Button(uiElements.exitToMenuBF, width = 20, height = 3, text="Exit to menu", command=lambda:[placeMenuUi(root,uiMenuElements,uiMetrics), hideMenuUi(uiElementsList), hideMultiplayerLabel(multiplayerOptions,uiElements)])
        uiElements.exitToMenuButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
        uiElementsList.append(uiElements.exitToMenuBF)  
        uiElementsList.append(uiElements.exitToMenuButton)  

        uiElements.costLBlue = ttk.Label(root,style = 'Grey.TLabel', text = "Team Blue Mass: " + str(info.blueCost), width = 24)
        uiElements.costLRed = ttk.Label(root,style = 'Grey.TLabel',  text = "Team Red Mass: " + str(info.redCost), width = 24)
        uiElements.massLBlue = ttk.Label(root,style = 'Grey.TLabel', text = "Team Blue Mass: " + str(info.blueMass), width = 24)
        uiElements.massLRed = ttk.Label(root,style = 'Grey.TLabel',  text = "Team Red Mass: " + str(info.redMass), width = 24)
        uiElementsList.append(uiElements.costLBlue)
        uiElementsList.append(uiElements.costLRed)          
        uiElementsList.append(uiElements.massLBlue)
        uiElementsList.append(uiElements.massLRed)  

        uiElements.mapLF = ttk.Labelframe(root,style = 'Grey.TLabelframe', width = uiMetrics.cgMapLFWidth, height = 100, text = "Map Choice")
        uiElements.mapOMF = tk.Frame(uiElements.mapLF)
       
        uiElements.mapOM = tk.OptionMenu(uiElements.mapOMF, info.mapChoice, *mapOptions, command = lambda _:[updateButton(info, uiElements.startGameButton, info.mapChoice,multiplayerOptions,configIn,uiElements),updateMissionCanvas(uiElements.missionCanvas,info,msmVar)])
        uiElements.foWLF = ttk.Labelframe(root,style = 'Grey.TLabelframe', width = uiMetrics.cgMapLFWidth, height = 150, text = "Special Rules")
        uiElements.foWCB = ttk.Checkbutton(uiElements.foWLF,style = "Red.TCheckbutton", variable = info.fogOfWar, text = "Fog of War", width = 20)
        uiElements.swapCB = ttk.Checkbutton(uiElements.foWLF,style = "Red.TCheckbutton", variable = info.swapStartingPositions, text = "Swap starting positions", width = 20)
               
        uiElements.mapOM.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.mapOMF.config(bg="#4582ec", width=2, height=2,padx=1)
        uiElements.foWCB.invoke()
        uiElements.foWCB.invoke()

        uiElements.blueShipLF0 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = uiMetrics.cgShipLFHeight, text = "Blue team ship 1")
        uiElements.blueShipLF1 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = uiMetrics.cgShipLFHeight, text = "Blue team ship 2")
        uiElements.blueShipLF2 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = uiMetrics.cgShipLFHeight, text = "Blue team ship 3")

        uiElements.redShipLF0 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = uiMetrics.cgShipLFHeight, text = "Red team ship 1")
        uiElements.redShipLF1 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = uiMetrics.cgShipLFHeight, text = "Red team ship 2")
        uiElements.redShipLF2 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = uiMetrics.cgShipLFHeight, text = "Red team ship 3")

        uiElements.blueShipOM0F = tk.Frame(uiElements.blueShipLF0)
        uiElements.blueShipOM0 = tk.OptionMenu(uiElements.blueShipOM0F, info.blueShip0, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.blueShip0,multiplayerOptions,configIn,uiElements))
        uiElements.blueShipOM0.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.blueShipOM0F.config(bg="#4582ec", width=2, height=2,padx=1)
        uiElements.blueShipOM1F = tk.Frame(uiElements.blueShipLF1)
        uiElements.blueShipOM1 = tk.OptionMenu(uiElements.blueShipOM1F, info.blueShip1, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.blueShip1,multiplayerOptions,configIn,uiElements))
        uiElements.blueShipOM1.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.blueShipOM1F.config(bg="#4582ec", width=2, height=2,padx=1)
        uiElements.blueShipOM2F = tk.Frame(uiElements.blueShipLF2)
        uiElements.blueShipOM2 = tk.OptionMenu(uiElements.blueShipOM2F, info.blueShip2, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.blueShip2,multiplayerOptions,configIn,uiElements))
        uiElements.blueShipOM2.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.blueShipOM2F.config(bg="#4582ec", width=1, height=1,padx=1)       
        

        uiElements.redShipOM0F = tk.Frame(uiElements.redShipLF0)
        uiElements.redShipOM0 = tk.OptionMenu(uiElements.redShipOM0F, info.redShip0, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.redShip0,multiplayerOptions,configIn,uiElements))
        uiElements.redShipOM0.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.redShipOM0F.config(bg="#4582ec", width=1, height=1,padx=1)
        uiElements.redShipOM1F = tk.Frame(uiElements.redShipLF1)
        uiElements.redShipOM1 = tk.OptionMenu(uiElements.redShipOM1F, info.redShip1, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.redShip1,multiplayerOptions,configIn,uiElements))
        uiElements.redShipOM1.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.redShipOM1F.config(bg="#4582ec", width=1, height=1,padx=1)
        uiElements.redShipOM2F = tk.Frame(uiElements.redShipLF2)
        uiElements.redShipOM2 = tk.OptionMenu(uiElements.redShipOM2F, info.redShip2, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.redShip2,multiplayerOptions,configIn,uiElements))
        uiElements.redShipOM2.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        uiElements.redShipOM2F.config(bg="#4582ec", width=1, height=1,padx=1)
     
        uiElementsList.append(uiElements.missionCanvas)
        uiElementsList.append(uiElements.redShipOM1)
        uiElementsList.append(uiElements.redShipOM2)
        uiElementsList.append(uiElements.blueShipLF0)
        uiElementsList.append(uiElements.blueShipLF1)
        uiElementsList.append(uiElements.blueShipLF2)
        uiElementsList.append(uiElements.redShipLF0)
        uiElementsList.append(uiElements.redShipLF1)
        uiElementsList.append(uiElements.redShipLF2)
        uiElementsList.append(uiElements.blueShipOM0)
        uiElementsList.append(uiElements.blueShipOM1)
        uiElementsList.append(uiElements.blueShipOM2)
        uiElementsList.append(uiElements.redShipOM0)
        uiElementsList.append(uiElements.redShipOM1)
        uiElementsList.append(uiElements.redShipOM2)
        uiElementsList.append(uiElements.blueShipLF0)
        uiElementsList.append(uiElements.blueShipLF1)
        uiElementsList.append(uiElements.blueShipLF2)
        uiElementsList.append(uiElements.redShipLF0)
        uiElementsList.append(uiElements.redShipLF1)
        uiElementsList.append(uiElements.redShipLF2)
        uiElementsList.append(uiElements.mapLF)
        uiElementsList.append(uiElements.mapOM)
        uiElementsList.append(uiElements.foWLF)
        uiElementsList.append(uiElements.foWCB)

        (settings.cgGameInfo).uiElements = uiElements
        (settings.cgGameInfo).uiElementsList = uiElementsList
        settings.cgGameUiReady = True

    placeCustomGameUi((settings.cgGameInfo).uiElements,uiMetrics,multiplayerOptions)
    mainloop()