import configparser
import sys
import tkinter as tk
import tkinter.ttk as ttk
from ctypes import pointer
from dis import dis
from ensurepip import bootstrap
from faulthandler import disable
from functools import partial
from pathlib import Path
from random import randint
from tabnanny import check
from tkinter import BOTH, Canvas, Frame, Tk
from tkinter.filedialog import askopenfilename

from src.ship import ship
from src.update import *
from src.turnManagers import *

def declareTargets(var):
    list1 = {}
    list2 = {}
    i = 2
    for ship in var.ships:
        if(not ship.owner == 'player1'):
            if(not ship.name in list1):
                list1.update({ship.name : ship.id})
            else:
                while((ship.name + ' (' + str(i) + ')') in list1):
                    i+=1
                ship.name = (ship.name + '(' + str(i) + ')')
                list1.update({ship.name : ship.id})
    i = 2
    for ship in var.ships:
        if(ship.owner == 'player1'):
            if(not ship.name in list2):
                list2.update({ship.name : ship.id})
            else:
                while((ship.name + ' (' + str(i) + ')') in list2):
                    i+=1
                ship.name = (ship.name + ' (' + str(i) + ')')
                list2.update({ship.name : ship.id})

    return list1,list2

def bindInputs(root,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,config,menuUiElements):
    root.bind('<Motion>', lambda e: motion(e, var,root))
    root.bind('<Button-1>', lambda e: mouseButton1(e, var))
    root.bind('<space>', lambda e: startTurn(uiElements,var,var.ships,gameRules,uiMetrics))
    root.bind('p', lambda e: pauseGame(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))
    root.bind('<Button-2>', lambda e: mouseButton3(e, var))
    root.bind('<ButtonRelease-2>', lambda e: mouseButton3up(e, var))
    root.bind('<MouseWheel>', lambda e: mouseWheel(e, var,uiMetrics))
    root.bind('<Configure>', lambda e: dragging(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements))

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
                system.setTargetStr(0)
                    #shipLookup[var.enemies[list(var.enemies.keys())[0]]].systemSlots[0])


def declareShipsTargets(var):
    for ship in var.ships:
        if(ship.owner == 'player1'):
            ship.setTargetStr(list(var.enemies.keys())[0])
            continue
        if(ship.owner == 'ai1'):
            ship.setTargetStr(list(var.players.keys())[0])


