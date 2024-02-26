from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from functools import partial
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




def statusWaitingForServer(multiplayerOptions):
    multiplayerOptions.statusLabel.config(text = "Waiting for server readiness")

def statusWaitingForClient(multiplayerOptions):
    multiplayerOptions.statusLabel.config(text = "Waiting for client readiness")


def encodeChoices(var,multiplayerOptions):
    config = configparser.ConfigParser()    
    i = 0
    for ship in var.ships:
        if(not ship.owner == 'player1'):
            continue
        config.add_section('ship' + str(i))
        encodeShip(var,config,'ship'+ str(i),ship)
        i+=1
    
    return config


def encodeShip(var,config,section,ship):
    config.set(section, "shipX", str(ship.xPos))
    config.set(section, "shipY", str(ship.yPos))
    config.set(section, "shipHp", str(ship.hp))
    config.set(section, "shipAp", str(ship.ap))
    if(ship.killed):
        config.set(section, "shipkilled", '1')
    else:
        config.set(section, "shipkilled", '0')
    if(ship.targetOnly):
        config.set(section, "shiptargetOnly", '1')
    else:
        config.set(section, "shiptargetOnly", '0')
    config.set(section, "shipmoveOrderX", str(ship.moveOrderX))
    config.set(section, "shipmoveOrderY", str(ship.moveOrderY))
    i = 0
    for shield in range(ship.maxShields):
        config.set(section, "shield" + str(i), str(ship.shieldsState[i]))
        i+=1
    i = 0
    for system in ship.systemSlots:
        config.set(section, "system" + str(i) + "energy" + str(i), str(ship.systemSlots[i].energy))
        config.set(section, "system" + str(i) + "integrity" + str(i), str(ship.systemSlots[i].integrity))
        config.set(section, "system" + str(i) + "cooldown" + str(i), str(ship.systemSlots[i].cooldown))
        config.set(section, "system" + str(i) + "cooling" + str(i), str(ship.systemSlots[i].cooling))
        config.set(section, "system" + str(i) + "heat" + str(i), str(ship.systemSlots[i].heat))
        config.set(section, "system" + str(i) + "coolUnits" + str(i), str(ship.systemSlots[i].coolUnits))
        config.set(section, "system" + str(i) + "heatUnits" + str(i), str(ship.systemSlots[i].heatUnits))
        config.set(section, "system" + str(i) + "heatDamageTicks" + str(i), str(ship.systemSlots[i].heatDamageTicks))
        if(system.category == 'weapon'):
            config.set(section, "system" + str(i) + "target" + str(i), str(ship.systemSlots[i].target))
            config.set(section, "system" + str(i) + "ASButton" + str(i), str(ship.systemSlots[i].ASButton))
            config.set(section, "system" + str(i) + "alphaStrike" + str(i), str(ship.systemSlots[i].alphaStrike))
            config.set(section, "system" + str(i) + "hold" + str(i), str(ship.systemSlots[i].hold))
            config.set(section, "system" + str(i) + "delay" + str(i), str(ship.systemSlots[i].delay))
            config.set(section, "system" + str(i) + "desynchronise" + str(i), str(ship.systemSlots[i].desynchronise))
            config.set(section, "system" + str(i) + "shotThisTurn" + str(i), str(ship.systemSlots[i].shotThisTurn))
        i+=1

def decodeChoices(var, config):
    i = 0
    for ship in var.ships:
        if(ship.owner == 'player1'):
            continue
        section = 'ship' + str(i)
        print(config.get(section, "shipX"))
        ship.xPos = float(config.get(section, "shipX"))
        ship.yPos = float(config.get(section, "shipY"))
        ship.hp = int(config.get(section, "shipHp"))
        ship.ap = int(config.get(section, "shipAp"))
        kill = config.get(section, "shipkilled")
        if(kill == 'True'):
            ship.killed = True
        ship.moveOrderX = float(config.get(section, "shipmoveOrderX"))
        ship.moveOrderY = float(config.get(section, "shipmoveOrderY"))
        ship.targetOnly = float(config.get(section, "shiptargetOnly"))
        i = 0
        for shield in range(ship.maxShields):
            config.set(section, "shield" + str(i), str(ship.shieldsState[i]))
            i+=1
        i = 0
        for system in ship.systemSlots:
            system.energy  =        int(config.get(section, "system" + str(i) + "energy" + str(i)))
            system.integrity   =    int(config.get(section, "system" + str(i) + "integrity" + str(i)))
            system.cooldown   =     float(config.get(section, "system" + str(i) + "cooldown" + str(i)))
            system.cooling   =      float(config.get(section, "system" + str(i) + "cooling" + str(i)))
            system.heat     =       float(config.get(section, "system" + str(i) + "heat" + str(i)))
            system.coolUnits    =   float(config.get(section, "system" + str(i) + "coolUnits" + str(i)))
            system.heatUnits   =    float(config.get(section, "system" + str(i) + "heatUnits" + str(i)))
            system.heatDamageTicks= float(config.get(section, "system" + str(i) + "heatDamageTicks" + str(i)))
            if(system.category == 'weapon'):
                config.set(section, "system" + str(i) + "target" + str(i), str(ship.systemSlots[i].target))
                config.set(section, "system" + str(i) + "ASButton" + str(i), str(ship.systemSlots[i].ASButton))
                config.set(section, "system" + str(i) + "alphaStrike" + str(i), str(ship.systemSlots[i].alphaStrike))
                config.set(section, "system" + str(i) + "hold" + str(i), str(ship.systemSlots[i].hold))
                config.set(section, "system" + str(i) + "delay" + str(i), str(ship.systemSlots[i].delay))
                config.set(section, "system" + str(i) + "desynchronise" + str(i), str(ship.systemSlots[i].desynchronise))
                config.set(section, "system" + str(i) + "shotThisTurn" + str(i), str(ship.systemSlots[i].shotThisTurn))
            i+=1