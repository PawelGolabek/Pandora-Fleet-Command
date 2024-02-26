from tkinter import *
from pathlib import Path
import socket
import configparser
import sys
import os
import configparser
import copy
import json

from src.settings import dynamic_object
from src.objects.ship import ship
from src.multiplayer.netCommands import fill_data_to_size
from src.loadGame import run

def readMultiplayerShip(confIn,shipId,x,y,outline,owner,id,color):
    ship = dynamic_object()
    ship.name = str(confIn.get(shipId,"name"))
    ship.shields = str(confIn.get(shipId,"shields"))
    ship.energyLimit = str(confIn.get(shipId,"energyLimit"))
    ship.maxShields = str(confIn.get(shipId,"maxShields"))
    ship.detectionRange = str(confIn.get(shipId,"detectionRange"))
    ship.turnRate = str(confIn.get(shipId,"turnrate"))
    ship.speed = str(confIn.get(shipId,"speed"))
    ship.maxSpeed = str(confIn.get(shipId,"maxSpeed"))

    ship.systemSlots1 = str(confIn.get(shipId,"systemSlots1"))
    ship.systemSlots2 = str(confIn.get(shipId,"systemSlots2"))
    ship.systemSlots3 = str(confIn.get(shipId,"systemSlots3"))
    ship.systemSlots4 = str(confIn.get(shipId,"systemSlots4"))
    ship.systemSlots5 = str(confIn.get(shipId,"systemSlots5"))
    ship.systemSlots6 = str(confIn.get(shipId,"systemSlots6"))

    ship.subsystemSlots1 = str(confIn.get(shipId,"subsystemSlots1"))
    ship.subsystemSlots2 = str(confIn.get(shipId,"subsystemSlots2"))
    ship.subsystemSlots3 = str(confIn.get(shipId,"subsystemSlots3"))
    ship.subsystemSlots4 = str(confIn.get(shipId,"subsystemSlots4"))
    ship.subsystemSlots5 = str(confIn.get(shipId,"subsystemSlots5"))
    ship.subsystemSlots6 = str(confIn.get(shipId,"subsystemSlots6"))
    ship.subsystemSlots7 = str(confIn.get(shipId,"subsystemSlots7"))
    ship.subsystemSlots8 = str(confIn.get(shipId,"subsystemSlots8"))
    
    ship.hp = str(confIn.get(shipId,"hp"))
    ship.ap = str(confIn.get(shipId,"ap"))
    ship.maxHp = str(confIn.get(shipId,"maxHp"))
    ship.maxAp = str(confIn.get(shipId,"maxAp"))

    ship.stance = str(confIn.get(shipId,"stance"))

    ship.xPos = str(x)
    ship.yPos = str(y)
    ship.outline = outline
    ship.owner = str(owner)
    ship.id = str(id)
    ship.color = str(color)
    return ship

def writeShip(ship,section,configOut):

    configOut.set(section, "name",ship.name)
    configOut.set(section, "systemSlots1",ship.systemSlots1)
    configOut.set(section, "systemSlots2",ship.systemSlots2)
    configOut.set(section, "systemSlots3",ship.systemSlots3)
    configOut.set(section, "systemSlots4",ship.systemSlots4)
    configOut.set(section, "systemSlots5",ship.systemSlots5)
    configOut.set(section, "systemSlots6",ship.systemSlots6)
    configOut.set(section, "systemStatus1","0")
    configOut.set(section, "systemStatus2","0")
    configOut.set(section, "systemStatus3","0")
    configOut.set(section, "systemStatus4","0")
    configOut.set(section, "systemStatus5","0")
    configOut.set(section, "systemStatus6","0")
    configOut.set(section, "subsystemSlots1",ship.subsystemSlots1)
    configOut.set(section, "subsystemSlots2",ship.subsystemSlots2)
    configOut.set(section, "subsystemSlots3",ship.subsystemSlots3)
    configOut.set(section, "subsystemSlots4",ship.subsystemSlots4)
    configOut.set(section, "subsystemSlots5",ship.subsystemSlots5)
    configOut.set(section, "subsystemSlots6",ship.subsystemSlots6)
    configOut.set(section, "subsystemSlots7",ship.subsystemSlots7)
    configOut.set(section, "subsystemSlots8",ship.subsystemSlots8)
    configOut.set(section, "shields",ship.shields)
    configOut.set(section, "energyLimit",ship.energyLimit)
    configOut.set(section, "hp",ship.hp)
    configOut.set(section, "maxHp",ship.maxHp)
    configOut.set(section, "ap",ship.hp)
    configOut.set(section, "maxAp",ship.maxHp)
    configOut.set(section, "turnRate",ship.turnRate)
    configOut.set(section, "maxShields",ship.maxShields)
    configOut.set(section, "detectionRange",ship.detectionRange)
    configOut.set(section, "maxSpeed",ship.maxSpeed)
    configOut.set(section, "speed",ship.speed)
    configOut.set(section, "xPos",ship.xPos)
    configOut.set(section, "yPos",ship.yPos)
    configOut.set(section, "outline",ship.outline)
    configOut.set(section, "outlineColor",ship.outline)
    configOut.set(section, "owner",ship.owner)
    configOut.set(section, "id",ship.id)
    configOut.set(section, "stance",ship.stance)
    configOut.set(section, "color",ship.color)



