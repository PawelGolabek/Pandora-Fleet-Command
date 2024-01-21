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


from src.naglowek import dynamic_object
from src.rootCommands import *
import src.naglowek as naglowek
from src.battleSystem import run

def shipChoiceCommand():
    x=10

def updateButton(info,button,variable):  
    if(not ((info.blueShip0).get() == "none" or (info.blueShip1).get() == "none"
     or (info.blueShip2).get() == "none" or ( info.redShip0).get() == "none"
     or( info.redShip1).get() == "none" or ( info.redShip2).get() == "none" 
     or ( info.mapChoice).get() == "none") ):
        button.config(state = NORMAL)
    else:
        button.config(state = DISABLED)


def runGame(info,configIn,root,menuUiElements):
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
    
    ship0 = readShip(configIn,shipName0,x=configIn1.get("spawnLocations","teamBlue1X"),y=configIn1.get("spawnLocations","teamBlue1Y"),outline="white",owner="player1",id = "0", color = "white")
    ship1 = readShip(configIn,shipName1,x=configIn1.get("spawnLocations","teamBlue2X"),y=configIn1.get("spawnLocations","teamBlue2Y"),outline="white",owner="player1",id = "1", color = "white")
    ship2 = readShip(configIn,shipName2,x=configIn1.get("spawnLocations","teamBlue3X"),y=configIn1.get("spawnLocations","teamBlue3Y"),outline="white",owner="player1",id = "2", color = "white")
    ship3 = readShip(configIn,shipName3,x=configIn1.get("spawnLocations","teamRed1X"),y=configIn1.get("spawnLocations","teamRed1Y"),outline="red",owner = "ai1",id = "3",color = "red")
    ship4 = readShip(configIn,shipName4,x=configIn1.get("spawnLocations","teamRed2X"),y=configIn1.get("spawnLocations","teamRed2Y"),outline="red",owner = "ai1",id = "4",color = "red")
    ship5 = readShip(configIn,shipName5,x=configIn1.get("spawnLocations","teamRed3X"),y=configIn1.get("spawnLocations","teamRed3Y"),outline="red",owner = "ai1",id = "5",color = "red")

    configOut = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    filePath = os.path.join(cwd, "gameData/customGame.ini")
    configOut.read(filePath)

    writeShip(ship0,"Player",configOut)
    writeShip(ship1,"Player2",configOut)
    writeShip(ship2,"Player3",configOut)
    writeShip(ship3,"Enemy",configOut)
    writeShip(ship4,"Enemy2",configOut)
    writeShip(ship5,"Enemy3",configOut)

    if(not configOut.has_section("Root")):
        configOut.add_section("Root")
    if(not configOut.has_section("Meta")):
        configOut.add_section("Meta")
    configOut.set("Meta", "winMessage","Blue Team Wins")
    configOut.set("Meta", "looseMessage","Red Team Wins")
    configOut.set("Root", "title","Custom Game")
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

    run(configOut,root,menuUiElements)

def readShip(confIn,shipId,x,y,outline,owner,id,color):
    ship = dynamic_object()
    ship.name = shipId
    ship.shields = str(confIn.get(ship.name,"shields"))
    ship.energyLimit = str(confIn.get(ship.name,"energyLimit"))
    ship.maxShields = str(confIn.get(shipId,"maxShields"))
    ship.detectionRange = str(confIn.get(shipId,"detectionRange"))
    ship.turnRate = str(confIn.get(shipId,"turnRate"))
    ship.speed = str(confIn.get(shipId,"speed"))
    ship.maxSpeed = str(confIn.get(shipId,"maxSpeed"))

    ship.systemSlots1 = str(confIn.get(shipId,"systemSlots1"))
    ship.systemSlots2 = str(confIn.get(shipId,"systemSlots2"))
    ship.systemSlots3 = str(confIn.get(shipId,"systemSlots3"))
    ship.systemSlots4 = str(confIn.get(shipId,"systemSlots4"))
    ship.systemSlots5 = str(confIn.get(shipId,"systemSlots5"))
    ship.systemSlots6 = str(confIn.get(shipId,"systemSlots6"))
    ship.systemSlots7 = str(confIn.get(shipId,"systemSlots7"))
    ship.systemSlots8 = str(confIn.get(shipId,"systemSlots8"))

    ship.subsystemSlots1 = str(confIn.get(shipId,"subsystemSlots1"))
    ship.subsystemSlots2 = str(confIn.get(shipId,"subsystemSlots2"))
    ship.subsystemSlots3 = str(confIn.get(shipId,"subsystemSlots3"))
    ship.subsystemSlots4 = str(confIn.get(shipId,"subsystemSlots4"))
    ship.subsystemSlots5 = str(confIn.get(shipId,"subsystemSlots5"))
    ship.subsystemSlots6 = str(confIn.get(shipId,"subsystemSlots6"))
    ship.subsystemSlots7 = str(confIn.get(shipId,"subsystemSlots7"))
    ship.subsystemSlots8 = str(confIn.get(shipId,"subsystemSlots8"))

    ship.stance = str(confIn.get(shipId,"stance"))

    ship.xPos = str(x)
    ship.yPos = str(y)
    ship.outline = outline
    ship.owner = str(owner)
    ship.id = str(id)
    ship.color = str(color)
    return ship

