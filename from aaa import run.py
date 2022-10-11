
from ctypes import pointer
from dis import dis
from email.policy import default
from faulthandler import disable
from tabnanny import check
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, Frame, BOTH
from random import randint
import math
from PIL import Image, ImageTk
import PIL.Image
import tkinter.ttk as ttk
from functools import partial
import configparser
import os

from aaa import *
from shipCombat import *
from canvasCalls import *

class _events():
    playerDestroyed = False
    showedWin = False

if __name__ == '__main__':
    parameter1 = "1.Exiled-To-Make-A-Stand"
    parameter1 = "2.Warcries-That-Shred-The-Clouds"
    config = configparser.ConfigParser()
    cwd = os.getcwd()
    filePath = os.path.join(cwd, "maps",parameter1,"level info.ini")
    config.read(filePath)

    uiMetrics = ui_metrics()
    globalVar = global_var(config)
    gameRules = game_rules()
    ammunitionType = ammunition_type()
    uiIcons = ui_icons()
    shipLookup = dict
    events = _events()
    uiElements = ui_elements()
    canvas = Canvas(root, width=uiMetrics.canvasWidth,
                        height=uiMetrics.canvasHeight)
    globalVar.playerName = (config.get("Ships", "playerName"))
    globalVar.playerName2 = (config.get("Ships", "playerName2"))
    globalVar.playerName3 = (config.get("Ships", "playerName3"))

    globalVar.enemyName =  (config.get("Ships", "enemyName"))
    globalVar.enemyName2 = (config.get("Ships", "enemyName2"))
    globalVar.enemyName3 = (config.get("Ships", "enemyName3"))
    player = ship(owner="player1", \
                name=globalVar.playerName, shields=int((config.get("Player", "shields"))), xPos=int((config.get("Player", "xPos"))), yPos=int((config.get("Player", "yPos"))),
                systemSlots=((config.get("Player", "systemSlots1")),(config.get("Player", "systemSlots2")),(config.get("Player", "systemSlots3")),(config.get("Player", "systemSlots4")), \
                (config.get("Player", "systemSlots5")),(config.get("Player", "systemSlots2")),(config.get("Player", "systemSlots6")),(config.get("Player", "systemSlots7")),\
                (config.get("Player", "systemSlots8"))), detectionRange=int(config.get("Player", "detectionRange")), turnRate = float(config.get("Player", "turnRate")),\
                maxSpeed = int((config.get("Player", "maxSpeed"))),outlineColor = ((config.get("Player", "outlineColor"))))
    player2 = ship( owner="player1", \
                name=globalVar.playerName2, shields=int((config.get("Player2", "shields"))), xPos=int((config.get("Player2", "xPos"))), yPos=int((config.get("Player2", "yPos"))),
                systemSlots=((config.get("Player2", "systemSlots1")),(config.get("Player2", "systemSlots2")),(config.get("Player2", "systemSlots3")),(config.get("Player2", "systemSlots4")), \
                (config.get("Player2", "systemSlots5")),(config.get("Player2", "systemSlots2")),(config.get("Player2", "systemSlots6")),(config.get("Player2", "systemSlots7")),\
                (config.get("Player2", "systemSlots8"))), detectionRange=int(config.get("Player2", "detectionRange")), turnRate = float(config.get("Player2", "turnRate")),\
                maxSpeed = int((config.get("Player2", "maxSpeed"))),outlineColor = ((config.get("Player2", "outlineColor"))))
    player3 = ship( owner="player1", \
                name=globalVar.playerName3, shields=int((config.get("Player3", "shields"))), xPos=int((config.get("Player3", "xPos"))), yPos=int((config.get("Player3", "yPos"))),
                systemSlots=((config.get("Player3", "systemSlots1")),(config.get("Player3", "systemSlots2")),(config.get("Player3", "systemSlots3")),(config.get("Player3", "systemSlots4")), \
                (config.get("Player3", "systemSlots5")),(config.get("Player3", "systemSlots2")),(config.get("Player3", "systemSlots6")),(config.get("Player3", "systemSlots7")),\
                (config.get("Player3", "systemSlots8"))), detectionRange=int(config.get("Player3", "detectionRange")), turnRate = float(config.get("Player3", "turnRate")), \
                maxSpeed = int((config.get("Player3", "maxSpeed"))),outlineColor = ((config.get("Player3", "outlineColor"))))

    enemy = ship(owner="ai1", \
                name=globalVar.enemyName, shields=int((config.get("Enemy", "shields"))), xPos=int((config.get("Enemy", "xPos"))), yPos=int((config.get("Enemy", "yPos"))),
                systemSlots=((config.get("Enemy", "systemSlots1")),(config.get("Enemy", "systemSlots2")),(config.get("Enemy", "systemSlots3")),(config.get("Enemy", "systemSlots4")), \
                (config.get("Enemy", "systemSlots5")),(config.get("Enemy", "systemSlots2")),(config.get("Enemy", "systemSlots6")),(config.get("Enemy", "systemSlots7")),\
                (config.get("Enemy", "systemSlots8"))), detectionRange=int(config.get("Enemy", "detectionRange")), turnRate = float(config.get("Enemy", "turnRate")),\
                maxSpeed = int((config.get("Enemy", "maxSpeed"))),outlineColor = ((config.get("Enemy", "outlineColor"))))
    enemy2 = ship( owner="ai1", \
                name=globalVar.enemyName2, shields=int((config.get("Enemy2", "shields"))), xPos=int((config.get("Enemy2", "xPos"))), yPos=int((config.get("Enemy2", "yPos"))),
                systemSlots=((config.get("Enemy2", "systemSlots1")),(config.get("Enemy2", "systemSlots2")),(config.get("Enemy2", "systemSlots3")),(config.get("Enemy2", "systemSlots4")), \
                (config.get("Enemy2", "systemSlots5")),(config.get("Enemy2", "systemSlots2")),(config.get("Enemy2", "systemSlots6")),(config.get("Enemy2", "systemSlots7")),\
                (config.get("Enemy2", "systemSlots8"))), detectionRange=int(config.get("Enemy2", "detectionRange")), turnRate = float(config.get("Enemy2", "turnRate")),\
                maxSpeed = int((config.get("Enemy2", "maxSpeed"))),outlineColor = ((config.get("Enemy2", "outlineColor"))))
    enemy3 = ship( owner="ai1", \
                name=globalVar.enemyName3, shields=int((config.get("Enemy3", "shields"))), xPos=int((config.get("Enemy3", "xPos"))), yPos=int((config.get("Enemy3", "yPos"))),
                systemSlots=((config.get("Enemy3", "systemSlots1")),(config.get("Enemy3", "systemSlots2")),(config.get("Enemy3", "systemSlots3")),(config.get("Enemy3", "systemSlots4")), \
                (config.get("Enemy3", "systemSlots5")),(config.get("Enemy3", "systemSlots2")),(config.get("Enemy3", "systemSlots6")),(config.get("Enemy3", "systemSlots7")),\
                (config.get("Enemy3", "systemSlots8"))), detectionRange=int(config.get("Enemy3", "detectionRange")), turnRate = float(config.get("Enemy3", "turnRate")), \
                maxSpeed = int((config.get("Enemy3", "maxSpeed"))),outlineColor = ((config.get("Enemy3", "outlineColor"))))


    root.bind('<Motion>', motion)
    root.bind('<Button-1>', mouseButton1)
    root.bind('<Button-2>', mouseButton3)
    root.bind('<ButtonRelease-2>', mouseButton3up)
    root.bind('<MouseWheel>', mouseWheel)

    uiElements.rootTitle = (config.get("Root", "title"))
    root.title(uiElements.rootTitle)
    getZoomMetrics()

    # Ships

    (globalVar.ships).append(player)
    (globalVar.ships).append(player2)
    (globalVar.ships).append(player3)

    (globalVar.ships).append(enemy)
    (globalVar.ships).append(enemy2)
    (globalVar.ships).append(enemy3)


    shipLookup = {
    globalVar.playerName: player,
    globalVar.enemyName: enemy,
    globalVar.playerName2: player2,
    globalVar.enemyName2: enemy2,
    globalVar.playerName3: player3,
    globalVar.enemyName3: enemy3}
    run(uiMetrics,globalVar,gameRules,ammunitionType,uiIcons,shipLookup,events,uiElements,canvas)