def readShip(confIn,shipId,x,y,outline,owner,id,color):
    ship = dynamic_object()
    ship.name = shipId
    ship.shields = str(confIn.get(ship.name,"shields"))
    ship.energyLimit = str(confIn.get(ship.name,"energyLimit"))
    ship.maxShields = str(confIn.get(shipId,"maxShields"))
    ship.detectionRange = str(confIn.get(shipId,"detectionRange"))
    ship.turnRate = str(confIn.get(shipId,"turnrate"))
    ship.speed = str(confIn.get(shipId,"speed"))
    ship.maxSpeed = str(confIn.get(shipId,"maxSpeed"))

    ship.systemSlots1 = str(confIn.get(shipId,"systemSlots1"))
    ship.systemSlots2 = str(confIn.get(shipId,"systemSlots2"))
    ship.systemSlots3 = str(confIn.get(shipId,"systemSlots3"))
    ship.systemSlots4 = str(confIn.get(shipId,"systemSlots4"))
    ship.systemSlots5 = str(confIn.get(shipId,"systemSlots5"))
    ship.systemSlots6 = str(confIn.get(shipId,"systemSlots6"))

    ship.subsystemSlots1 = str(confIn.get(shipId,"subsystemSlots1"))
    ship.subsystemSlots2 = str(confIn.get(shipId,"subsystemSlots2"))
    ship.subsystemSlots3 = str(confIn.get(shipId,"subsystemSlots3"))
    ship.subsystemSlots4 = str(confIn.get(shipId,"subsystemSlots4"))
    ship.subsystemSlots5 = str(confIn.get(shipId,"subsystemSlots5"))
    ship.subsystemSlots6 = str(confIn.get(shipId,"subsystemSlots6"))
    ship.subsystemSlots7 = str(confIn.get(shipId,"subsystemSlots7"))
    ship.subsystemSlots8 = str(confIn.get(shipId,"subsystemSlots8"))
    
    ship.hp = str(confIn.get(shipId,"hp"))
    ship.ap = str(confIn.get(shipId,"ap"))
    ship.maxHp = str(confIn.get(shipId,"maxHp"))
    ship.maxAp = str(confIn.get(shipId,"maxAp"))

    ship.stance = str(confIn.get(shipId,"stance"))

    ship.xPos = str(x)
    ship.yPos = str(y)
    ship.outline = outline
    ship.owner = str(owner)
    ship.id = str(id)
    ship.color = str(color)
    return ship


