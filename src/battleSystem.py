import configparser
import math
import os
import sys
import time
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
import PIL.Image
from PIL import Image, ImageTk

import src.naglowek as naglowek
from src.ammunitionType import *
from src.canvasCalls import *
from src.rootCommands import *
from src.shipCombat import *
from src.systems import *
from src.aiControllers import *
import src.endConditions as endConditions
import src.respawns as respawns

#   Artemis 2021
#   Project by Pawel Golabek
#
#   Used libraries (excluding build-in): Pillow, Pil


#s = ttk.Style()
#s.theme_use('xpnative')
##s.configure("red.Horizontal.TProgressbar", foreground='blue', background='red')

class ui_icons():
    x=10

class _events():
    playerDestroyed = False
    showedWin = False
    showedLoose = False
    disabledWin = False
    disabledLoose = False

############################## AMUNITION #############################################

class ship():
    def setTarget(self,variable):
        self.target = variable.get()
    def setTargetStr(self,variable):
        self.target = variable
    def setTargetOnly(self):
        if(self.targetOnly):
            self.targetOnly = False
        else:
            self.targetOnly = True

    def declareSystemSlots(self,systemSlots,systemStatus):
        for tmp in systemSlots:
            if(not tmp == 'none'):
                targetClass =  naglowek.systemLookup[tmp]
                tmpSystem = targetClass()
                self.systemSlots.append(tmpSystem)
        i = 0
        for tmp in systemStatus:
            if(i < len(self.systemSlots)):
                self.systemSlots[i].cooldown = int(tmp)
                i+=1

    def declareShieldState(self,shields,maxShields,var):
        self.shields = shields
        self.maxShields = maxShields
        self.shieldsState = []
        tmp = 0
        while(tmp < maxShields):
            self.shieldsState.append(var.shieldMaxState)
            tmp += 1

    def __init__(self,var, name="MSS Artemis", owner="ai2", target=0,
                 hp=0, maxHp=None, ap=0, maxAp=None, shields=0, maxShields = 0, xPos=300, yPos=300,energy = 0,
                 ammunitionChoice=0, ammunitionNumberChoice=0, systemSlots = [], systemStatus = [],
                 detectionRange=1, xDir=0, yDir=1, turnRate=0, ghostPoints = [], signatures = [], speed=0, maxSpeed = 0,
                 outlineColor="red",id = 9999,signatureCounter=0, stance='rush',color = "red"):
        # Init info                                             
        self.name = name
        self.owner = owner
        self.target = target
        self.xPos = xPos
        self.yPos = yPos

        self.energyLimit = energy
        self.tmpEnergyLimit = energy
        self.energy = energy
        self.ammunitionChoice = ammunitionChoice
        self.ammunitionNumberChoice = ammunitionNumberChoice
        self.signatureCounter = signatureCounter
        self.systemSlots = []
        self.declareSystemSlots(systemSlots,systemStatus)

        self.detectionRange = detectionRange
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.ghostPoints = ghostPoints
        self.signatures = signatures
        self.speed = round(float(speed))
        self.maxSpeed = round(float(maxSpeed))
        self.outlineColor = outlineColor
        self.hp = hp
        if(maxHp == None):
            self.maxHp = hp
        else:
            self.maxHp = maxHp
        self.ap = ap
        if(maxAp == None):
            self.maxAp = ap
        else:
            self.maxAp = maxAp
        self.declareShieldState(shields,maxShields,var)
        # Mid-round info
        self.visible = False
        self.moveOrderX = xPos+0.01
        self.moveOrderY = yPos+0.01
        self.id = id
        self.signatureCounter = 0
        self.killed = False
        self.color = color
        self.targetOnly = False
        self.CBVar = IntVar()
        self.CBVar.set(0)
        #for events
        self.disabled = False
        #ui
        self.uiHeatBuildup = 0
        #ai info
        if(owner=="ai1"):
            self.prefMinRange = 100
            self.prefAverageRange = 200
            self.prefMaxRange = 300
            self.stance = stance

################################################ STARTUP ######################################

def manageSystemActivations(ships,var,gameRules,uiMetrics,shipLookup):
    for ship in ships:
        for system in ship.systemSlots:
            system.activate(ship,var,gameRules,uiMetrics)

