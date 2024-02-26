import configparser
import sys
import os
import tkinter as tk
import tkinter.ttk as ttk
from ctypes import pointer
from dis import dis
from ensurepip import bootstrap
from faulthandler import disable
from functools import partial
from pathlib import Path
from tabnanny import check
from tkinter import BOTH, Canvas
from tkinter.filedialog import askopenfilename
import random as random
from tabnanny import check
from tkinter.filedialog import askopenfilename
import PIL.Image
from tkinter import PhotoImage,HORIZONTAL
import gc
import atexit

import src.settings as settings
from src.objects.ship import ship
from src.update import dragging,checkForKilledShips,update,newWindow,putTracer,updateLabels,radioBox,endTurn,updateBattleUi,detectionCheck,manageLandmarks,pauseGame
from src.shipCombat import getZoomMetrics
from src.aiControllers import aiController
from src.turnManagers import startTurn
from src.inputs import mouseButton3,mouseWheel,motion,mouseButton1,mouseButton3up
from src.canvasCalls import createMask,createPFMask
from src.endConditions import finishSetTrue
from src.winConditionsLoader import loadWinConditions
from src.editor.ammunitionType import ammunition_type
from src.rootCommands import placeMenuUi,hideBattleUi
from src.editor.systems import loadSounds

def declareTargets(var):
    list1 = {}
    list2 = {}
    for ship in var.ships:
        if(not ship.owner == 'player1'):
            if(not ship.name in list1):
                list1.update({ship.name : ship.id})
            else:
                i = 2
                while((ship.name + ' (' + str(i) + ')') in list1):
                    i+=1
                ship.name = (ship.name + ' (' + str(i) + ')')
                list1.update({ship.name : ship.id})
    for ship1 in var.ships:
        if(ship1.owner == 'player1'):
            if(not ship1.name in list2):
                list2.update({ship1.name : ship1.id})
            else:
                i = 2
                while((ship1.name + ' (' + str(i) + ')') in list2):
                    i+=1
                ship1.name = (ship1.name + ' (' + str(i) + ')')
                list2.update({ship1.name : ship1.id})
    return list1,list2

def bindInputs(root,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,config,menuUiElements, multiplayerOptions):
    root.bind('<Motion>', lambda e: motion(e, var,root))
    root.bind('<Button-1>', lambda e: mouseButton1(e, var))
    root.bind('<space>', lambda e: startTurn(uiElements,var,var.ships,gameRules,uiMetrics,multiplayerOptions,root))
    root.bind('p', lambda e: pauseGame(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions))
    root.bind('<Button-2>', lambda e: mouseButton3(e, var))
    root.bind('<ButtonRelease-2>', lambda e: mouseButton3up(e, var))
    root.bind('<MouseWheel>', lambda e: mouseWheel(e, var,uiMetrics))
    root.bind('<Configure>', lambda e: dragging(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions))

def onExit(var):
    for t in var.t1:
        t._stop()
######################################################### MAIN ####################################

def declareSystemTargets(var,shipLookup):
    for ship in var.ships:
        list1 = {}
        i = 2
        for system in ship.systemSlots:
            if(not system.name in list1):
                list1.update({system.name : system.id})
            else:
                while((system.name + ' (' + str(i) + ')') in list1):
                    i+=1
                system.name = (system.name + ' (' + str(i) + ')')
                list1.update({system.name : system.id})
            if(system.category == 'weapon'):
                system.setTargetStr(-1)
                    #shipLookup[var.enemies[list(var.enemies.keys())[0]]].systemSlots[0])


def declareShipsTargets(var):
    for ship in var.ships:
        if(ship.owner == 'player1'):
            ship.setTargetStr(list(var.enemies.keys())[0])
            continue
        if(ship.owner == 'ai1'):
            ship.setTargetStr(list(var.players.keys())[0])