def startGameAsServer(info,configIn,root,menuUiElements, multiplayerOptions):

    shipName0 = (info.blueShip0).get()
    shipName1 = (info.blueShip1).get()
    shipName2 = (info.blueShip2).get()

    configIn1 = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    a = ("maps\\" + info.mapChoice.get() +"\mapInfo.ini")
    filePath = os.path.join(cwd, a)
    configIn1.read(filePath)
      
    configOut = configparser.ConfigParser()

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

    if(not configOut.has_section("Ships")):
        configOut.add_section("Ships")

    if(not configOut.has_section("Options")):
        configOut.add_section("Options")
    configOut.set("Options", "fogOfWar",info.fogOfWar.get())

    if(not configOut.has_section("Images")):
        configOut.add_section("Images")
    configOut.set("Images", "map", info.mapChoice.get())
    configOut.set("Images", "img", cwd + "\maps\\" + info.mapChoice.get() + "\map.png")
    configOut.set("Images", "image", cwd + "\maps\\" + info.mapChoice.get() + "\map.png")
    configOut.set("Images", "imageMask", cwd + "\maps\\" + info.mapChoice.get() +"\mapMask.png")

    receivedData = multiplayerOptions.clientSocket.recv(16384).decode()          ##### client info received
    multiplayerOptions.clientSocket.recv(0)

    dataDict = json.loads(receivedData)

    # Step 2: Convert the dictionary to configparser format
    config = configparser.ConfigParser()
    configOutForClient = copy.deepcopy(configOut)


  #  for section in configOutForClient.sections():
  #      print(f"[{section}]")
  #      for key, value in configOutForClient.items(section):
  #          print(f"{key} = {value}")
  #      print()
  #  print("###########################################################")

    for section, options in dataDict.items():
        config.add_section(section)
        for option, value in options.items():
            config.set(section, option, value)
 

    if(not shipName0 == "none"): 
        ship0 = readShip(configIn,shipName0,x=configIn1.get("spawnLocations","teamBlue1X"), y=configIn1.get("spawnLocations","teamBlue1Y"),outline="white",owner="player1",id = "0", color = "white")
        ship0Client = readShip(configIn,shipName0,x=configIn1.get("spawnLocations","teamBlue1X"), y=configIn1.get("spawnLocations","teamBlue1Y"),outline="red",owner = "ai1",id = "3",color = "red")
        configOut.add_section('Player')
        configOutForClient.add_section('Enemy')
        writeShip(ship0,"Player",configOut)       
        writeShip(ship0Client,"Enemy",configOutForClient)  

    if(not shipName1 == "none"):  
        ship1 = readShip(configIn,shipName1,x=configIn1.get("spawnLocations","teamBlue2X"), y=configIn1.get("spawnLocations","teamBlue2Y"),outline="white",owner="player1",id = "1", color = "white")
        ship1Client = readShip(configIn,shipName1,x=configIn1.get("spawnLocations","teamBlue2X"), y=configIn1.get("spawnLocations","teamBlue2Y"),outline="red",owner = "ai1",id = "4",color = "red")
        configOut.add_section('Player2')
        configOutForClient.add_section('Enemy2')
        writeShip(ship1,"Player2",configOut)   
        writeShip(ship1Client,"Enemy2",configOutForClient)   
        
    if(not shipName2 == "none"):     
        ship2 = readShip(configIn,shipName2,x=configIn1.get("spawnLocations","teamBlue3X"), y=configIn1.get("spawnLocations","teamBlue3Y"),outline="white",owner="player1",id = "2", color = "white")
        ship2Client = readShip(configIn,shipName2,x=configIn1.get("spawnLocations","teamBlue3X"), y=configIn1.get("spawnLocations","teamBlue3Y"),outline="red",owner = "ai1",id = "5",color = "red")
        configOut.add_section('Player3')
        configOutForClient.add_section('Enemy3')
        writeShip(ship2,"Player3",configOut)     
        writeShip(ship2Client,"Enemy3",configOutForClient)

    if(config.has_section('Player')):
        ship3 = readMultiplayerShip(config,'Player',x=configIn1.get("spawnLocations","teamRed1X"), y=configIn1.get("spawnLocations","teamRed1Y"),outline="red",owner = "ai1",id = "3",color = "red")
        ship3ForClient = readMultiplayerShip(config,'Player',x=configIn1.get("spawnLocations","teamRed1X"), y=configIn1.get("spawnLocations","teamRed1Y"),outline="white",owner = "player1",id = "0",color = "white")
        configOut.set("Ships", "enemyName",ship3.name)
        configOutForClient.set("Ships", "playerName",ship3.name)      
        configOut.add_section('Enemy')
        configOutForClient.add_section('Player')
        writeShip(ship3,'Enemy',configOut)
        writeShip(ship3ForClient,'Player',configOutForClient)

    if(config.has_section('Player2')):
        ship4 = readMultiplayerShip(config,'Player2',x=configIn1.get("spawnLocations","teamRed2X"), y=configIn1.get("spawnLocations","teamRed2Y"),outline="red",owner = "ai1",id = "4",color = "red")
        ship4ForClient = readMultiplayerShip(config,'Player2',x=configIn1.get("spawnLocations","teamRed2X"), y=configIn1.get("spawnLocations","teamRed2Y"),outline="white",owner = "player1",id = "1",color = "white")
        configOut.set("Ships", "enemyName2",ship4.name)
        configOutForClient.set("Ships", "playerName2",ship4.name)
        configOut.add_section('Enemy2')
        configOutForClient.add_section('Player2')
        writeShip(ship4,'Enemy2',configOut)
        writeShip(ship4ForClient,'Player2',configOutForClient)


    if(config.has_section('Player3')):
        ship5 = readMultiplayerShip(config,'Player3',x=configIn1.get("spawnLocations","teamRed3X"), y=configIn1.get("spawnLocations","teamRed3Y"),outline="red",owner = "ai1",id = "5",color = "red")
        ship5ForClient = readMultiplayerShip(config,'Player3',x=configIn1.get("spawnLocations","teamRed3X"), y=configIn1.get("spawnLocations","teamRed3Y"),outline="white",owner = "player1",id = "2",color = "white")
        configOut.set("Ships", "enemyName3",ship5.name)
        configOutForClient.set("Ships", "playerName3",ship5.name)
        configOut.add_section('Enemy3')
        configOutForClient.add_section('Player3')
        writeShip(ship5,'Enemy3',configOut)
        writeShip(ship5ForClient,'Player3',configOutForClient)



    ### send game ready data to client
    #Convert the configparser object into a Python dictionary
    config_dict = {section: dict(configOutForClient[section]) for section in configOutForClient.sections()}

    #Convert the Python dictionary into JSON format using json module
    configJson = json.dumps(config_dict, indent=4)
    data = configJson
    data = fill_data_to_size(data,65536)
    multiplayerOptions.clientSocket.send(data.encode())             ### send info to client

    print("#################################################################################")
    #for section in configOut.sections():
    #    print(f"[{section}]")
    #    for key, value in configOut.items(section):
    #        print(f"{key} = {value}")
    #    print()
    
  #  FlushListen(multiplayerOptions.clientSocket)

    run(configOut,root,menuUiElements, multiplayerOptions)