def manageSystemTriggers(ships,var,shipLookup,uiMetrics):
    for ship1 in ships:
        if(ship1.hp > 0):
            for system in ship1.systemSlots:
                system.trigger(var,ship1,ships,shipLookup,uiMetrics)
                    # trigger is activated during round and activation is between
    for ship1 in ships:
        for system in ship1.systemSlots:
            if(system.category == 'weapon'):
                system.shotThisTurn = False
                                    
def getOrders(ship,var,gameRules,uiMetrics,forced=False):
    tracered = False
    if(ship.owner == "player1"):
        if(var.mouseButton1 and mouseOnCanvas(var,uiMetrics) and var.selection == ship.id):
            ship.moveOrderX = var.left + \
                ((var.pointerX-uiMetrics.canvasX)/var.zoom)
            ship.moveOrderY = var.top + \
                ((var.pointerY-uiMetrics.canvasY)/var.zoom)
            print(ship.moveOrderX,ship.moveOrderY)
            tracered = True
            putTracer(ship,var,gameRules,uiMetrics)
    if(not tracered and ship.owner == "player1" and forced ):
            putTracer(ship,var,gameRules,uiMetrics)

def manageLandmarks(landmarks, ships):
    for landmark in landmarks:
        if(landmark.cooldown > 0):
            landmark.cooldown -= 1
        for ship in ships:
            dist = ((landmark.xPos - ship.xPos)*(landmark.xPos - ship.xPos) +
                    (landmark.yPos - ship.yPos)*(landmark.yPos - ship.yPos))
            if(dist < landmark.radius*landmark.radius and landmark.cooldown == 0):
                landmark.visible = True
                getBonus(ship, landmark.boost)
                landmark.cooldown = landmark.defaultCooldown


def getBonus(ship, boost):
    if(boost == 'health'):
        ship.hp += 50
    elif(boost == 'armor'):
        ship.ap += 50
        # add boosts


############################################## MISSLES ##############################################


def manageRockets(missles,shipLookup,var,events,uiElements,uiMetrics,root,canvas):    # manage mid-air munitions
    for missle in missles:
        if(missle.sort == 'laser'):
            putLaser(missle,var,shipLookup)
            dealDamage(shipLookup[missle.target], missle.damage,var,missle.targetSystem, missle.heat,uiElements,shipLookup,root,events)
            missles.remove(missle)
            checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas)
            continue
        
        # check for terrain
        if(missle.ttl % 30 == 0):
            colorWeight = var.mask[int(missle.xPos)][int(missle.yPos)]
            if(colorWeight <= 200):
                missles.remove(missle)
                continue

        targetShipX = shipLookup[missle.target].xPos
        targetShipY = shipLookup[missle.target].yPos

        if(missle.xPos == max(missle.xPos,targetShipX)):
            aroundDistance = uiMetrics.canvasWidth - missle.xPos + targetShipX
            straightDistance = missle.xPos - targetShipX
        else:
            aroundDistance = uiMetrics.canvasWidth + missle.xPos - targetShipX
            straightDistance = targetShipX - missle.xPos

        if (straightDistance < aroundDistance):
            minDistX = (targetShipX - missle.xPos)            
        else:
            minDistX = (missle.xPos - targetShipX)
        ##
        if(missle.yPos == max(missle.yPos,targetShipY)):
            aroundDistance = uiMetrics.canvasHeight - missle.yPos + targetShipY
            straightDistance = missle.yPos - targetShipY
        else:
            aroundDistance = uiMetrics.canvasHeight + missle.yPos - targetShipY
            straightDistance = targetShipY - missle.yPos

        if (straightDistance < aroundDistance):
            minDistY = targetShipY - missle.yPos          
        else:
            minDistY = missle.yPos - targetShipY  

        scale = math.sqrt((minDistX) * (minDistX) + minDistY * minDistY)
        if scale == 0:
            scale = 0.01
        minDistX /= scale
        minDistY /= scale
        degree = missle.turnRate
        rotateVector(degree, missle, minDistX, minDistY)
        missle.xPos += missle.xDir*missle.speed/360
        missle.yPos += missle.yDir*missle.speed/360
        if((abs(missle.xPos - targetShipX) *
            abs(missle.xPos - targetShipX) +
            abs(missle.yPos - targetShipY) *
            abs(missle.yPos - targetShipY)) < 25):
            dealDamage(shipLookup[missle.target], missle.damage,var,missle.targetSystem,missle.heat,uiElements,shipLookup,root,events)
            missles.remove(missle)
            continue
        if(0 > missle.xPos):
            missle.xPos += uiMetrics.canvasWidth
        if(missle.xPos > uiMetrics.canvasWidth):
            missle.xPos -= uiMetrics.canvasWidth
        if(0 > missle.yPos):
            missle.yPos += uiMetrics.canvasHeight
        if(missle.yPos > uiMetrics.canvasHeight):
            missle.yPos -= uiMetrics.canvasHeight
        missle.ttl -= 1

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