def writeShip(ship,target,configOut):

    configOut.set(target, "name",ship.name)
    configOut.set(target, "systemSlots1",ship.systemSlots1)
    configOut.set(target, "systemSlots2",ship.systemSlots2)
    configOut.set(target, "systemSlots3",ship.systemSlots3)
    configOut.set(target, "systemSlots4",ship.systemSlots4)
    configOut.set(target, "systemSlots5",ship.systemSlots5)
    configOut.set(target, "systemSlots6",ship.systemSlots6)
    configOut.set(target, "systemSlots7",ship.systemSlots7)
    configOut.set(target, "systemSlots8",ship.systemSlots8)
    configOut.set(target, "systemStatus1","0")
    configOut.set(target, "systemStatus2","0")
    configOut.set(target, "systemStatus3","0")
    configOut.set(target, "systemStatus4","0")
    configOut.set(target, "systemStatus5","0")
    configOut.set(target, "systemStatus6","0")
    configOut.set(target, "systemStatus7","0")
    configOut.set(target, "systemStatus8","0")
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
    configOut.set(target, "maxShields",ship.maxShields)
    configOut.set(target, "detectionRange",ship.detectionRange)
    configOut.set(target, "maxSpeed",ship.maxSpeed)
    configOut.set(target, "speed",ship.speed)
    configOut.set(target, "xPos",ship.xPos)
    configOut.set(target, "yPos",ship.yPos)
    configOut.set(target, "outline",ship.outline)
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
    b = b.resize((800, 500), PIL.Image.ANTIALIAS)
    msmVar.img = ImageTk.PhotoImage(b)
    missionCanvas.create_image(0,0,image=msmVar.img,anchor=NW)
    return msmVar.img


def customGame(root,config,uiMenuElements,uiMetrics):
    root.title("Custom Game Menu")
    if(not naglowek.cgGameUiReady):
        configIn = configparser.ConfigParser()
        cwd = Path(sys.argv[0])
        cwd = str(cwd.parent)
        filePath = os.path.join(cwd, "gameData/customShips.ini")
        configIn.read(filePath)

        uiElements = dynamic_object()        
        uiElementsList = []
        info = naglowek.cgGameInfo   
            
        cwd = str(sys.argv[0]).removesuffix("\main.py")
        cwd = str(sys.argv[0]).removesuffix("/main.py")

        mapOptions = naglowek.mapOptions
        info.mapChoice = StringVar(root)
        info.mapChoice.set(mapOptions[0])
        uiElements.missionCanvas = Canvas(root,width = uiMetrics.cgCanvasWidth, height = uiMetrics.cgCanvasHeight)
        (uiElements.missionCanvas).config(bg="green")
        msmVar = naglowek.dynamic_object()
        imageToAvoidTrashCollecting = updateMissionCanvas(uiElements.missionCanvas,info,msmVar)

        info.fogOfWar = StringVar(root)

        shipOptions = configIn.sections()
        shipOptions = ["none"] + shipOptions

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

        buttonCommand = partial(runGame,info,configIn,root,uiMenuElements)
        uiElements.startGameButton = Button(root, text="Start Game", command = lambda:[buttonCommand(), hideMenuUi(uiElementsList)],width=20,height=3,state = DISABLED)
        uiElements.exitToMenuButton = tk.Button(root, width = 20, height = 3, text="Exit to menu", command=lambda:[placeMenuUi(root,uiMenuElements,uiMetrics), hideMenuUi(uiElementsList)])
        uiElementsList.append(uiElements.startGameButton)
        uiElementsList.append(uiElements.exitToMenuButton)

        uiElements.mapLF = ttk.Labelframe(root,style = 'Grey.TLabelframe', width = uiMetrics.cgMapLFWidth, height = 100, text = "Map Choice")
        uiElements.mapOM = OptionMenu(uiElements.mapLF, info.mapChoice, *mapOptions, command = lambda _:[updateButton(info, uiElements.startGameButton, info.mapChoice),updateMissionCanvas(uiElements.missionCanvas,info,msmVar)])
        uiElements.foWLF = ttk.Labelframe(root,style = 'Grey.TLabelframe', width = uiMetrics.cgMapLFWidth, height = 70, text = "Special Rules")
        uiElements.foWCB = ttk.Checkbutton(uiElements.foWLF,style = "Red.TCheckbutton", text = "Fog of War", width = 20)
        uiElements.foWCB.invoke()

        uiElements.blueShipLF0 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = 80, text = "Blue team ship 1")
        uiElements.blueShipLF1 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = 80, text = "Blue team ship 2")
        uiElements.blueShipLF2 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = 80, text = "Blue team ship 3")
        uiElements.redShipLF0 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = 80, text = "Red team ship 1")
        uiElements.redShipLF1 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = 80, text = "Red team ship 2")
        uiElements.redShipLF2 = ttk.Labelframe(root, style = 'Grey.TLabelframe', width = uiMetrics.cgShipLF, height = 80, text = "Red team ship 3")

        uiElements.blueShipOM0 = OptionMenu(uiElements.blueShipLF0, info.blueShip0, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.blueShip0))
        uiElements.blueShipOM1 = OptionMenu(uiElements.blueShipLF1, info.blueShip1, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.blueShip1))
        uiElements.blueShipOM2 = OptionMenu(uiElements.blueShipLF2, info.blueShip2, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.blueShip2))
        uiElements.redShipOM0 = OptionMenu(uiElements.redShipLF0, info.redShip0, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.redShip0))
        uiElements.redShipOM1 = OptionMenu(uiElements.redShipLF1, info.redShip1, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.redShip1))
        uiElements.redShipOM2 = OptionMenu(uiElements.redShipLF2, info.redShip2, *shipOptions, command = lambda _: updateButton(info, uiElements.startGameButton, info.redShip2))

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

        (naglowek.cgGameInfo).uiElements = uiElements
        (naglowek.cgGameInfo).uiElementsList = uiElementsList
        naglowek.cgGameUiReady = True

    placeCustomGameUi((naglowek.cgGameInfo).uiElements,uiMetrics)
    mainloop()