def declareShips(var,config,events,shipLookup,uiElements,uiMetrics,root,canvas,multiplayerOptions):

        var.player = 0
        var.player2 = 0
        var.player3 = 0

        var.enemy = 0
        var.enemy2 = 0
        var.enemy3 = 0

        creationList = [var.player, var.player2,var.player3,var.enemy,var.enemy2,var.enemy3]
        configList = ["Player", "Player2", "Player3", "Enemy", "Enemy2", "Enemy3"]
        i=0
        for element in creationList:
            if(i<=2):               #change if more ships
                owner1 = "player1"
            else:
                owner1 = "ai1"
            creationList[i] = ship(var, owner=owner1, name=">Not Available<")
            creationList[i].id = i
            creationList[i].hp = 0
            if(config.has_section(configList[i])):
             #   print("has")
                creationList[i].name = config.get(configList[i], "name")
                creationList[i].color = config.get(configList[i], "color")
                creationList[i].declareShieldState(int((config.get(configList[i], "shields"))),int((config.get(configList[i], "maxShields"))),var)
                creationList[i].energyLimit=int((config.get(configList[i], "energyLimit")))
                creationList[i].tmpEnergyLimit=int((config.get(configList[i], "energyLimit")))
                creationList[i].energy=int((config.get(configList[i], "energyLimit")))        
                creationList[i].xPos=int((config.get(configList[i], "xPos")))
                creationList[i].yPos=int((config.get(configList[i], "yPos")))
                creationList[i].declareSystemSlots(
                    [(config.get(configList[i], "systemSlots1")),
                    config.get(configList[i], "systemSlots2"),
                    config.get(configList[i], "systemSlots3"),
                    config.get(configList[i], "systemSlots4"),
                    config.get(configList[i], "systemSlots5"),
                    config.get(configList[i], "systemSlots6")],
                    [(config.get(configList[i], "systemStatus1")),
                    (config.get(configList[i], "systemStatus2")),
                    (config.get(configList[i], "systemStatus3")),
                    (config.get(configList[i], "systemStatus4")),
                    (config.get(configList[i], "systemStatus5")),
                    (config.get(configList[i], "systemStatus6"))]
                    )
                creationList[i].speed = float(config.get(configList[i], "speed"))
                creationList[i].ghostPoints = []
                creationList[i].signatures = []
                creationList[i].detectionRange=int(config.get(configList[i], "detectionRange"))
                creationList[i].turnRate = float(config.get(configList[i], "turnRate"))
                creationList[i].maxSpeed = float(config.get(configList[i], "maxSpeed"))
                creationList[i].outlineColor = ((config.get(configList[i], "outlineColor")))
                creationList[i].hp = int((config.get(configList[i], "hp")))
                creationList[i].maxHp = int((config.get(configList[i], "hp")))
                creationList[i].ap = int((config.get(configList[i], "ap")))
                creationList[i].maxAp = int((config.get(configList[i], "ap")))
                creationList[i].stance = ((config.get(configList[i], "stance")))
                creationList[i].killed = False
            i+=1
        checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas,multiplayerOptions)
        
        var.player = creationList[0]
        var.ships.append(var.player)
        var.player2 = creationList[1]
        var.ships.append(var.player2)
        var.player3 = creationList[2]
        var.ships.append(var.player3)
        var.enemy = creationList[3]
        var.ships.append(var.enemy)
        var.enemy2 = creationList[4]
        var.ships.append(var.enemy2)
        var.enemy3 = creationList[5]
        var.ships.append(var.enemy3)


def declareLandmarks(var,config):
        configList = ["Landmark0", "Landmark1", "Landmark2", "Landmark3","Landmark4", "Landmark5", "Landmark6","Landmark7"]
        i=0
        while (i < 8):
            if(config.has_section(configList[i])):
                if(config.get(configList[i], "visible") == '1'):
                    _visible = True
                else:
                    _visible = False

                var.landmarks.append(settings.landmark( xPos = float(config.get(configList[i], "xPos")),
                yPos = float(config.get(configList[i], "yPos")),
                cooldown = float(config.get(configList[i], "cooldown")),
                defaultCooldown = float(config.get(configList[i], "cooldown")),
                radius = float(config.get(configList[i], "radius")),
                boost = config.get(configList[i], "boost"),
                visible = _visible,
                id = i
                ))
            i+=1
        if config.has_option('Meta', 'deleteRandomLandmarks'):
            toDelete = int(config.get("Meta", "deleteRandomLandmarks"))
            while toDelete:
                id = random.randrange(len(var.landmarks))
              #  randomLandmark = var.landmarks[id]
                var.landmarks.pop(id)
                toDelete -= 1
        