def drawLasers(var,canvas,uiMetrics):
    for laser in var.lasers:
        if laser.ttl>0:
            drawX = (laser.xPos - var.left) * var.zoom
            drawY = (laser.yPos - var.top) * var.zoom
            aroundFlagX = False
            aroundFlagY = False
            if(laser.xPos == max(laser.xPos,laser.targetXPos)):
                aroundDistance = uiMetrics.canvasWidth - laser.xPos + laser.targetXPos
                laserCloserToRight = True
                straightDistance = laser.xPos - laser.targetXPos
            else:
                aroundDistance = uiMetrics.canvasWidth + laser.xPos - laser.targetXPos
                laserCloserToRight = False
                straightDistance = laser.targetXPos - laser.xPos

            if (straightDistance < aroundDistance):
                x2 = laser.targetXPos
                x3 = laser.xPos
                x4 = laser.targetXPos
            else:
                aroundFlagX = True
                if(laserCloserToRight):
                    x2 = laser.targetXPos + uiMetrics.canvasWidth
                    x3 = laser.xPos - uiMetrics.canvasWidth
                    x4 = laser.targetXPos
                else: 
                    x2 = laser.targetXPos - uiMetrics.canvasWidth
                    x3 = laser.xPos + uiMetrics.canvasWidth
                    x4 = laser.targetXPos
            ##
            if(laser.yPos == max(laser.yPos,laser.targetYPos)):
                aroundDistance = uiMetrics.canvasHeight - laser.yPos + laser.targetYPos
                laserCloserToDown = True
                straightDistance = laser.yPos - laser.targetYPos
            else:
                aroundDistance = uiMetrics.canvasHeight + laser.yPos - laser.targetYPos
                laserCloserToDown = False
                straightDistance = laser.targetYPos - laser.yPos

            if (straightDistance < aroundDistance):
                y2 = laser.targetYPos 
                y3 = laser.yPos
                y4 = laser.targetYPos
            else:
                aroundFlagY = True
                if(laserCloserToDown):
                    y2 = laser.targetYPos + uiMetrics.canvasHeight
                    y3 = laser.yPos - uiMetrics.canvasHeight
                    y4 = laser.targetYPos
                else: 
                    y2 = laser.targetYPos - uiMetrics.canvasHeight
                    y3 = laser.yPos + uiMetrics.canvasHeight
                    y4 = laser.targetYPos

            drawX2 = (x2- var.left) * var.zoom
            drawX3 = (x3- var.left) * var.zoom
            drawX4 = (x4- var.left) * var.zoom

            drawY2 = (y2- var.top) * var.zoom
            drawY3 = (y3- var.top) * var.zoom
            drawY4 = (y4- var.top) * var.zoom

            line = canvas.create_line(drawX,drawY,drawX2,drawY2, fill = laser.color, #stipple="gray75"
                                      )
            canvas.elements.append(line)
            

            if(aroundFlagX or aroundFlagY):
                line = canvas.create_line(drawX3,drawY3,drawX4,drawY4, fill = laser.color, #stipple="gray75"
                                          )
                canvas.elements.append(line)
        else:
            (var.lasers).remove(laser)
            del laser