def declareShips(var,config,events,shipLookup,uiElements,uiMetrics,root,canvas):

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
                creationList[i].ap = int((config.get(configList[i], "ap")))
                creationList[i].stance = ((config.get(configList[i], "stance")))
                creationList[i].killed = False
            i+=1
        checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas)
        
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

                var.landmarks.append(naglowek.landmark( xPos = float(config.get(configList[i], "xPos")),
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
def run(config,root,menuUiElements):
    if(naglowek.combatUiReady):
        cinfo = naglowek.combatSystemInfo
        naglowek.combatUiReady = False
        for element in ((naglowek.combatSystemInfo).canvas).imageList :
            del element
        del (naglowek.combatSystemInfo).canvas                # theoretically not necessary but avoids accidental memory leaks
        del (naglowek.combatSystemInfo).uiMetrics             # or carrying over data from previous games
        for element in ((naglowek.combatSystemInfo).uiElements).staticUi:
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
        del (cinfo.var).img
        del (cinfo.var).radio
        (cinfo.uiElements).uiSystems = []
        (cinfo.uiElements).uiSystemsProgressbars = []
        del (cinfo.var)
        del (cinfo.gameRules)
        del (cinfo.ammunitionType)
        del (cinfo.uiIcons)
        del (cinfo.shipLookup)
        del (cinfo.events)
        del (cinfo.uiElements)
        del (cinfo.uiElementsToPlace)

    resume(config,root,menuUiElements)
# main
def resume(config,root,menuUiElements):
    if(not naglowek.combatUiReady):
        cwd = Path(sys.argv[0])
        cwd = str(cwd.parent)
        """
        rootX = root.winfo_screenwidth()
        rootY = root.winfo_screenheight()
        root.attributes('-fullscreen', True)
        """
        #root.deiconify()
        uiMetrics = naglowek.uiMetrics
        var = naglowek.global_var(config,root)
        gameRules = naglowek.game_rules()
        ammunitionType = ammunition_type()
        uiIcons = naglowek.ui_icons()
        shipLookup = dict
        events = naglowek._events()
        uiElements = naglowek.dynamic_object()
        uiElements.systemsLF = ttk.Labelframe(root,style = 'Grey.TLabelframe', text= "" + " systems",borderwidth=2, width=uiMetrics.canvasWidth*4/5)
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
        canvas = Canvas(root, width=uiMetrics.canvasWidth, height=uiMetrics.canvasHeight)
        canvas.ovalList = []
        canvas.availableOvalList = []
        tmp = uiIcons.armorIcon 
        canvas.imageID = canvas.create_image(0,0,image = tmp)
        getZoomMetrics(var,uiMetrics)
        (uiElements.staticUi).append(canvas)
        declareShips(var,config,events,shipLookup,uiElements,uiMetrics,root,canvas)
        uiElements.rootTitle = (config.get("Root", "title"))
        fog = (config.get("Options", "fogOfWar"))
        if(fog == '0'):
            var.fogOfWar = False
        else:
            var.fogOfWar = True

        root.title(uiElements.rootTitle)

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
        var.winMessage = config.get("Meta", "winMessage")
        var.looseMessage = config.get("Meta", "looseMessage")
        
        if config.get("Meta", "winByEliminatingEnemy") == "0":
            var.winByEliminatingEnemy = False
        else:
            var.winByEliminatingEnemy = True


        if config.get("Meta", "looseByEliminatingEnemy") == "0":
            var.looseByEliminatingEnemy = False
        else:
            var.looseByEliminatingEnemy = True

        if config.get("Meta", "winByEliminatingPlayer") == "0":
            var.winByEliminatingPlayer = False
        else:
            var.winByEliminatingPlayer = True

        if config.get("Meta", "looseByEliminatingPlayer") == "0":
            var.looseByEliminatingPlayer = False
        else:
            var.looseByEliminatingPlayer = True

        if config.get("Meta", "winByDisablingEnemy") == "0":
            var.winByDisablingEnemy = False
        else:
            var.winByDisablingEnemy = True

        if config.get("Meta", "winByDisablingPlayer") == "0":
            var.winByDisablingPlayer = False
        else:
            var.winByDisablingPlayer = True

        if config.get("Meta", "looseByDisablingPlayer") == "0":
            var.looseByDisablingPlayer = False
        else:
            var.looseByDisablingPlayer = True

        if config.get("Meta", "looseByDisablingEnemy") == "0":
            var.looseByDisablingEnemy = False
        else:
            var.looseByDisablingEnemy = True

        if config.get("Meta", "winByEliminating0") == "0":
            var.winByEliminating0 = False
        else:
            var.winByEliminating0 = True
        if config.get("Meta", "winByEliminating1") == "0":
            var.winByEliminating1 = False
        else:
            var.winByEliminating1 = True
        if config.get("Meta", "winByEliminating2") == "0":
            var.winByEliminating2 = False
        else:
            var.winByEliminating2 = True
        if config.get("Meta", "winByEliminating3") == "0":
            var.winByEliminating3 = False
        else:
            var.winByEliminating3 = True
        if config.get("Meta", "winByEliminating4") == "0":
            var.winByEliminating4 = False
        else:
            var.winByEliminating4 = True
        if config.get("Meta", "winByEliminating5") == "0":
            var.winByEliminating5 = False
        else:
            var.winByEliminating5 = True
            
        if config.get("Meta", "looseByEliminating0") == "0":
            var.looseByEliminating0 = False
        else:
            var.looseByEliminating0 = True
        if config.get("Meta", "looseByEliminating1") == "0":
            var.looseByEliminating1 = False
        else:
            var.looseByEliminating1 = True
        if config.get("Meta", "looseByEliminating2") == "0":
            var.looseByEliminating2 = False
        else:
            var.looseByEliminating2 = True
        if config.get("Meta", "looseByEliminating3") == "0":
            var.looseByEliminating3 = False
        else:
            var.looseByEliminating3 = True
        if config.get("Meta", "looseByEliminating4") == "0":
            var.looseByEliminating4 = False
        else:
            var.looseByEliminating4 = True
        if config.get("Meta", "looseByEliminating5") == "0":
            var.looseByEliminating5 = False
        else:
            var.looseByEliminating5 = True

        if config.get("Meta", "looseByDisabling0") == "0":
            var.looseByDisabling0 = False
        else:
            var.looseByDisabling0 = True
        if config.get("Meta", "looseByDisabling1") == "0":
            var.looseByDisabling1 = False
        else:
            var.looseByDisabling1 = True
        if config.get("Meta", "looseByDisabling2") == "0":
            var.looseByDisabling2 = False
        else:
            var.looseByDisabling2 = True
        if config.get("Meta", "looseByDisabling3") == "0":
            var.looseByDisabling3 = False
        else:
            var.looseByDisabling3 = True
        if config.get("Meta", "looseByDisabling4") == "0":
            var.looseByDisabling4 = False
        else:
            var.looseByDisabling4 = True
        if config.get("Meta", "looseByDisabling5") == "0":
            var.looseByDisabling5 = False
        else:
            var.looseByDisabling5 = True

        if config.get("Meta", "winByDisabling0") == "0":
            var.winByDisabling0 = False
        else:
            var.looseByDisabling0 = True
        if config.get("Meta", "winByDisabling1") == "0":
            var.winByDisabling1 = False
        else:
            var.winByDisabling1 = True
        if config.get("Meta", "winByDisabling2") == "0":
            var.winByDisabling2 = False
        else:
            var.winByDisabling2 = True
        if config.get("Meta", "winByDisabling3") == "0":
            var.winByDisabling3 = False
        else:
            var.winByDisabling3 = True
        if config.get("Meta", "winByDisabling4") == "0":
            var.winByDisabling4 = False
        else:
            var.winByDisabling4 = True
        if config.get("Meta", "winByDisabling5") == "0":
            var.winByDisabling5 = False
        else:
            var.winByDisabling5 = True

        if config.has_option('Meta', 'winBySeeingLandmarks'):
            if config.get("Meta", "winBySeeingLandmarks") == "0":
                var.winBySeeingLandmarks = False
            else:
                var.winBySeeingLandmarks = True

        if config.has_option('Meta', 'winByDomination'):
            if config.get("Meta", "winByDomination") == "0":
                var.winByDomination = False
            else:
                var.winByDomination = True
        if config.has_option('Meta', 'looseByDomination'):
            if config.get("Meta", "looseByDomination") == "0":
                var.looseByDomination = False
            else:
                var.looseByDomination = True

        var.winMessage = config.get("Meta", "winMessage")
        
        (uiElements.gameSpeedScale).set(8)
        uiElements.timeElapsedLabel = ttk.Label(root, style = 'Grey.TLabel', text="Time elapsed")
        uiElements.timeElapsedProgressBar = ttk.Progressbar(root, maximum=var.turnLength, variable=1,  orient='horizontal',
                                                mode='determinate', length=uiMetrics.shipDataWidth)

        uiElements.startTurnButton = tk.Button(root, text="Start turn", command=lambda:[startTurn(uiElements,var,var.ships,gameRules,uiMetrics)], width = 20, height= 7)
        uiElements.exitButton = tk.Button(root, text="Exit", command=exit)
        uiElements.exitToMenuButton = tk.Button(root, text="Exit to menu", command=lambda:[placeMenuUi(root,menuUiElements,uiMetrics), hideBattleUi(uiElements.staticUi,uiElements), finishSetTrue(var),saveCurrentGame(var)], width = 20, height= 7)

        (uiElements.staticUi).append(uiElements.pausedL)
        (uiElements.staticUi).append(uiElements.gameSpeedScale)
        (uiElements.staticUi).append(uiElements.gameSpeedL)
        (uiElements.staticUi).append(uiElements.timeElapsedLabel)
        (uiElements.staticUi).append(uiElements.timeElapsedProgressBar)
        (uiElements.staticUi).append(uiElements.startTurnButton)
        (uiElements.staticUi).append(uiElements.exitButton)
        (uiElements.staticUi).append(uiElements.exitToMenuButton)

        for ship1 in var.ships:
            if(ship1.owner == "player1"):
                putTracer(ship1,var,gameRules,uiMetrics)

        uiElements.enemyLF = ttk.Labelframe(root, style = 'Grey.TLabelframe',text = shipLookup[3].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.enemyLF2 = ttk.Labelframe(root, style = 'Grey.TLabelframe',text = shipLookup[4].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.enemyLF3 = ttk.Labelframe(root, style = 'Grey.TLabelframe',text = shipLookup[5].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.playerLF = ttk.Labelframe(root, style = 'Grey.TLabelframe',text = shipLookup[0].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.playerLF2 = ttk.Labelframe(root, style = 'Grey.TLabelframe',text = shipLookup[1].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)
        uiElements.playerLF3 = ttk.Labelframe(root, style = 'Grey.TLabelframe',text = shipLookup[2].name, height = uiMetrics.canvasHeight/5*2, width = uiMetrics.systemsLFWidth)

        var.playerShields = []
        var.playerShields2 = []
        var.playerShields3 = []
        var.enemyShields = []
        var.enemyShields2 = []
        var.enemyShields3 = []

        targets = [var.playerShields,var.playerShields2,var.playerShields3,var.enemyShields,var.enemyShields2,var.enemyShields3]
        elements = [var.player,var.player2,var.player3,var.enemy,var.enemy2,var.enemy3]
        labelframes = [uiElements.playerLF, uiElements.playerLF2, uiElements.playerLF3, uiElements.enemyLF,uiElements.enemyLF2, uiElements.enemyLF3]
        for target,element,labelframe in zip(targets,elements,labelframes):
            x = (element).maxShields
            n = 0
            if(element.maxShields == 1):
                lenGap = 0
                lenPro = 5
            else:
                lenGap = (element.maxShields-1)
                lenPro = (element.maxShields)*4
            lenTotal = lenGap + lenPro
            while(n < x):
                target.append(ttk.Progressbar(labelframe, maximum=100, length = (((lenPro/lenTotal)/element.maxShields)*(uiMetrics.systemsLFWidth - 15)),variable=100))
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

        (uiElements.tmpShieldsLabel) = []
        (uiElements.tmpShieldsLabel).append(var.playerShields)
        (uiElements.tmpShieldsLabel).append(var.playerShields2)
        (uiElements.tmpShieldsLabel).append(var.playerShields3)
        (uiElements.tmpShieldsLabel).append(var.enemyShields)
        (uiElements.tmpShieldsLabel).append(var.enemyShields2)
        (uiElements.tmpShieldsLabel).append(var.enemyShields3)        # create list of elements to disable if round is in progress
        (uiElements.UIElementsList).append(uiElements.gameSpeedScale)
        (uiElements.UIElementsList).append(uiElements.startTurnButton)
        (uiElements.UIElementsList).append(uiElements.exitToMenuButton)

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

            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "System: "))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Readiness: "))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Integrity: "))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Heat: "))
            target.append(ttk.Label(targetLF, style='Grey.TLabel', text = "Energy: "))
            for element in shipLookup[shipID].systemSlots:
                system = shipLookup[shipID].systemSlots[i]
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = system.name))
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(round((system.cooldown/system.maxCooldown))*100)))
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(system.integrity)))
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(system.heat)))
                target.append(ttk.Label(targetLF, style='Grey.TLabel', text = str(system.energy)))
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
        radioCommand = partial(radioBox,shipLookup , uiElements,var,uiMetrics,root,canvas)
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

        radioBox(shipLookup,uiElements,var,uiMetrics,root,canvas)
        bindInputs(root,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,config,menuUiElements)
        
        # first update 

        checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas)
        detectionCheck(var,uiMetrics)
        endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root)
        newWindow(uiMetrics,var,canvas,root)
        updateLabels(uiElements,shipLookup,var,root)

        (naglowek.combatSystemInfo).canvas = canvas
        (naglowek.combatSystemInfo).uiMetrics = uiMetrics
        (naglowek.combatSystemInfo).var = var
        (naglowek.combatSystemInfo).gameRules = gameRules
        (naglowek.combatSystemInfo).ammunitionType = ammunitionType
        (naglowek.combatSystemInfo).uiIcons = uiIcons
        (naglowek.combatSystemInfo).shipLookup = shipLookup
        (naglowek.combatSystemInfo).events = events
        (naglowek.combatSystemInfo).uiElements = uiElements
        (naglowek.combatSystemInfo).canvas = canvas
        (naglowek.combatSystemInfo).uiElementsToPlace = uiElementsToPlace
        naglowek.combatUiReady = True
    else:
        ((naglowek.combatSystemInfo).var).finished = False
        ((naglowek.combatSystemInfo).uiElements).systemsLF = ttk.Labelframe(root,text= "" + " systems",borderwidth=2,style='Grey.TLabelframe.Label')
        updateBattleUi((naglowek.combatSystemInfo).shipLookup,(naglowek.combatSystemInfo).uiMetrics,(naglowek.combatSystemInfo).var,root,(naglowek.combatSystemInfo).uiElements,(naglowek.combatSystemInfo).canvas)
    update((naglowek.combatSystemInfo).var,(naglowek.combatSystemInfo).uiElements,(naglowek.combatSystemInfo).uiMetrics,(naglowek.combatSystemInfo).uiIcons,(naglowek.combatSystemInfo).canvas,(naglowek.combatSystemInfo).events,(naglowek.combatSystemInfo).shipLookup,(naglowek.combatSystemInfo).gameRules,(naglowek.combatSystemInfo).ammunitionType,root,config,menuUiElements)