def saveCurrentGame(var):   
    config = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    filePath = os.path.join(cwd, "gameData","currentGame.ini")
    config.read(filePath)

    creationList = [var.player, var.player2,var.player3,var.enemy,var.enemy2,var.enemy3]
    #nameList = [var.playerName, var.playerName2, var.playerName3, var.enemyName, var.enemyName2, var.enemyName3]
    configList = ["Player", "Player2", "Player3", "Enemy", "Enemy2", "Enemy3"]
    i=0
    for element in creationList:
        if(not config.has_section(configList[i])):
            config.add_section(configList[i])
        config.set(configList[i], "owner",element.owner)
        config.set(configList[i],"name",element.name)
        config.set(configList[i], "maxShields",str(element.maxShields)),
        config.set(configList[i], "shields",str(element.shields)), 
        config.set(configList[i], "xPos",str(element.xPos)), 
        config.set(configList[i], "yPos",str(element.yPos)),
        j=0
        for system in element.systemSlots:
            config.set(configList[i], ("systemSlots" + str(j+1)),element.systemSlots[j].name)
            config.set(configList[i], ("systemStatus" + str(j+1)),str((element.systemSlots[j]).cooldown))
            j+=1
        config.set(configList[i], "speed",str(element.speed)), 
        config.set(configList[i], "detectionRange",str(element.detectionRange)), 
        config.set(configList[i], "turnRate",str(element.turnRate)),
        config.set(configList[i], "maxSpeed",str(element.maxSpeed)),
        config.set(configList[i], "outlineColor",element.outlineColor),
        config.set(configList[i], "hp",str(element.hp)), 
        config.set(configList[i], "id",str(element.id)),
        config.set(configList[i], "ap",str(element.ap))
        i+=1

    hd = open(filePath, "w")
    config.write(hd)
    hd.close()
        #### wip
def run(config,root,menuUiElements, multiplayerOptions):
 #   tracemalloc.start()
   # print(naglowek.combatUiReady)
    if(settings.combatUiReady):
        cinfo = settings.combatSystemInfo
        settings.combatUiReady = False
        for element in ((settings.combatSystemInfo).canvas).imageList :
            del element
        del (settings.combatSystemInfo).canvas           
        del (settings.combatSystemInfo).uiMetrics        
        for element in ((settings.combatSystemInfo).uiElements).staticUi:
            element.destroy()
        for element in (cinfo.var).playerShields:
            element.destroy()
        for element in (cinfo.var).playerShields2:
            element.destroy()
        for element in (cinfo.var).playerShields3:
            element.destroy()
        for element in (cinfo.var).enemyShields:
            element.destroy()
        for element in (cinfo.var).enemyShields2:
            element.destroy()
        for element in (cinfo.var).enemyShields3:
            element.destroy()
        for widget in ((cinfo.uiElements).systemsLF).winfo_children():
            widget.destroy()
        for element in ((cinfo.var).shipChoiceRadioButtons):
            element.destroy()
        for element in ((cinfo.uiElements).UIElementsList):
            element.destroy()
        for key, element in cinfo.shipLookup.items():
            del element
        for element in cinfo.uiElements.uiSystemsProgressbars:
            element.destroy()

        cinfo.var.uiTargetOnlyCB.destroy()
        del cinfo.uiElementsToPlace      
        del cinfo.var.mask 
        del cinfo.var.PFMask 
        cinfo.uiElements.enemyLF.destroy()
        cinfo.uiElements.enemyLF2.destroy()
        cinfo.uiElements.enemyLF3.destroy()
        cinfo.uiElements.playerLF.destroy()
        cinfo.uiElements.playerLF2.destroy()
        cinfo.uiElements.playerLF3.destroy()

        cinfo.uiElements.systemsLF.destroy()
        del cinfo.uiElements.systemsLF
        cinfo.var.uiEnergyLabel.destroy()
        del cinfo.var.uiEnergyLabel
        del (cinfo.var).img
        del (cinfo.var).imgg
        del (cinfo.var).radio
        (cinfo.uiElements).uiSystems = []
        (cinfo.uiElements).uiSystemsProgressbars = []
        del(cinfo.var.image)
        del(cinfo.var.imageMask)
        del (cinfo.var)
        del (cinfo.gameRules)
        del (cinfo.ammunitionType)
        del (cinfo.uiIcons.armorIcon)
        del (cinfo.uiIcons.spotterIcon)
        del (cinfo.uiIcons.controlIconP)
        del (cinfo.uiIcons.controlIconE)
        del (cinfo.uiIcons.controlIconN)
        del cinfo.uiIcons
        del (cinfo.shipLookup)
        del (cinfo.events)
        del (cinfo.uiElements)
        gc.collect()
        del cinfo   ## par nowych sprawdz
  #      for child in root.winfo_children():
  #         print(str(child.winfo_height()) + str(child.winfo_parent()) + str(child) + '\n')
  #         #child.place(x=10,y=10)
  #      snapshot = tracemalloc.take_snapshot()
  #      top_stats = snapshot.statistics('traceback')
  #      i = 0
  #      stat = top_stats[i]
  #      while(True):
  #          try:
  #              stat = top_stats[i]
  #              for line in stat.traceback.format():
  #                  print(line)
  #              tracemalloc.stop()
  #              print("\n\n\n\n")
  #              i+=1
  #          except:
  #              break
    root.after_cancel("all")
    resume(config,root,menuUiElements, multiplayerOptions)