def update(var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root):
    #for ship in var.ships:
    #    print(str(ship.name) + " " + str(ship.killed))
    if(var.drag=='' and not var.paused):
        canvas.delete('all')
        if(var.frameTime % 10 == 0):
            updateLabels(uiElements,shipLookup,var)
        hidePausedText(var,uiElements)
        updateScales(uiElements,var,shipLookup)
        updateEnergy(var,uiElements,shipLookup)
        var.gameSpeed = float((uiElements.gameSpeedScale).get())
        if(not var.turnInProgress):
            manageSystemActivations(var.ships,var,gameRules,uiMetrics,shipLookup)
            for ship in var.ships:
                getOrders(ship,var,gameRules,uiMetrics)
        ticksToEndFrame = 0
        root.title(uiElements.rootTitle)
        if(var.turnInProgress):
            root.title("TURN IN PROGRESS")
            var.systemTime = time.time()
            while(ticksToEndFrame < var.gameSpeed):
                checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas)
                detectionCheck(var,uiMetrics)
                updateShips(var,uiMetrics,gameRules,shipLookup,events,uiElements,root,canvas)
                manageLandmarks(var.landmarks,var.ships)
                manageSystemTriggers(var.ships,var,shipLookup,uiMetrics)
                manageRockets(var.currentMissles,shipLookup,var,events,uiElements,uiMetrics,root,canvas) 
                updateShields(var.ships,var)
                updateCooldowns(var.ships,var,shipLookup,uiMetrics)
                updateHeat(var.ships)
                dealHeatDamage(var.ships)
                updateSignatures(var.ships)
                for laser in var.lasers:
                    if var.turnInProgress:
                        laser.ttl -= 1
                ticksToEndFrame += 1
                uiElements.timeElapsedProgressBar['value'] += 1
                if(uiElements.timeElapsedProgressBar['value'] > var.turnLength):
                    root.title("AI IS THINKING")
                    endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root)
                    break
        var.input = (var.mouseWheelUp or var.mouseWheelDown or (var.mouseButton3 and var.zoom != 1 and mouseOnCanvas(var,uiMetrics)) or var.mouseButton1 )
        newWindow(uiMetrics,var,canvas)
        drawGhostPoints(canvas,var)
        drawSignatures(canvas,var)
        drawLandmarks(var,canvas,uiIcons,uiMetrics)
        drawLasers(var,canvas,uiMetrics)
        drawRockets(var,ammunitionType,canvas)
        var.mouseOnUI = False
        var.mouseWheelUp = False
        var.mouseWheelDown = False
        var.mouseButton1 = False
        var.mouseButton2 = False
        var.zoomChange = False
        endConditions.killedShips(var,events)
        endConditions.disabledShips(var,events)
        endConditions.foundLandmarks(var,events)
        endConditions.showWin(var,events)
        endConditions.showLoose(var,events)
        drawShips(canvas,var,uiMetrics)
        trackMouse(var)
        var.frameTime+=1
        if(var.finished):
            return
        if(var.updateTimer>0):
            var.updateTimer -= 1
        if(var.turnInProgress or var.mouseButton3):
            root.after(10, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))
        else:
            root.after(100, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))
    else:
        showPausedText(var,uiElements,uiMetrics)