def sendReadiness(info,configIn,root,uiMenuElements,multiplayerOptions,menuUiElements):
    shipName0 = (info.blueShip0).get()
    shipName1 = (info.blueShip1).get()
    shipName2 = (info.blueShip2).get()

    configIn1 = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    a = ("maps\\" + info.mapChoice.get() +"\mapInfo.ini")
    filePath = os.path.join(cwd, a)
    configIn1.read(filePath)
      
    configOut = configparser.ConfigParser()

    if(not (info.blueShip0).get() == "none"):
        if(not configOut.has_section('Player')):
            configOut.add_section('Player')
        ship0 = readShip(configIn,shipName0,x=0, y=0,outline="white",owner="player1",id = "0", color = "white")
    else:
        if(configOut.has_section('Player')):
            configOut.remove_section('Player')


    if(not (info.blueShip1).get() == "none"):
        if(not configOut.has_section('Player2')):
            configOut.add_section('Player2')
        ship1 = readShip(configIn,shipName1,x=0, y=0,outline="white",owner="player1",id = "1", color = "white")
    else:
        if(configOut.has_section('Player2')):
            configOut.remove_section('Player2')


    if(not (info.blueShip2).get() == "none"):
        ship2 = readShip(configIn,shipName2,x=0, y=0,outline="white",owner="player1",id = "2", color = "white")
        if(not configOut.has_section('Player3')):
            configOut.add_section('Player3')
    else:
        if(configOut.has_section('Player3')):
            configOut.remove_section('Player3')



    if(not (info.blueShip0).get() == "none"):
        writeShip(ship0,"Player",configOut)
    if(not (info.blueShip1).get() == "none"):
        writeShip(ship1,"Player2",configOut)
    if(not (info.blueShip2).get() == "none"):
        writeShip(ship2,"Player3",configOut)
        

    #Convert the configparser object into a Python dictionary
    config_dict = {section: dict(configOut[section]) for section in configOut.sections()}

    #Convert the Python dictionary into JSON format using json module
    configJson = json.dumps(config_dict, indent=4)
    data = configJson

    multiplayerOptions.clientSocket.send(data.encode())
    configOut = configparser.ConfigParser()
    configOut = multiplayerOptions.clientSocket.recv(65536).decode()
    multiplayerOptions.clientSocket.recv(0)
    dataDict = json.loads(configOut)

    # Step 2: Convert the dictionary to configparser format
    config = configparser.ConfigParser()

    for section, options in dataDict.items():
        config.add_section(section)
        for option, value in options.items():
            config.set(section, option, value)

 #  FlushListen(multiplayerOptions.clientSocket)
 #  FlushListen(multiplayerOptions.serverSocket)
    run(config,root,menuUiElements, multiplayerOptions)