# main
def resume(config,root,menuUiElements, multiplayerOptions):
    if(not settings.combatUiReady):
        cwd = Path(sys.argv[0])
        cwd = str(cwd.parent)
        """
        rootX = root.winfo_screenwidth()
        rootY = root.winfo_screenheight()
        root.attributes('-fullscreen', True)
        """
        #root.deiconify()
        uiMetrics = settings.uiMetrics
        var = settings.global_var(config,root)
        loadSounds(var)
        gameRules = settings.game_rules()
        ammunitionType = ammunition_type()
        uiIcons = settings.ui_icons()
        shipLookup = dict
        events = settings._events()
        uiElements = settings.dynamic_object()
        uiElements.systemsLF = ttk.Labelframe(root,style = 'Green.TLabelframe', text= "" + " systems",borderwidth=2, width=uiMetrics.canvasWidth, height = uiMetrics.systemScalesLFHeight)
        uiElements.objectivesLF = ttk.Labelframe(root,style = 'Grey.TLabelframe', text= "Current objectives",borderwidth=2, width=uiMetrics.objectivesLFWidth,height = uiMetrics.objectivesLFHeight)
        uiElements.objectivesL = ttk.Label(uiElements.objectivesLF,style = 'Grey.TLabel',justify = "left", text= "")
        uiElements.objectivesL.config(text = config.get("Meta", "objectives", fallback = "Objective 1\nObjective 2\nObjective 3"))
        uiElements.staticUi = []
        uiIcons.armorIcon = PhotoImage(file=os.path.join(cwd, "icons","armor.png"))
        uiIcons.spotterIcon = PhotoImage(file=os.path.join(cwd, "icons","spotter.png"))
        uiIcons.controlIconP = PhotoImage(file=os.path.join(cwd, "icons","controlP.png"))
        uiIcons.controlIconE = PhotoImage(file=os.path.join(cwd, "icons","controlE.png"))
        uiIcons.controlIconN = PhotoImage(file=os.path.join(cwd, "icons","controlN.png"))

        # canvas
        var.image = PIL.Image.open(os.path.join(cwd, config.get("Images", "img")))
        var.imageMask = PIL.Image.open(os.path.join(cwd, config.get("Images", "imageMask")))
        var.w,var.h = (var.image).size
        scaleX = var.w / uiMetrics.canvasWidth
        scaleY = var.h / uiMetrics.canvasHeight
        imgRatio = int(var.w/var.h)
        if(scaleX > scaleY):
            uiMetrics.canvasWidth = int(var.w/scaleX)
            uiMetrics.canvasHeight = int((var.h/scaleX))

            var.image = var.image.resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight))
            var.imageMask = var.imageMask.resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight))
        else:
            uiMetrics.canvasWidth = int(var.w/scaleY)
            uiMetrics.canvasHeight = int(var.h/scaleY)
            var.image = var.image.resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight))
            var.imageMask = var.imageMask.resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight))
      #  var.img = var.img.resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight))
        canvas = tk.Canvas(root, width=uiMetrics.canvasWidth, height=uiMetrics.canvasHeight,relief="raised")
        canvas.ovalList = []
        canvas.availableOvalList = []
        tmp = uiIcons.armorIcon 
        canvas.imageID = canvas.create_image(0,0,image = tmp)
        getZoomMetrics(var,uiMetrics)
        (uiElements.staticUi).append(canvas)
        declareShips(var,config,events,shipLookup,uiElements,uiMetrics,root,canvas,multiplayerOptions)
        uiElements.rootTitle = (config.get("Root", "title"))
        fog = (config.get("Options", "fogOfWar"))
        if(fog == '0'):
            var.fogOfWar = False
        else:
            var.fogOfWar = True


        # Ships
        shipLookup = {
            0: var.player,
            1: var.player2,
            2: var.player3,
            3: var.enemy,
            4: var.enemy2,
            5: var.enemy3
        }

        var.enemies,var.players = declareTargets(var)
        declareShipsTargets(var)
        declareSystemTargets(var,shipLookup)
        declareLandmarks(var,config)

        var.resizedImage = var.image
        canvas.imageList = []
        canvas.elements = []
        newWindow(uiMetrics,var,canvas,root)
        # item with background to avoid python bug people were mentioning about disappearing non-anchored images

        canvas.imageList.append(var.image)
        canvas.imageList.append(var.imageMask)
        canvas.imageList.append(var.resizedImage)

        var.mask = createMask(var,uiMetrics)                # environment collision map
        var.PFMask = createPFMask(var,uiMetrics)            # lower precision mask for ai to use

        uiElements.UIElementsList = []
        uiElements.RadioElementsList = []            
        uiElements.pausedL = ttk.Label(canvas, style = "Pause.TLabel", text = "Paused")

        uiElements.gameSpeedScale = tk.Scale(root, orient=HORIZONTAL, length=100, from_=3, to=30)
        uiElements.gameSpeedL = ttk.Label(root, style = 'Grey.TLabel', text = "Playback Speed:")
        var.img = tk.PhotoImage(file= os.path.join(cwd, config.get("Images", "img")))


        loadWinConditions(var,config)
        
        (uiElements.gameSpeedScale).set(8)
        uiElements.timeElapsedLabel = ttk.Label(root, style = 'Grey.TLabel', text="Time elapsed")
        uiElements.timeElapsedProgressBar = ttk.Progressbar(root, maximum=var.turnLength, variable=1,  orient='horizontal',
                                                mode='determinate', length=uiMetrics.shipDataWidth)

        uiElements.startTurnBFrame = tk.Frame(root)
        uiElements.exitToMenuBFrame = tk.Frame(root)
        uiElements.startTurnBFrame.config(bg="#4582ec", width=200, height=200,padx=1)
        uiElements.exitToMenuBFrame.config(bg="#4582ec", width=200, height=200,padx=1)

        uiElements.startTurnButton = tk.Button(uiElements.startTurnBFrame, text="Start turn", width = 20, height= 7, command=lambda:[startTurn(uiElements,var,var.ships,gameRules,uiMetrics,multiplayerOptions,root)])
        uiElements.exitToMenuButton = tk.Button(uiElements.exitToMenuBFrame, text="Exit to menu", width = 20, height= 7, command=lambda:[placeMenuUi(root,menuUiElements,uiMetrics), hideBattleUi(uiElements.staticUi,uiElements), finishSetTrue(var),saveCurrentGame(var)])

        uiElements.startTurnButton.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 10 normal'), highlightbackground="#4582ec")
        uiElements.exitToMenuButton.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 10 normal'), highlightbackground="#4582ec")

        uiElements.staticUi.append(uiElements.pausedL)
        uiElements.staticUi.append(uiElements.gameSpeedScale)
        uiElements.staticUi.append(uiElements.gameSpeedL)
        uiElements.staticUi.append(uiElements.timeElapsedLabel)
        uiElements.staticUi.append(uiElements.timeElapsedProgressBar)
        uiElements.staticUi.append(uiElements.startTurnButton)
        uiElements.staticUi.append(uiElements.exitToMenuButton)
        uiElements.staticUi.append(uiElements.objectivesLF)

        uiElements.staticUi.append(uiElements.startTurnBFrame)
        uiElements.staticUi.append(uiElements.exitToMenuBFrame)

        for ship1 in var.ships:
            if(ship1.owner == "player1"):
                putTracer(ship1,var,gameRules,uiMetrics)

        uiElements.playerLF = ttk.Labelframe(root,  text = shipLookup[0].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.playerLF2 = ttk.Labelframe(root, text = shipLookup[1].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.playerLF3 = ttk.Labelframe(root, text = shipLookup[2].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.enemyLF = ttk.Labelframe(root,   text = shipLookup[3].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.enemyLF2 = ttk.Labelframe(root,  text = shipLookup[4].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.enemyLF3 = ttk.Labelframe(root,  text = shipLookup[5].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
    

        var.playerShields = []
        var.playerShields2 = []
        var.playerShields3 = []
        var.enemyShields = []
        var.enemyShields2 = []
        var.enemyShields3 = []

        targets = [var.playerShields,var.playerShields2,var.playerShields3,var.enemyShields,var.enemyShields2,var.enemyShields3]
        ships = [var.player,var.player2,var.player3,var.enemy,var.enemy2,var.enemy3]
        labelframes = [uiElements.playerLF, uiElements.playerLF2, uiElements.playerLF3, uiElements.enemyLF,uiElements.enemyLF2, uiElements.enemyLF3]
        for target,ship1,labelframe in zip(targets,ships,labelframes):
            
            x = (ship1).maxShields
            n = 0
            if(ship1.maxShields == 1):
                lenGap = 0
                lenPro = 5
            else:
                lenGap = (ship1.maxShields-1)
                lenPro = (ship1.maxShields)*4
            lenTotal = lenGap + lenPro
            while(n < x):
                target.append(ttk.Progressbar(labelframe, maximum=100, length = (((lenPro/lenTotal)/ship1.maxShields)*(uiMetrics.systemsLFWidth - 15)),variable=100))
                n += 1

        for ship1 in var.ships:
            if(ship1.owner == "ai1"):
                aiController.moveOrderChoice(ship1,var.ships,var,gameRules,uiMetrics)

        ######################################################### PROGRESSBAR ASSIGNMENT ####################################

        (var.player).shieldsLabel = var.playerShields
        (var.player2).shieldsLabel = var.playerShields2
        (var.player3).shieldsLabel = var.playerShields3
        (var.enemy).shieldsLabel = var.enemyShields
        (var.enemy2).shieldsLabel = var.enemyShields2
        (var.enemy3).shieldsLabel = var.enemyShields3

        uiElements.tmpShieldsLabel = []
        uiElements.tmpShieldsLabel.append(var.playerShields)
        uiElements.tmpShieldsLabel.append(var.playerShields2)
        uiElements.tmpShieldsLabel.append(var.playerShields3)
        uiElements.tmpShieldsLabel.append(var.enemyShields)
        uiElements.tmpShieldsLabel.append(var.enemyShields2)
        uiElements.tmpShieldsLabel.append(var.enemyShields3)        # create list of elements to disable if round is in progress
        uiElements.UIElementsList.append(uiElements.gameSpeedScale)
      #  (uiElements.UIElementsList).append(uiElements.startTurnButton)
       # (uiElements.UIElementsList).append(uiElements.exitToMenuButton)

      #  (uiElements.staticUi).append(uiElements.systemsLabelFrame)

        uiElementsToPlace = uiElements
        
##################################

        uiElements.playerLabels = []
        uiElements.playerLabels2 = []
        uiElements.playerLabels3 = []
        uiElements.enemyLabels = []
        uiElements.enemyLabels2 = []
        uiElements.enemyLabels3 = []
        uiElements.systemLFs = []

        targets = [uiElements.playerLabels, uiElements.playerLabels2, uiElements.playerLabels3, uiElements.enemyLabels, uiElements.enemyLabels2, uiElements.enemyLabels3]


        (uiElements.staticUi).append(uiElements.playerLF)
        (uiElements.staticUi).append(uiElements.playerLF2)
        (uiElements.staticUi).append(uiElements.playerLF3)
        (uiElements.staticUi).append(uiElements.enemyLF)
        (uiElements.staticUi).append(uiElements.enemyLF2)
        (uiElements.staticUi).append(uiElements.enemyLF3)

        targetLFs = [uiElements.playerLF,uiElements.playerLF2,uiElements.playerLF3,uiElements.enemyLF,uiElements.enemyLF2,uiElements.enemyLF3]
        shipID = 0
        for target,targetLF in zip(targets,targetLFs):
            i = 0
      #      system = shipLookup[shipID].systemSlots[i] 
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Hull: "))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(shipLookup[shipID].hp)))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Armor: "))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(shipLookup[shipID].ap)))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = ""))

            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "System"))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Reload"))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Integrity"))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Heat"))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Energy"))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = ""))
            for element in shipLookup[shipID].systemSlots:
                system = shipLookup[shipID].systemSlots[i]
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = system.name))
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(round((system.cooldown/system.maxCooldown))*100)))
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(system.integrity)))
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(system.heat)))
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(system.energy)))
                af = tk.Frame(targetLF)
                af.config(bg="#4582ec", width=1, height=1,padx=1)
                a = tk.Button(af, text = '?')
                a.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 9 normal'), width = 2, height = 1)
                a.bind("<Button-1>", system.showInfo)
                a.pack()
                target.append(af)
                (uiElements.staticUi).append(target[i])
                i+=1
            shipID += 1

        uiElements.systemLFs.append(uiElements.playerLF)
        uiElements.systemLFs.append(uiElements.playerLF2)
        uiElements.systemLFs.append(uiElements.playerLF3)
        uiElements.systemLFs.append(uiElements.enemyLF)
        uiElements.systemLFs.append(uiElements.enemyLF2)
        uiElements.systemLFs.append(uiElements.enemyLF3)

        # ships choice
        var.shipChoiceRadioButtons = []
        radioCommand = partial(radioBox,shipLookup , uiElements,var,uiMetrics,root,canvas,uiElements.UIElementsList,multiplayerOptions)
        var.shipChoice = (var.player).name

        (uiElements.RadioElementsList).append(ttk.Radiobutton(root, style = "Grey.TRadiobutton", text=(shipLookup[0]).name, variable=var.radio, value=0, command=radioCommand))
        (uiElements.RadioElementsList).append(ttk.Radiobutton(root, style = "Grey.TRadiobutton", text=(shipLookup[1]).name, variable=var.radio, value=1, command=radioCommand))
        (uiElements.RadioElementsList).append(ttk.Radiobutton(root, style = "Grey.TRadiobutton", text=(shipLookup[2]).name, variable=var.radio, value=2, command=radioCommand))

        uiElements.shipChoiceRadioButton0 = uiElements.RadioElementsList[0]
        uiElements.shipChoiceRadioButton1 = uiElements.RadioElementsList[1]
        uiElements.shipChoiceRadioButton2 = uiElements.RadioElementsList[2]

        (var.shipChoiceRadioButtons).append(uiElements.RadioElementsList[0])
        (var.shipChoiceRadioButtons).append(uiElements.RadioElementsList[1])
        (var.shipChoiceRadioButtons).append(uiElements.RadioElementsList[2])
        
        (uiElements.staticUi).append(uiElements.RadioElementsList[0])
        (uiElements.staticUi).append(uiElements.RadioElementsList[1])
        (uiElements.staticUi).append(uiElements.RadioElementsList[2])

        radioBox(shipLookup,uiElements,var,uiMetrics,root,canvas,uiElements.UIElementsList,multiplayerOptions)
        bindInputs(root,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,config,menuUiElements, multiplayerOptions)
        
        atexit.register(onExit,var)
        
        uiElements.playerLF.bind("<Button-1>", lambda e: (var.radio.set(0), radioCommand()))
        uiElements.playerLF2.bind("<Button-1>", lambda e: (var.radio.set(1), radioCommand()))
        uiElements.playerLF3.bind("<Button-1>", lambda e: (var.radio.set(2), radioCommand()))

        for child in uiElements.playerLF.winfo_children():
            if(not isinstance(child, ttk.Button) and not isinstance(child, ttk.Frame) and not isinstance(child, tk.Button) and not isinstance(child, tk.Frame)):
                child.bind("<Button-1>", lambda e: (var.radio.set(0), radioCommand()))
        for child in uiElements.playerLF2.winfo_children():
            if(not isinstance(child, ttk.Button) and not isinstance(child, ttk.Frame) and not isinstance(child, tk.Button) and not isinstance(child, tk.Frame)):
                child.bind("<Button-1>", lambda e: (var.radio.set(1), radioCommand()))
        for child in uiElements.playerLF3.winfo_children():
            if(not isinstance(child, ttk.Button) and not isinstance(child, ttk.Frame) and not isinstance(child, tk.Button) and not isinstance(child, tk.Frame)):
                child.bind("<Button-1>", lambda e: (var.radio.set(2), radioCommand()))
            
        # first update 

        checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas,multiplayerOptions)
        detectionCheck(var,uiMetrics)
        endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root,multiplayerOptions)
        manageLandmarks(var.landmarks, var.ships,uiMetrics,events)
        newWindow(uiMetrics,var,canvas,root)
        updateLabels(uiElements,shipLookup,var,root)

        (settings.combatSystemInfo).canvas = canvas
        (settings.combatSystemInfo).uiMetrics = uiMetrics
        (settings.combatSystemInfo).var = var
        (settings.combatSystemInfo).gameRules = gameRules
        (settings.combatSystemInfo).ammunitionType = ammunitionType
        (settings.combatSystemInfo).uiIcons = uiIcons
        (settings.combatSystemInfo).shipLookup = shipLookup
        (settings.combatSystemInfo).events = events
        (settings.combatSystemInfo).uiElements = uiElements
        (settings.combatSystemInfo).canvas = canvas
        (settings.combatSystemInfo).uiElementsToPlace = uiElementsToPlace
        settings.combatUiReady = True
        settings.loadingCombat = False
        root.title((settings.combatSystemInfo).uiElements.rootTitle)
    else:
        ((settings.combatSystemInfo).var).finished = False
        ((settings.combatSystemInfo).uiElements).systemsLF = ttk.Labelframe(root,text= "" + " systems",borderwidth=2,style='Grey.TLabelframe.Label')
        root.title((settings.combatSystemInfo).uiElements.rootTitle)
        updateBattleUi((settings.combatSystemInfo).shipLookup,(settings.combatSystemInfo).uiMetrics,(settings.combatSystemInfo).var,root,(settings.combatSystemInfo).uiElements,(settings.combatSystemInfo).canvas,(settings.combatSystemInfo).uiElements.UIElementsList, multiplayerOptions)
    update((settings.combatSystemInfo).var,(settings.combatSystemInfo).uiElements,(settings.combatSystemInfo).uiMetrics,(settings.combatSystemInfo).uiIcons,(settings.combatSystemInfo).canvas,(settings.combatSystemInfo).events,(settings.combatSystemInfo).shipLookup,(settings.combatSystemInfo).gameRules,(settings.combatSystemInfo).ammunitionType,root,config,menuUiElements, multiplayerOptions)