def newWindow(uiMetrics,var,canvas):
    canvas.delete(canvas.imageID)
    canPoiX = var.pointerX - uiMetrics.canvasX
    canPoiY = var.pointerY - uiMetrics.canvasY
    var.imgg = ImageTk.PhotoImage(var.resizedImage)
    if(not var.mouseWheelUp and not var.mouseWheelDown and var.mouseButton3 and var.zoom != 1 and mouseOnCanvas(var,uiMetrics)):
        if(var.zoom == 1):
            var.mouseX = ((canPoiX + var.pointerDeltaX) + var.left)
            var.mouseY = ((canPoiY + var.pointerDeltaY) + var.top)
        else:
            var.mouseX = ((canPoiX + var.pointerDeltaX) / (var.zoom-1) + var.left)
            var.mouseY = ((canPoiY + var.pointerDeltaY) / (var.zoom-1) + var.top)
        var.yellowX = (uiMetrics.canvasWidth/var.zoom)/2
        var.yellowY = (uiMetrics.canvasHeight/var.zoom)/2

        if(var.mouseX > uiMetrics.canvasWidth - var.yellowX):  # bumpers on sides
            var.mouseX = var.right - var.yellowX
        if(var.mouseX < var.yellowX):
            var.mouseX = var.left + var.yellowX
        if(var.mouseY > uiMetrics.canvasHeight - var.yellowY):
            var.mouseY = var.bottom - var.yellowY
        if(var.mouseY < var.yellowY):
            var.mouseY = var.top + var.yellowY

        var.left = var.mouseX - var.yellowX
        var.right = var.mouseX + var.yellowX
        var.top = var.mouseY - var.yellowY
        var.bottom = var.mouseY + var.yellowY
        var.mouseX = var.right - var.left
        var.mouseY = var.bottom - var.top

        var.resizedImage = (var.image).crop((var.left, var.top, var.right, var.bottom))
        var.resizedImage = (var.resizedImage).resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

        var.imgg = ImageTk.PhotoImage(var.resizedImage)
        canvas.imageID = canvas.create_image(0, 0, image=var.imgg, anchor='nw')


    if((var.mouseWheelUp or var.mouseWheelDown) and mouseOnCanvas(var,uiMetrics) and var.zoomChange):
        var.imgg = var.image
        if(var.mouseWheelUp and var.zoomChange):
            if(var.zoom == 1):
                var.mouseX = (canPoiX)
                var.mouseY = (canPoiY)
            else:
                var.mouseX = ((canPoiX) / (var.zoom) + var.left)
                var.mouseY = ((canPoiY) / (var.zoom) + var.top)

        elif(var.mouseWheelDown):
            var.zoom = 1
            var.left = 0
            var.top = 0
            var.right = uiMetrics.canvasWidth
            var.bottom = uiMetrics.canvasHeight
            var.resizedImage = var.image
            var.imgg = ImageTk.PhotoImage(var.resizedImage)
    
        var.yellowX = (uiMetrics.canvasWidth/var.zoom)/2
        var.yellowY = (uiMetrics.canvasHeight/var.zoom)/2

        if(var.mouseX > uiMetrics.canvasWidth - var.yellowX):  # bumpers on sides
            var.mouseX = var.right - var.yellowX
        if(var.mouseX < var.yellowX):
            var.mouseX = var.left + var.yellowX
        if(var.mouseY > uiMetrics.canvasHeight - var.yellowY):
            var.mouseY = var.bottom - var.yellowY
        if(var.mouseY < var.yellowY):
            var.mouseY = var.top + var.yellowY

        var.left = var.mouseX - var.yellowX
        var.right = var.mouseX + var.yellowX
        var.top = var.mouseY - var.yellowY
        var.bottom = var.mouseY + var.yellowY
        var.resizedImage = (var.image).crop((var.left, var.top, var.right, var.bottom))
        var.resizedImage = (var.resizedImage).resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

        var.imgg = ImageTk.PhotoImage(var.resizedImage)
        canvas.imageID = canvas.create_image(0, 0, image=var.imgg, anchor='nw')
    else:
        var.imgg = ImageTk.PhotoImage(var.resizedImage)
        canvas.imageID = canvas.create_image(0, 0, image=var.imgg, anchor='nw')


def startTurn(uiElements,var,ships,gameRules,uiMetrics):
    if(not var.turnInProgress):
        print("New Round")
        var.turnInProgress = True
        uiElements.timeElapsedProgressBar['value'] = 0
        for object in uiElements.UIElementsList:
            object.config(state=DISABLED, background="#D0D0D0")
        for object in uiElements.RadioElementsList:
            object.config(state=DISABLED)
        for object in uiElements.uiSystems:
            object.config(state = DISABLED, background="#D0D0D0")
        for object in var.uiSystemsAS:
            object.config(state = DISABLED, style = 'Disabled.TCheckbutton')


def endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root): 
    var.turnInProgress = False
    for object in uiElements.UIElementsList:
        object.config(state = NORMAL, bg="#4582ec",highlightcolor = "white",fg = "white",highlightbackground = "#bfbfbf")
    if(not var.radio0Hidden):
        uiElements.RadioElementsList[0].config(state = NORMAL)
    if(not var.radio1Hidden):
        uiElements.RadioElementsList[1].config(state = NORMAL)
    if(not var.radio2Hidden):
        uiElements.RadioElementsList[2].config(state = NORMAL)
    for object in uiElements.uiSystems:
        object.config(state = NORMAL, bg="#4582ec",highlightcolor = "white")
    for object in var.uiSystemsAS:
        object.config(state = NORMAL, style = 'Red.TCheckbutton')
    uiElements.gameSpeedScale.config(bg="#4582ec",highlightcolor = "white",fg = "white")
    for ship in var.ships:
        ship.ghostPoints = []
    for ship1 in var.ships:
        if(ship1.owner == "ai1"):
            aiController.moveOrderChoice(ship1,var.ships,var,gameRules,uiMetrics)

            aiController.systemChoice(ship1,var.ships)
        getOrders(ship1,var,gameRules,uiMetrics,True)
    var.updateTimer = 3
    newWindow(uiMetrics,var,canvas)
    detectionCheck(var,uiMetrics)
    drawShips(canvas,var,uiMetrics)
    drawGhostPoints(canvas,var)
    drawSignatures(canvas,var)
    drawLandmarks(var,canvas,uiIcons,uiMetrics)
    drawLasers(var,canvas,uiMetrics)
    drawRockets(var,ammunitionType,canvas)
    updateShields(var.ships,var)
    updateLabels(uiElements,shipLookup,var)

def updateScales(uiElements,var,shipLookup):
    var.tmpCounter += 1
    shipChosen = shipLookup[var.shipChoice]
    uiElements.timeElapsedProgressBar.config(maximum=var.turnLength)
    i = 0 
    for system in uiElements.uiSystemsProgressbars:
        if(i>=len(shipChosen.systemSlots)):
            break
        (shipChosen.systemSlots[i]).energy = (uiElements.uiSystems[i]).get()
        system1 = shipChosen.systemSlots[i]
        system['value'] = (system1.maxCooldown-system1.cooldown)
        cldwn = round((abs(system1.maxCooldown-system1.cooldown)/float(system1.maxCooldown))*100.0)
        if(cldwn == 100):
            system.config(bootstyle = 'success')
        elif(cldwn < 30):
            system.config(bootstyle = 'danger')
        elif(cldwn > 70):
            system.config(bootstyle = 'primary')
        else:
            system.config(bootstyle = 'warning')
        i+=1

def updateCooldowns(ships,var,shipLookup,uiMetrics):
    for ship in ships:
        for system in ship.systemSlots:
            #change if needed
            energyTicks = system.energy
            while(system.cooldown > 0 and energyTicks):
                cooldownReduction = 2
                if(system.heat < 70):
                    cooldownReduction -= 0.3
                elif(system.heat < 30):
                    cooldownReduction -= 0
                elif(system.heat > 200):
                    cooldownReduction -= 0.9
                else:
                    cooldownReduction -= 0.6
                
                if(system.integrity == system.maxIntegrity):
                    cooldownReduction -= 0
                elif(system.integrity == 0):
                    energyTicks -= 1
                    break
                elif(system.integrity < system.maxIntegrity * 0.3):
                    cooldownReduction -= 0.9
                elif(system.integrity > system.maxIntegrity * 0.7):
                    cooldownReduction -= 0.3
                else:
                    cooldownReduction -= 0.6
                if(cooldownReduction > 0):
                    system.cooldown -= cooldownReduction
                energyTicks -= 1
                if(system.cooldown < 0):
                    system.cooldown = 0
                    break
                system.trigger(var,ship,ships,shipLookup,uiMetrics)

def updateHeat(ships):
    for ship in ships:
        for system in ship.systemSlots:
            system.coolUnits += system.cooling
            system.coolTicks = floor(system.coolUnits/100)
            if(system.coolTicks):
                system.coolUnits -= system.coolTicks * 100
                while(system.heat > 0 and system.coolTicks):
                    system.coolTicks -= 1
                    if(system.heat < 70):
                        system.heat -= 0.5
                    if(system.heat < 30):
                        system.heat -= 0
                    elif(system.heat > 200):
                        system.heat -= 2
                    else:
                        system.heat -= 1
            system.heat = round(system.heat*100)/100
            if(system.heat < 0):
                system.heat = 0

def dealHeatDamage(ships):
    for ship in ships:
        for system in ship.systemSlots:
            if(system.heat < 70):
                heatDamage = 0.2
            if(system.heat < 30):
                heatDamage = 0
            elif(system.heat > 200):
                heatDamage = 5
            else:
                heatDamage = 1
            system.heatUnits += heatDamage
            system.heatDamageTicks = floor(system.heatUnits/100)
            if(system.heatDamageTicks):
                system.heatUnits -= system.heatDamageTicks*100
                while(system.integrity > 0 and system.heatDamageTicks):
                    system.integrity -= 1
                    system.heatDamageTicks -= 1

def updateEnergy(var,uiElements,shipLookup):
    shipChosen = shipLookup[var.shipChoice]
    tmpEnergy = shipChosen.tmpEnergyLimit
    for system in shipChosen.systemSlots:
        tmpEnergy -= system.energy
    shipChosen.energy = tmpEnergy
    if(tmpEnergy<0):
        (var.uiEnergyLabel).config(foreground = "red")
        for radio in var.shipChoiceRadioButtons:
            radio.configure(state=DISABLED)
            (uiElements.startTurnButton).config(state = DISABLED)
    else:
        (var.uiEnergyLabel).config(foreground = "white")
        for radio in var.shipChoiceRadioButtons:
            radio.configure(state = NORMAL)
        disable = var.radio0Hidden
        if(disable):
            uiElements.RadioElementsList[0].config(state = DISABLED)
        
        disable = var.radio1Hidden
        if(disable):
            uiElements.RadioElementsList[1].config(state = DISABLED)
    
        disable = var.radio2Hidden
        if(disable):
            uiElements.RadioElementsList[2].config(state = DISABLED)

        if(not var.turnInProgress):
            (uiElements.startTurnButton).config(state = NORMAL)
    (var.uiEnergyLabel).config(text = "Energy left: " + str(shipChosen.energy))
    

def updateShields(ship1,var):
    for ship1 in var.ships:
        for tmp, progressBar in enumerate(ship1.shieldsLabel):
            if(var.turnInProgress):
                tmpShieldRegen = var.shieldRegen
                while(ship1.shieldsState[tmp] < var.shieldMaxState and tmpShieldRegen > 0):
                    ship1.shieldsState[tmp] += 1
                    tmpShieldRegen -= 1
                    if(ship1.shieldsState[tmp] == var.shieldMaxState):
                        ship1.shields += 1
            if(ship1.shieldsState[tmp] > var.shieldMaxState-var.turnLength):
                progressBar.config(bootstyle = 'primary')
            else:
                progressBar.config(bootstyle = 'danger')

            progressBar['value'] = ship1.shieldsState[tmp] * 100 \
                / var.shieldMaxState
########################################## MULTIPURPOSE #########################################


def radioBox(shipLookup,uiElements,var,uiMetrics,root,canvas):
    var.selection = int((var.radio).get())
    if(var.selection == 0):
        var.shipChoice = shipLookup[0].id
    if(var.selection == 1):
        var.shipChoice = shipLookup[1].id
    if(var.selection == 2):
        var.shipChoice = shipLookup[2].id
    updateBattleUi(shipLookup,uiMetrics,var,root,uiElements,canvas)
    updateLabels(uiElements,shipLookup,var)


def mouseOnCanvas(var,uiMetrics):
    if(var.pointerX > uiMetrics.canvasX and var.pointerX <
       (uiMetrics.canvasX + uiMetrics.canvasWidth) and var.pointerY >
            uiMetrics.canvasY and var.pointerY < (uiMetrics.canvasY + uiMetrics.canvasHeight)):
        return True
    else:
        return False

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

                if(config.get(configList[i], "visible") == 0):
                    _visible = True
                else:
                    _visible = False

                var.landmarks.append(naglowek.landmark( xPos = float(config.get(configList[i], "xPos")),
                yPos = float(config.get(configList[i], "yPos")),
                cooldown = float(config.get(configList[i], "cooldown")),
                defaultCooldown = float(config.get(configList[i], "cooldown")),
                radius = float(config.get(configList[i], "radius")),
                boost = config.get(configList[i], "boost"),
                visible = _visible
                ))
            i+=1
        if config.has_option('Meta', 'deleteRandomLandmarks'):
            toDelete = int(config.get("Meta", "deleteRandomLandmarks"))
            while toDelete:
                id = random.randrange(len(var.landmarks))
              #  randomLandmark = var.landmarks[id]
                var.landmarks.pop(id)
                toDelete -= 1
        
############################################ INPUTS #############################################

def bindInputs(root,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType):
    root.bind('<Motion>', lambda e: motion(e, var,root))
    root.bind('<Button-1>', lambda e: mouseButton1(e, var))
    root.bind('<space>', lambda e: startTurn(uiElements,var,var.ships,gameRules,uiMetrics))
    root.bind('p', lambda e: pauseGame(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))
    root.bind('<Button-2>', lambda e: mouseButton3(e, var))
    root.bind('<ButtonRelease-2>', lambda e: mouseButton3up(e, var))
    root.bind('<MouseWheel>', lambda e: mouseWheel(e, var,uiMetrics))
    root.bind('<Configure>', lambda e: dragging(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))

def pauseGame(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root):
    if(var.paused):
        var.paused = False
        root.after(1, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))
    else:
        var.paused = True

def motion(event,var,root):
    var.pointerX = root.winfo_pointerx() - root.winfo_rootx()
    var.pointerY = root.winfo_pointery() - root.winfo_rooty()


def mouseButton1(event, var):  # get left mouse button and set it in var
    if event:
        var.mouseButton1 = True
        var.updateTimer = 2
    else:
        var.mouseButton1 = False


def mouseWheel(event, var,uiMetrics):
    if event.delta > 0:
        var.mouseWheelUp = True
        if(var.zoom < 4 and mouseOnCanvas(var,uiMetrics)):
            var.zoom += 0.2
            var.zoomChange = True
    else:
        if(var.zoom > 1 and mouseOnCanvas(var,uiMetrics)):
            var.zoom -= 0.2
            var.zoomChange = True
        var.mouseWheelDown = True

def mouseButton3(event, var):
    if event:
        var.mouseButton3 = True

def mouseButton3up(event, var):
    if event:
        var.mouseButton3 = False


def dragging(event,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root):
    if event.widget is root:
        if not var.drag == '':
            root.after_cancel(var.drag)
        var.drag = root.after(100, partial(stop_drag,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))


def stop_drag(var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root):
    var.drag = ''
    root.after(1, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))



def trackMouse(var):
    var.pointerDeltaX = var.pointerX - var.prevPointerX
    var.pointerDeltaY = var.pointerY - var.prevPointerY

    var.prevPointerX = var.pointerX
    var.prevPointerY = var.pointerY


######################################################### MAIN ####################################

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
        uiIcons = ui_icons()
        shipLookup = dict
        events = _events()
        uiElements = naglowek.dynamic_object()
        uiElements.systemsLF = ttk.Labelframe(root,style = 'Grey.TLabelframe', text= "" + " systems",borderwidth=2, width=uiMetrics.canvasWidth*4/5)
        uiElements.staticUi = []
        uiIcons.armorIcon = PhotoImage(file=os.path.join(cwd, "icons","armor.png"))
        uiIcons.spotterIcon = PhotoImage(file=os.path.join(cwd, "icons","spotter.png"))

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
        newWindow(uiMetrics,var,canvas)
        # item with background to avoid python bug people were mentioning about disappearing non-anchored images

        canvas.imageList.append(var.image)
        canvas.imageList.append(var.imageMask)
        canvas.imageList.append(var.resizedImage)

        var.mask = createMask(var,uiMetrics)
        var.PFMask = createPFMask(var,uiMetrics)

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
        bindInputs(root,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType)
        
        # first update 

        checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas)
        detectionCheck(var,uiMetrics)
        endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root)
        newWindow(uiMetrics,var,canvas)
        updateLabels(uiElements,shipLookup,var)

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
    update((naglowek.combatSystemInfo).var,(naglowek.combatSystemInfo).uiElements,(naglowek.combatSystemInfo).uiMetrics,(naglowek.combatSystemInfo).uiIcons,(naglowek.combatSystemInfo).canvas,(naglowek.combatSystemInfo).events,(naglowek.combatSystemInfo).shipLookup,(naglowek.combatSystemInfo).gameRules,(naglowek.combatSystemInfo).ammunitionType,root)