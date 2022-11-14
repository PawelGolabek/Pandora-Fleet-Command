from ctypes import pointer
from dis import dis
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
import random

from shipCombat import *
from canvasCalls import *
import naglowek
from rootCommands import *
from systems import *
from ammunitionType import *

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


############################## AMUNITION #############################################



class ship():
    def __init__(self,globalVar, name="MSS Artemis", owner="ai2", target='MSS Artemis',
                 hp=200, maxHp=None, ap=200, maxAp=None, shields=3, xPos=300, yPos=300,energyLimit = 20,
                 ammunitionChoice=0, ammunitionNumberChoice=0, systemSlots = [],
                 detectionRange=200, xDir=0.0, yDir=1, turnRate=0.5, ghostPoints = [], speed=40, maxSpeed = 40,
                 outlineColor="red"):  # replace shot handler
        # Init info                                             ## to handle shots when more than one enemy in range
        self.name = name
        self.owner = owner
        self.target = target
        self.xPos = xPos
        self.yPos = yPos
        self.energyLimit = energyLimit
        self.tmpEnergyLimit = energyLimit
        self.energy = energyLimit
        self.ammunitionChoice = ammunitionChoice
        self.ammunitionNumberChoice = ammunitionNumberChoice

        self.systemSlots = []
        for tmp in systemSlots:
            if(not tmp == ''):
                targetClass =  system_lookup[tmp]
                tmpSystem = targetClass(globalVar)
                self.systemSlots.append(tmpSystem)

        self.detectionRange = detectionRange
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.ghostPoints = ghostPoints
        self.speed = speed
        self.maxSpeed = maxSpeed
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
        self.shields = shields
        self.shieldsState = []
        self.alreadyShot = FALSE
        tmp = 0
        while(tmp < shields):
            self.shieldsState.append(globalVar.shieldMaxState)
            tmp += 1
        # Mid-round info
        self.shotsTaken = 0
        self.shotsNotTaken = 0
        self.visible = FALSE
        self.moveOrderX = xPos+0.01
        self.moveOrderY = yPos+0.01

class tracer():
    def __init__(self, xPos=300, yPos=300, xDir=0.0, yDir=1.0, turnRate=0.5, speed=40): 
        self.xPos = xPos
        self.yPos = yPos
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.speed = speed
        self.moveOrderX = None
        self.moveOrderY = None

class playerController():
    a = 10

class aiController():
    def systemChoice(ship,ships):
        basicEnergy = 0
        for system in ship.systemSlots:
            system.energy = system.minEnergy
            basicEnergy += system.minEnergy
        systemPool = []
        energy = ship.energyLimit - basicEnergy
        systemChecked = 0
        for system in ship.systemSlots:         # create system pool
            systemMaxPoints = system.maxEnergy
            while(systemMaxPoints > 0):
                systemPool.append(systemChecked)
                systemMaxPoints -= 1
            systemChecked += 1
                                                # add modifiers to pool if neeeded
        while(energy > 0 and len(systemPool)):
            choiceRand = random.randrange(0,len(systemPool))
            choiceNumber = systemPool.pop(choiceRand)
            (ship.systemSlots[choiceNumber]).energy += 1
            energy-=1
                           

    def moveOrderChoice(ship,ships,var,gameRules,uiMetrics):
        checksLeft = 40
        bestOrderX = 100    #default if everything else fails
        bestOrderY = 100    #default if everything else fails
        bestOrderValue = float('-inf')
        while(checksLeft):
            currentOrderValue = random.randint(19000, 21000)
            currentOrderX = ship.xPos + random.randint(-100, 100)
            currentOrderY = ship.yPos + random.randint(-100, 100)
           # print( "check: " + str(checksLeft) + " " + str(currentOrderX))
            ship.ghostPoints = []
            currentTracer = tracer()
            currentTracer.xPos = ship.xPos
            currentTracer.yPos = ship.yPos
            currentTracer.xDir = ship.xDir
            currentTracer.yDir = ship.yDir
            currentTracer.turnRate = ship.turnRate
            currentTracer.speed = ship.speed
            currentTracer.moveOrderX = currentOrderX
            currentTracer.moveOrderY = currentOrderY
            currentTracer.ttl = var.turnLength
            if(not 5 < currentOrderX < uiMetrics.canvasWidth-5):
                currentOrderValue = float('-inf')  
                checksLeft -= 1
                continue
            if(not 5 < currentOrderY < uiMetrics.canvasHeight-5):
                currentOrderValue = float('-inf')  
                checksLeft -= 1
                continue
            colorWeight  = var.mask[int(currentTracer.xPos)][int(currentTracer.yPos)] # test
            if(colorWeight <= 200):
                checksLeft -= 1
                continue
            while(True):
                # check for terrain
                if(not 5 < currentTracer.xPos < uiMetrics.canvasWidth-5):
                    currentOrderValue = float('-inf')  
                    break
                if(not 5 < currentTracer.yPos < uiMetrics.canvasHeight-5):
                    currentOrderValue = float('-inf')  
                    break
                # to prefer staying off the edges
                distanceToEdgeX = min(currentTracer.xPos,uiMetrics.canvasWidth -currentTracer.xPos)
                distanceToEdgeY = min(currentTracer.yPos,uiMetrics.canvasHeight -currentTracer.yPos)
                currentOrderValue += distanceToEdgeX / 1000
                currentOrderValue += distanceToEdgeY / 1000
                colorWeight = var.mask[int(currentTracer.xPos)][int(currentTracer.yPos)]
                # vector normalisation
                scale = math.sqrt((currentTracer.moveOrderX-currentTracer.xPos)*(currentTracer.moveOrderX-currentTracer.xPos) +
                                    (currentTracer.moveOrderY-currentTracer.yPos)*(currentTracer.moveOrderY-currentTracer.yPos))
                if(scale == 0):
                    scale = 0.01
                # move order into normalised vector
                moveDirX = -(currentTracer.xPos-currentTracer.moveOrderX) / scale
                moveDirY = -(currentTracer.yPos-currentTracer.moveOrderY) / scale

                degree = currentTracer.turnRate
                rotateVector(degree, currentTracer, moveDirX, moveDirY)

                if(colorWeight < 600 and colorWeight > 400):
                    movementPenality = gameRules.movementPenalityMedium
                elif(colorWeight < 400 and colorWeight > 200):
                    movementPenality = gameRules.movementPenalityMedium
                    currentOrderValue -= 400
                elif(colorWeight <= 200):
                    movementPenality = gameRules.movementPenalityHard
                    currentOrderValue -= 4000
                else:
                    movementPenality = 0.000001  # change

                xVector = currentTracer.xDir*currentTracer.speed/360
                yVector = currentTracer.yDir*currentTracer.speed/360

                currentTracer.xPos += xVector - xVector * movementPenality
                currentTracer.yPos += yVector - yVector * movementPenality
                currentTracer.ttl -= 1
                if(not currentTracer.ttl):
                    break
            if(currentOrderValue > bestOrderValue):
                bestOrderX = currentOrderX
                bestOrderY = currentOrderY
                bestOrderValue = currentOrderValue
            del currentTracer
            checksLeft -= 1
            if(not checksLeft):
                break
        ship.moveOrderX = bestOrderX
        ship.moveOrderY = bestOrderY


    def ammunitionChoiceScale(ship):  # virtual choice for AI Controller
        return 1
    a = 10

################################################ STARTUP ######################################
def finishSetTrue(globalVar):
    globalVar.finished = True

def getZoomMetrics(var,uiMetrics):
    var.mouseX = uiMetrics.canvasWidth/2
    var.mouseY = uiMetrics.canvasHeight/2
    var.left = 0
    var.right = uiMetrics.canvasWidth
    var.top = 0
    var.bottom = uiMetrics.canvasHeight
    var.yellowX = 0
    var.yellowY = 0
    var.zoomChange = False





def manageSystemActivations(ships,var,gameRules,uiMetrics,shipLookup):
    for ship in ships:
        for system in ship.systemSlots:
            system.activate(ship,var,gameRules,uiMetrics)

def manageSystemTriggers(ships,var,shipLookup):
    for ship1 in ships:
        for system in ship1.systemSlots:
            system.trigger(var,ship1,ships,shipLookup)
                # trigger is activated during round and activation is between
                                    
def getOrders(ship,var,gameRules,uiMetrics,forced=False):
    tracered = False
    if(ship.owner == "player1"):
        if(var.mouseButton1 and mouseOnCanvas(var,uiMetrics) and var.shipChoice == ship.name):
            ship.moveOrderX = var.left + \
                ((var.pointerX-uiMetrics.canvasX)/var.zoom)
            ship.moveOrderY = var.top + \
                ((var.pointerY-uiMetrics.canvasY)/var.zoom)
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
                getBonus(ship, landmark.boost)
                landmark.cooldown = landmark.defaultCooldown


def getBonus(ship, boost):
    if(boost == 'health'):
        ship.hp += 50
    elif(boost == 'armor'):
        ship.ap += 50
        # add boosts


def killShips(ships,missles,events):
    for ship1 in ships:
        if(ship1.hp < 1):
            ships.remove(ship1)
            for missle in missles:
                if missle.target == ship1:
                    missles.remove(missle)
            noEnemies = TRUE

            for progressBar in ship1.shieldsLabel:
                progressBar['value'] = 0

            for ship in ships:
                if(not ship.owner == "player1"):
                    noEnemies = FALSE
            if noEnemies and not events.showedWin:
                window = tk.Toplevel()
                label = tk.Label(window, text='yes, you win')
                label.place(x=0, y=0)
                events.showedWin = True
            elif(ship1.owner == 'player1' and events.playerDestroyed == False):
                events.playerDestroyed = True
                window = tk.Toplevel()
                label = tk.Label(window, text='yes, you looose')
                label.place(x=0, y=0)


############################################## MISSLES ##############################################


def manageRockets(missles,shipLookup,var):    # manage mid-air munitions
    for missle in missles:
        if(missle.sort == 'laser'):
            putLaser(missle,var,shipLookup)
            dealDamage(shipLookup[missle.target], missle.damage,var)
            missles.remove(missle)
            continue
        scale = math.sqrt((shipLookup[missle.target].xPos-missle.xPos) *
                          (shipLookup[missle.target].xPos-missle.xPos) +
                          (shipLookup[missle.target].yPos-missle.yPos) *
                          (shipLookup[missle.target].yPos-missle.yPos))
        if scale == 0:
            scale = 0.01
        # move order into normalised vector
        moveDirX = - (missle.xPos-shipLookup[missle.target].xPos) / scale
        moveDirY = - \
            (missle.yPos-shipLookup[missle.target].yPos) / scale
        degree = missle.turnRate
        rotateVector(degree, missle, moveDirX, moveDirY)
        missle.xPos += missle.xDir*missle.speed/360
        missle.yPos += missle.yDir*missle.speed/360
        if((abs(missle.xPos - shipLookup[missle.target].xPos) *
            abs(missle.xPos - shipLookup[missle.target].xPos) +
            abs(missle.xPos - shipLookup[missle.target].xPos) *
            abs(missle.xPos - shipLookup[missle.target].xPos) +
            abs(missle.yPos - shipLookup[missle.target].yPos) *
                abs(missle.yPos - shipLookup[missle.target].yPos)) < 25):
            dealDamage(shipLookup[missle.target], missle.damage,var)
            missles.remove(missle)




def drawLasers(var,canvas):
    for laser in var.lasers:
        if laser.ttl>0:
            drawX = (laser.xPos - var.left) * \
                var.zoom
            drawY = (laser.yPos - var.top) * \
                var.zoom
            drawX2 = (laser.targetXPos - var.left) * \
                var.zoom
            drawY2 = (laser.targetYPos - var.top) * \
                var.zoom
            canvas.create_line(drawX,drawY,drawX2,drawY2, fill = laser.color)# "yellow")
        else:
            (var.lasers).remove(laser)

############################################ INPUTS #############################################

def motion(event,var,root):
    var.pointerX = root.winfo_pointerx() - root.winfo_rootx()
    var.pointerY = root.winfo_pointery() - root.winfo_rooty()


def mouseButton1(event, var):  # get left mouse button and set it in globalvar
    if event:
        var.mouseButton1 = True
    else:
        var.mouseButton1 = False


def mouseWheel(event, var,uiMetrics):
    if event.delta > 0:
        var.mouseWheelUp = True
        if(var.zoom < 7 and mouseOnCanvas(var,uiMetrics)):
            var.zoom += 1
            var.zoomChange = True
    else:
        if(var.zoom > 1 and mouseOnCanvas(var,uiMetrics)):
            var.zoom -= 1
            var.zoomChange = True
        var.mouseWheelDown = True

def mouseButton3(event, var):
    if event:
        var.mouseButton3 = True

def mouseButton3up(event, var):
    if event:
        var.mouseButton3 = False


def trackMouse(var):
    var.pointerDeltaX = var.pointerX - var.prevPointerX
    var.pointerDeltaY = var.pointerY - var.prevPointerY
    var.prevPointerX = var.pointerX
    var.prevPointerY = var.pointerY
    var.prevPointerX = var.pointerX
    var.prevPointerY = var.pointerY

##################################### IN-GAME EVENTS ################################################


def update(globalVar,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root):
    canvas.delete('all')
    updateScales(uiElements,globalVar,shipLookup)
    updateEnergy(globalVar,uiElements,shipLookup)
    globalVar.gameSpeed = (uiElements.gameSpeedScale).get()
    newWindow(uiMetrics,globalVar,canvas)
    if(not globalVar.turnInProgress):
        manageSystemActivations(globalVar.ships,globalVar,gameRules,uiMetrics,shipLookup)
        for ship in globalVar.ships:
            getOrders(ship,globalVar,gameRules,uiMetrics)
    ticksToEndFrame = 0
    if(globalVar.turnInProgress):
        root.title("TURN IN PROGRESS")
        while(ticksToEndFrame < globalVar.gameSpeed):
            detectionCheck(globalVar.ships)
            updateShips(globalVar,uiMetrics,gameRules,shipLookup,canvas)
            manageLandmarks(globalVar.landmarks,globalVar.ships)
           # manageShots(globalVar.ships,globalVar.turnLength,uiElements,globalVar)   # check ship shot
            manageRockets(globalVar.currentMissles,shipLookup,globalVar)   # manage mid-air munitions
            manageSystemTriggers(globalVar.ships,globalVar,shipLookup)
            updateCooldowns(globalVar.ships)
            for laser in globalVar.lasers:
                if globalVar.turnInProgress:
                    laser.ttl -= 1
            killShips(globalVar.ships,globalVar.currentMissles,events)
            ticksToEndFrame += 1
            uiElements.timeElapsedProgressBar['value'] += 1
            if(uiElements.timeElapsedProgressBar['value'] > globalVar.turnLength):
                endTurn(uiElements,globalVar,gameRules,uiMetrics)
                break
    else:
        root.title(uiElements.rootTitle)
    drawShips(canvas,globalVar)
    drawGhostPoints(canvas,globalVar)
    drawLandmarks(globalVar,canvas,uiIcons)
    drawLasers(globalVar,canvas)
    drawRockets(globalVar,ammunitionType,canvas)
    globalVar.mouseOnUI = False
    globalVar.mouseWheelUp = False
    globalVar.mouseWheelDown = False
    globalVar.mouseButton1 = False
    globalVar.mouseButton2 = False
    trackMouse(globalVar)
    globalVar.zoomChange = False
    if(globalVar.finished):
        print("exiting")
        return
    root.after(10, partial(update,globalVar,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))


def newWindow(uiMetrics,var,canvas):
    if(not var.mouseWheelUp and not var.mouseWheelDown and var.mouseButton3 and var.zoom != 1):
        if(mouseOnCanvas(var,uiMetrics)):
            im = PIL.Image.open('resized_image.png')
            var.im = ImageTk.PhotoImage(im)

            if(var.zoom == 1):
                var.mouseX = (
                    (var.pointerX + var.pointerDeltaX- uiMetrics.canvasX) + var.left)
                var.mouseY = (
                    (var.pointerY + var.pointerDeltaY - uiMetrics.canvasY) + var.top)
            else:
                var.mouseX = (
                    (var.pointerX + var.pointerDeltaX - uiMetrics.canvasX)/(var.zoom-1) + var.left)
                var.mouseY = (
                    (var.pointerY + var.pointerDeltaY - uiMetrics.canvasY) / (var.zoom-1) + var.top)

            var.yellowX = (
                uiMetrics.canvasWidth/var.zoom)/2
            var.yellowY = (
                uiMetrics.canvasHeight/var.zoom)/2

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

            tmp = im.crop((var.left, var.top,
                            var.right, var.bottom))
            im = tmp
            im = im.resize(
                (uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

            var.im = ImageTk.PhotoImage(im)
            canvas.create_image(0, 0, image=var.im, anchor='nw')
    else:
        if((var.mouseWheelUp or var.mouseWheelDown) and mouseOnCanvas(var,uiMetrics)):
            im = PIL.Image.open('resized_image.png')
            var.im = ImageTk.PhotoImage(im)

            if(var.mouseWheelUp and var.zoomChange):
                if(var.zoom == 1):
                    var.mouseX = (
                        (var.pointerX - uiMetrics.canvasX) + var.left)
                    var.mouseY = (
                        (var.pointerY - uiMetrics.canvasY) + var.top)
                else:
                    var.mouseX = (
                        (var.pointerX - uiMetrics.canvasX)/(var.zoom-1) + var.left)
                    var.mouseY = (
                        (var.pointerY - uiMetrics.canvasY) / (var.zoom-1) + var.top)

                var.yellowX = (
                    uiMetrics.canvasWidth/var.zoom)/2
                var.yellowY = (
                    uiMetrics.canvasHeight/var.zoom)/2

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

            elif(var.mouseWheelDown):
                var.mouseX = uiMetrics.canvasWidth/2
                var.mouseY = uiMetrics.canvasHeight/2
                var.zoom = 1
                var.left = 0
                var.top = 0
                var.right = uiMetrics.canvasWidth
                var.bottom = uiMetrics.canvasHeight

            if(var.zoom != 1):

                tmp = im.crop((var.left, var.top,
                               var.right, var.bottom))
                im = tmp
                im = im.resize(
                    (uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

                var.im = ImageTk.PhotoImage(im)

            canvas.create_image(0, 0, image=var.im, anchor='nw')

        else:
            canvas.create_image(0, 0, image=var.im, anchor='nw')


def startTurn(uiElements,var,ships,gameRules,uiMetrics):
    print("New Round")
    var.turnInProgress = TRUE
    uiElements.timeElapsedProgressBar['value'] = 0
    for ship1 in var.ships:
        ship1.shotsNotTaken = 0
        ship1.shotsTaken = 0
    for object in uiElements.UIElementsList:
        object.config(state=DISABLED, background="#D0D0D0")
    for object in uiElements.RadioElementsList:
        object.config(state=DISABLED)
    for object in var.uiSystems:
        object.config(state = DISABLED, background="#D0D0D0")


def endTurn(uiElements,var,gameRules,uiMetrics): 
    var.turnInProgress = FALSE
    for object in uiElements.UIElementsList:
        object.config(state=NORMAL, background="#F0F0F0")
    for object in uiElements.RadioElementsList:
        object.config(state=NORMAL)
    for object in var.uiSystems:
        object.config(state = NORMAL, background="#F0F0F0")
    for ship in var.ships:
        ship.ghostPoints = []
    for ship1 in var.ships:
        if(ship1.owner == "ai1"):
            aiController.moveOrderChoice(ship1,var.ships,var,gameRules,uiMetrics)
            aiController.systemChoice(ship1,var.ships)
        getOrders(ship1,var,gameRules,uiMetrics,True)


def updateScales(uiElements,var,shipLookup):
    uiElements.playerAPProgressBar['value'] = shipLookup[var.playerName].ap
    uiElements.playerAPProgressBar2['value'] = shipLookup[var.playerName2].ap
    uiElements.playerAPProgressBar3['value'] = shipLookup[var.playerName3].ap
    uiElements.enemyAPProgressBar['value'] = shipLookup[var.enemyName].ap
    uiElements.enemyAPProgressBar2['value'] = shipLookup[var.enemyName2].ap
    uiElements.enemyAPProgressBar3['value'] = shipLookup[var.enemyName3].ap
    uiElements.playerHPProgressBar['value'] = shipLookup[var.playerName].hp
    uiElements.playerHPProgressBar2['value'] = shipLookup[var.playerName2].hp
    uiElements.playerHPProgressBar3['value'] = shipLookup[var.playerName3].hp
    uiElements.enemyHPProgressBar['value'] = shipLookup[var.enemyName].hp
    uiElements.enemyHPProgressBar2['value'] = shipLookup[var.enemyName2].hp
    uiElements.enemyHPProgressBar3['value'] = shipLookup[var.enemyName3].hp

    for ship1 in var.ships:
        updateShields(ship1,var)

    var.tmpCounter += 1
    shipChosen = shipLookup[var.shipChoice]

    uiElements.timeElapsedProgressBar.config(maximum=var.turnLength)

    i = 0 
    for system in var.uiSystemsProgressbars:
        (shipChosen.systemSlots[i]).energy = (var.uiSystems[i]).get()
        system1 = shipChosen.systemSlots[i]
        system['value'] = (system1.maxCooldown-system1.cooldown)
        i+=1

def updateCooldowns(ships):
    for ship in ships:
        for system in ship.systemSlots:
            #change if needed
            energyTicks = system.energy
            while( system.cooldown > 0 and energyTicks):
                system.cooldown -= 0.1
                energyTicks -=1

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
        (var.uiEnergyLabel).config(foreground = "black")
        for radio in var.shipChoiceRadioButtons:
            radio.configure(state = NORMAL)
            if(not var.turnInProgress):
                (uiElements.startTurnButton).config(state = NORMAL)
    (var.uiEnergyLabel).config(text = "Energy remaining: " + str(shipChosen.energy))
    

def updateShields(ship1,var):
    for tmp, progressBar in enumerate(ship1.shieldsLabel):
        if(var.turnInProgress):
            tmpShieldRegen = var.shieldRegen
            while(ship1.shieldsState[tmp] < var.shieldMaxState and tmpShieldRegen > 0):
                ship1.shieldsState[tmp] += 1
                tmpShieldRegen -= 1
                if(ship1.shieldsState[tmp] == var.shieldMaxState):
                    ship1.shields += 1
        progressBar['value'] = ship1.shieldsState[tmp] * 100 \
            / var.shieldMaxState
########################################## MULTIPURPOSE #########################################


def radioBox(shipLookup,uiElements,var,uiMetrics,root):
    var.selection = int((var.radio).get())
    if(var.selection == 0):
        var.shipChoice = var.playerName
    if(var.selection == 1):
        var.shipChoice = var.playerName2
    if(var.selection == 2):
        var.shipChoice = var.playerName3
    shipChosen = shipLookup[var.shipChoice]
    updateUtilityChoice(shipLookup,uiMetrics,var,root)


def updateUtilityChoice(shipLookup,uiMetrics,var,root):
    shipChosen = shipLookup[var.shipChoice]
    for widget in (var.uiSystemsLabelFrame).winfo_children():
        widget.destroy()
    (var.uiSystemsLabelFrame).destroy()
    var.uiSystems = []
    var.uiSystemsProgressbars = []
    shipChosen = shipLookup[var.shipChoice]
    var.uiSystemsLabelFrame = tk.LabelFrame(root,width=uiMetrics.systemScalesLabelFrameWidth, \
                                                    height = (uiMetrics.systemScalesMarginTop*1.5 + (uiMetrics.systemScalesHeightOffset)*len(shipChosen.systemSlots)), text= shipChosen.name + " systems", \
                                                    borderwidth=2, relief="groove")
    (var.uiSystemsLabelFrame).place(x = uiMetrics.leftMargin, y = uiMetrics.canvasY)
    i=0
    var.uiEnergyLabel = ttk.Label(var.uiSystemsLabelFrame, width=20, text = "Energy remaining: " + str(shipChosen.energy), font = "16")
    var.uiEnergyLabel.place(x = 10, y = 20)
    for system in shipChosen.systemSlots:
        scale = tk.Scale(var.uiSystemsLabelFrame, orient=HORIZONTAL, length=uiMetrics.systemScalesWidth, \
                            label=system.name, from_ = system.minEnergy, to=system.maxEnergy, relief=RIDGE)
        scale.set(system.energy)
        if(var.turnInProgress):
            scale.config(state = 'disabled', background="#D0D0D0")
        (var.uiSystems).append(scale)
        progressBar = ttk.Progressbar(var.uiSystemsLabelFrame, maximum=system.maxCooldown, length=(uiMetrics.systemScalesWidth), variable=(system.maxCooldown-system.cooldown))
        (var.uiSystemsProgressbars).append(progressBar)
        scale.place(x=10,y=uiMetrics.systemScalesMarginTop+i*uiMetrics.systemScalesHeightOffset)
        progressBar.place(x=10,y=uiMetrics.systemScalesMarginTop+i*(uiMetrics.systemScalesHeightOffset)+uiMetrics.systemProgressbarsHeightOffset)
        i+=1
        
def mouseOnCanvas(var,uiMetrics):
    if(var.pointerX > uiMetrics.canvasX and var.pointerX <
       (uiMetrics.canvasX + uiMetrics.canvasWidth) and var.pointerY >
            uiMetrics.canvasY and var.pointerY < (uiMetrics.canvasY + uiMetrics.canvasHeight)):
        return True
    else:
        return False


######################################################### MAIN ####################################


# main
def run(config,root,menuUiElements):
    if(not naglowek.combatUiReady):
        print("loading ui")
        """
        rootX = root.winfo_screenwidth()
        rootY = root.winfo_screenheight()
        root.attributes('-fullscreen', True)
        """
        #root.deiconify()
        uiMetrics = ui_metrics()
        globalVar = global_var(config,root)
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

        player = ship(globalVar, owner="player1", \
                    name=globalVar.playerName, shields=int((config.get("Player", "shields"))), xPos=int((config.get("Player", "xPos"))), yPos=int((config.get("Player", "yPos"))),
                    systemSlots=((config.get("Player", "systemSlots1")),(config.get("Player", "systemSlots2")),(config.get("Player", "systemSlots3")),(config.get("Player", "systemSlots4")), \
                    (config.get("Player", "systemSlots5")),(config.get("Player", "systemSlots6")),(config.get("Player", "systemSlots7")),(config.get("Player", "systemSlots8"))),speed = int((config.get("Player", "speed"))), \
                    detectionRange=int(config.get("Player", "detectionRange")), turnRate = float(config.get("Player", "turnRate")),\
                    maxSpeed = int((config.get("Player", "maxSpeed"))),outlineColor = ((config.get("Player", "outlineColor"))))
        player2 = ship(globalVar, owner="player1", \
                    name=globalVar.playerName2, shields=int((config.get("Player2", "shields"))), xPos=int((config.get("Player2", "xPos"))), yPos=int((config.get("Player2", "yPos"))),
                    systemSlots=((config.get("Player2", "systemSlots1")),(config.get("Player2", "systemSlots2")),(config.get("Player2", "systemSlots3")),(config.get("Player2", "systemSlots4")), \
                    (config.get("Player2", "systemSlots5")),(config.get("Player2", "systemSlots6")),(config.get("Player2", "systemSlots7")),\
                    (config.get("Player2", "systemSlots8"))), speed = int((config.get("Player2", "speed"))),detectionRange=int(config.get("Player2", "detectionRange")), turnRate = float(config.get("Player2", "turnRate")),\
                    maxSpeed = int((config.get("Player2", "maxSpeed"))),outlineColor = ((config.get("Player2", "outlineColor"))))
        player3 = ship(globalVar, owner="player1", \
                    name=globalVar.playerName3, shields=int((config.get("Player3", "shields"))), xPos=int((config.get("Player3", "xPos"))), yPos=int((config.get("Player3", "yPos"))),
                    systemSlots=((config.get("Player3", "systemSlots1")),(config.get("Player3", "systemSlots2")),(config.get("Player3", "systemSlots3")),(config.get("Player3", "systemSlots4")), \
                    (config.get("Player3", "systemSlots5")),(config.get("Player3", "systemSlots6")),(config.get("Player3", "systemSlots7")),\
                    (config.get("Player3", "systemSlots8"))), speed = int((config.get("Player3", "speed"))), detectionRange=int(config.get("Player3", "detectionRange")), turnRate = float(config.get("Player3", "turnRate")), \
                    maxSpeed = int((config.get("Player3", "maxSpeed"))),outlineColor = ((config.get("Player3", "outlineColor"))))

        enemy = ship(globalVar, owner="ai1", \
                    name=globalVar.enemyName, shields=int((config.get("Enemy", "shields"))), xPos=int((config.get("Enemy", "xPos"))), yPos=int((config.get("Enemy", "yPos"))),
                    systemSlots=((config.get("Enemy", "systemSlots1")),(config.get("Enemy", "systemSlots2")),(config.get("Enemy", "systemSlots3")),(config.get("Enemy", "systemSlots4")), \
                    (config.get("Enemy", "systemSlots5")),(config.get("Enemy", "systemSlots6")),(config.get("Enemy", "systemSlots7")),\
                    (config.get("Enemy", "systemSlots8"))), detectionRange=int(config.get("Enemy", "detectionRange")), turnRate = float(config.get("Enemy", "turnRate")),\
                    speed = int((config.get("Enemy", "speed"))),maxSpeed = int((config.get("Enemy", "maxSpeed"))),outlineColor = ((config.get("Enemy", "outlineColor"))))
        enemy2 = ship(globalVar, owner="ai1", \
                    name=globalVar.enemyName2, shields=int((config.get("Enemy2", "shields"))), xPos=int((config.get("Enemy2", "xPos"))), yPos=int((config.get("Enemy2", "yPos"))),
                    systemSlots=((config.get("Enemy2", "systemSlots1")),(config.get("Enemy2", "systemSlots2")),(config.get("Enemy2", "systemSlots3")),(config.get("Enemy2", "systemSlots4")), \
                    (config.get("Enemy2", "systemSlots5")),(config.get("Enemy2", "systemSlots6")),(config.get("Enemy2", "systemSlots7")),\
                    (config.get("Enemy2", "systemSlots8"))), detectionRange=int(config.get("Enemy2", "detectionRange")), turnRate = float(config.get("Enemy2", "turnRate")),\
                    speed = int((config.get("Enemy2", "speed"))),maxSpeed = int((config.get("Enemy2", "maxSpeed"))),outlineColor = ((config.get("Enemy2", "outlineColor"))))
        enemy3 = ship(globalVar, owner="ai1", \
                    name=globalVar.enemyName3, shields=int((config.get("Enemy3", "shields"))), xPos=int((config.get("Enemy3", "xPos"))), yPos=int((config.get("Enemy3", "yPos"))),
                    systemSlots=((config.get("Enemy3", "systemSlots1")),(config.get("Enemy3", "systemSlots2")),(config.get("Enemy3", "systemSlots3")),(config.get("Enemy3", "systemSlots4")), \
                    (config.get("Enemy3", "systemSlots5")),(config.get("Enemy3", "systemSlots6")),(config.get("Enemy3", "systemSlots7")),\
                    (config.get("Enemy3", "systemSlots8"))), detectionRange=int(config.get("Enemy3", "detectionRange")), turnRate = float(config.get("Enemy3", "turnRate")),\
                    speed = int((config.get("Enemy3", "speed"))),maxSpeed = int((config.get("Enemy3", "maxSpeed"))),outlineColor = ((config.get("Enemy3", "outlineColor"))))

        uiElements.staticUi = []
        (uiElements.staticUi).append(canvas)
        uiIcons.armorIcon = PhotoImage(file="icons/armor.png")
        motionCommand = partial(motion,True,globalVar,root)
        root.bind('<Motion>', lambda e: motion(e, globalVar,root))
        root.bind('<Button-1>', lambda e: mouseButton1(e, globalVar))
        root.bind('<Button-2>', lambda e: mouseButton3(e, globalVar))
        root.bind('<ButtonRelease-2>', lambda e: mouseButton3up(e, globalVar))
        root.bind('<MouseWheel>', lambda e: mouseWheel(e, globalVar,uiMetrics))
        root.protocol("WM_DELETE_WINDOW", on_closing)

        uiElements.rootTitle = (config.get("Root", "title"))
        root.title(uiElements.rootTitle)
        getZoomMetrics(globalVar,uiMetrics)

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
        globalVar.enemyName3: enemy3
        }

        land1 = landmark(200, 200, 3200, 3200, 50, 'armor')
        (globalVar.landmarks).append(land1)

        # canvas
        img = PIL.Image.open((config.get("Images", "img")))
        img = img.resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight))

        globalVar.img = PhotoImage("resized_image.png")
        canvas.imageList = []
        # item with background to avoid python bug people were mentioning about disappearing non-anchored images

        globalVar.imageMask = PIL.Image.open((config.get("Images", "imageMask")))
        img = PIL.Image.open((config.get("Images", "img")))
        im = img.resize(
            (uiMetrics.canvasWidth, uiMetrics.canvasHeight))

        globalVar.imageMask = globalVar.imageMask.resize(
            (uiMetrics.canvasWidth, uiMetrics.canvasHeight))

        globalVar.mask = createMask(globalVar,uiMetrics)

        globalVar.im = ImageTk.PhotoImage(im)
        canvas.imageList.append(im)
        canvas.imageList.append(globalVar.img)

        uiElements.UIElementsList = []
        uiElements.RadioElementsList = []

        uiElements.gameSpeedScale = tk.Scale(
            root, orient=HORIZONTAL, length=100, label="Playback speed", from_=1, to=16, resolution=-20, variable=2, relief=RIDGE)
        img = tk.PhotoImage(file=r'resized_image.png')
        (uiElements.gameSpeedScale).set(3)
        uiElements.timeElapsedLabel = tk.Label(root, text="Time elapsed")
        uiElements.timeElapsedProgressBar = ttk.Progressbar(root, maximum=globalVar.turnLength, variable=1,  orient='horizontal',
                                                mode='determinate', length=uiMetrics.shipDataWidth)

        startTurnCommand = partial(startTurn, uiElements,globalVar,globalVar.ships,gameRules,uiMetrics)
        uiElements.startTurnButton = tk.Button(root, text="Start turn", command=startTurnCommand, width = 20, height= 7)
        uiElements.exitButton = tk.Button(root, text="Exit", command=exit)
        uiElements.exitToMenuButton = tk.Button(root, text="Exit to menu", command=lambda:[showMenuUi(menuUiElements), hideBattleUi(uiElements.staticUi,root), finishSetTrue(globalVar)], width = 20, height= 7)


        (uiElements.staticUi).append(uiElements.gameSpeedScale)
        (uiElements.staticUi).append(uiElements.timeElapsedLabel)
        (uiElements.staticUi).append(uiElements.timeElapsedProgressBar)
        (uiElements.staticUi).append(uiElements.startTurnButton)
        (uiElements.staticUi).append(uiElements.exitButton)
        (uiElements.staticUi).append(uiElements.exitToMenuButton)

        # ships choice
        globalVar.shipChoice = player.name
        radioCommand = partial(radioBox,shipLookup , uiElements,globalVar,uiMetrics,root)
        uiElements.shipChoiceRadioButton1 = ttk.Radiobutton(
            root, text='1. MMS Artemis', variable=globalVar.radio, value=0, command=radioCommand)
        uiElements.shipChoiceRadioButton2 = ttk.Radiobutton(
            root, text='2. MMS Scout', variable=globalVar.radio, value=1, command=radioCommand)
        uiElements.shipChoiceRadioButton3 = ttk.Radiobutton(
            root, text='3. MMS Catalyst', variable=globalVar.radio, value=2, command=radioCommand)

        (uiElements.staticUi).append(uiElements.shipChoiceRadioButton1)
        (uiElements.staticUi).append(uiElements.shipChoiceRadioButton2)
        (uiElements.staticUi).append(uiElements.shipChoiceRadioButton3)

        radioBox(shipLookup,uiElements,globalVar,uiMetrics,root)
        updateUtilityChoice(shipLookup,uiMetrics,globalVar,root)
        detectionCheck(globalVar.ships)
        for ship1 in globalVar.ships:
            if(ship1.owner == "player1"):
                putTracer(ship1,globalVar,gameRules,uiMetrics)

        globalVar.shipChoiceRadioButtons = []
        (globalVar.shipChoiceRadioButtons).append(uiElements.shipChoiceRadioButton1)
        (globalVar.shipChoiceRadioButtons).append(uiElements.shipChoiceRadioButton2)
        (globalVar.shipChoiceRadioButtons).append(uiElements.shipChoiceRadioButton3)

        # ship shields
        playerSPLabelFrame = tk.LabelFrame(root, text= globalVar.playerName + " Shields",
                                            borderwidth=2, relief="groove")
        playerSPLabelFrame2 = tk.LabelFrame(root, text= globalVar.playerName2 + " Shields",
                                            borderwidth=2, relief="groove")
        playerSPLabelFrame3 = tk.LabelFrame(root, text= globalVar.playerName3 + " Shields",
                                            borderwidth=2, relief="groove")
        enemySPLabelFrame = tk.LabelFrame(root, text=globalVar.enemyName + " Shields",
                                        borderwidth=2, relief="groove")
        enemySPLabelFrame2 = tk.LabelFrame(root, text=globalVar.enemyName2 + " Shields",
                                            borderwidth=2, relief="groove")
        enemySPLabelFrame3 = tk.LabelFrame(root, text= globalVar.enemyName3 + " Shields",
                                            borderwidth=2, relief="groove")
        
        (uiElements.staticUi).append(playerSPLabelFrame)
        (uiElements.staticUi).append(playerSPLabelFrame2)
        (uiElements.staticUi).append(playerSPLabelFrame3)
        (uiElements.staticUi).append(enemySPLabelFrame)
        (uiElements.staticUi).append(enemySPLabelFrame2)
        (uiElements.staticUi).append(enemySPLabelFrame3)

        playerShields = []
        playerShields2 = []
        playerShields3 = []
        enemyShields = []
        enemyShields2 = []
        enemyShields3 = []

        x = player.shields
        n = 0
        while(n < x):
            playerShields.append(ttk.Progressbar(
                playerSPLabelFrame, maximum=100, length=math.floor((uiMetrics.shipDataWidth-10)/x * 4/5), variable=100))
            n += 1
        x = player2.shields
        n = 0
        while(n < x):
            playerShields2.append(ttk.Progressbar(
                playerSPLabelFrame2, maximum=100, length=math.floor((uiMetrics.shipDataWidth-10)/x * 4/5), variable=100))
            n += 1
        x = player3.shields
        n = 0
        while(n < x):
            playerShields3.append(ttk.Progressbar(
                playerSPLabelFrame3, maximum=100, length=math.floor((uiMetrics.shipDataWidth-10)/x * 4/5), variable=100))
            n += 1

        x = enemy.shields
        n = 0
        while(n < x):
            enemyShields.append(ttk.Progressbar(
                enemySPLabelFrame, maximum=100, length=math.floor((uiMetrics.shipDataWidth-10)/x * 4/5), variable=100))
            n += 1
        x = enemy2.shields
        n = 0
        while(n < x):
            enemyShields2.append(ttk.Progressbar(
                enemySPLabelFrame2, maximum=100, length=math.floor((uiMetrics.shipDataWidth-10)/x * 4/5), variable=100))
            n += 1
        x = enemy3.shields
        n = 0
        while(n < x):
            enemyShields3.append(ttk.Progressbar(
                enemySPLabelFrame3, maximum=100, length=math.floor((uiMetrics.shipDataWidth-10)/x * 4/5), variable=100))
            n += 1

        # ship armor
        uiElements.playerAPLabelFrame = tk.LabelFrame(root, text=globalVar.playerName + " Armor Effectivness",
                                            borderwidth=2, relief="groove")
        uiElements.playerAPProgressBar = ttk.Progressbar(
            uiElements.playerAPLabelFrame, maximum=player.maxAp, length=(uiMetrics.shipDataWidth-10), variable=100)
        uiElements.playerAPLabelFrame2 = tk.LabelFrame(root, text=globalVar.playerName2 + " Armor Effectivness",
                                            borderwidth=2, relief="groove")
        uiElements.playerAPProgressBar2 = ttk.Progressbar(
            uiElements.playerAPLabelFrame2, maximum=player2.maxAp, length=(uiMetrics.shipDataWidth-10), variable=100)
        uiElements.playerAPLabelFrame3 = tk.LabelFrame(root, text=globalVar.playerName3 + " Armor Effectivness",
                                            borderwidth=2, relief="groove")
        uiElements.playerAPProgressBar3 = ttk.Progressbar(
            uiElements.playerAPLabelFrame3, maximum=player3.maxAp, length=(uiMetrics.shipDataWidth-10), variable=100)
        uiElements.enemyAPLabelFrame = tk.LabelFrame(root, text=globalVar.enemyName + " Armor Effectivness",
                                        borderwidth=2, relief="groove")
        uiElements.enemyAPProgressBar = ttk.Progressbar(
            uiElements.enemyAPLabelFrame, maximum=enemy.maxAp, length=(uiMetrics.shipDataWidth-10), variable=100)
        uiElements.enemyAPLabelFrame2 = tk.LabelFrame(root, text= globalVar.enemyName2 + " Armor Effectivness",
                                            borderwidth=2, relief="groove")
        uiElements.enemyAPProgressBar2 = ttk.Progressbar(
            uiElements.enemyAPLabelFrame2, maximum=enemy.maxAp, length=(uiMetrics.shipDataWidth-10), variable=100)

        uiElements.enemyAPLabelFrame3 = tk.LabelFrame(root, text=globalVar.enemyName3 + " Armor Effectivness",
                                            borderwidth=2, relief="groove")
        uiElements.enemyAPProgressBar3 = ttk.Progressbar(
            uiElements.enemyAPLabelFrame3, maximum=enemy.maxAp, length=(uiMetrics.shipDataWidth-10), variable=100)

            
        (uiElements.staticUi).append(uiElements.playerAPLabelFrame)
        (uiElements.staticUi).append(uiElements.playerAPLabelFrame2)
        (uiElements.staticUi).append(uiElements.playerAPLabelFrame3)
        (uiElements.staticUi).append(uiElements.enemyAPLabelFrame)
        (uiElements.staticUi).append(uiElements.enemyAPLabelFrame2)
        (uiElements.staticUi).append(uiElements.enemyAPLabelFrame3)

        # ship hp
        uiElements.playerHPLabelFrame = tk.LabelFrame(root, text= globalVar.playerName + " Hull Integrity",
                                            borderwidth=2, relief="groove")
        uiElements.playerHPProgressBar = ttk.Progressbar(
            uiElements.playerHPLabelFrame, maximum=player.maxHp, length=(uiMetrics.shipDataWidth-10), variable=100)
        uiElements.playerHPLabelFrame2 = tk.LabelFrame(root, text= globalVar.playerName2 + " Hull Integrity",
                                            borderwidth=2, relief="groove")
        uiElements.playerHPProgressBar2 = ttk.Progressbar(
            uiElements.playerHPLabelFrame2, maximum=player2.maxHp, length=(uiMetrics.shipDataWidth-10), variable=100)

        uiElements.playerHPLabelFrame3 = tk.LabelFrame(root, text=globalVar.playerName3 + " Hull Integrity",
                                            borderwidth=2, relief="groove")
        uiElements.playerHPProgressBar3 = ttk.Progressbar(
            uiElements.playerHPLabelFrame3, maximum=player3.maxHp, length=(uiMetrics.shipDataWidth-10), variable=100)

        uiElements.enemyHPLabelFrame = tk.LabelFrame(root, text=globalVar.enemyName + " Hull Integrity",
                                        borderwidth=2, relief="groove")
        uiElements.enemyHPProgressBar = ttk.Progressbar(
            uiElements.enemyHPLabelFrame, maximum=enemy.maxHp, length=(uiMetrics.shipDataWidth-10), variable=100)
        uiElements.enemyHPLabelFrame2 = tk.LabelFrame(root, text= globalVar.enemyName2 + " Hull Integrity",
                                            borderwidth=2, relief="groove")
        uiElements.enemyHPProgressBar2 = ttk.Progressbar(
            uiElements.enemyHPLabelFrame2, maximum=enemy2.maxHp, length=(uiMetrics.shipDataWidth-10), variable=100)
        uiElements.enemyHPLabelFrame3 = tk.LabelFrame(root, text= globalVar.enemyName3 +" Hull Integrity",
                                            borderwidth=2, relief="groove")
        uiElements.enemyHPProgressBar3 = ttk.Progressbar(
            uiElements.enemyHPLabelFrame3, maximum=enemy3.maxHp, length=(uiMetrics.shipDataWidth-10), variable=100)

        (uiElements.staticUi).append(uiElements.playerHPLabelFrame)
        (uiElements.staticUi).append(uiElements.playerHPLabelFrame2)
        (uiElements.staticUi).append(uiElements.playerHPLabelFrame3)
        (uiElements.staticUi).append(uiElements.enemyHPLabelFrame)
        (uiElements.staticUi).append(uiElements.enemyHPLabelFrame2)
        (uiElements.staticUi).append(uiElements.enemyHPLabelFrame3)

        ######################################################### PROGRESSBAR ASSIGNMENT ####################################

        player.shieldsLabel = playerShields
        player2.shieldsLabel = playerShields2
        player3.shieldsLabel = playerShields3
        enemy.shieldsLabel = enemyShields
        enemy2.shieldsLabel = enemyShields2
        enemy3.shieldsLabel = enemyShields3

        (uiElements.tmpShieldsLabel) = []
        (uiElements.tmpShieldsLabel).append(playerShields)
        (uiElements.tmpShieldsLabel).append(playerShields2)
        (uiElements.tmpShieldsLabel).append(playerShields3)
        (uiElements.tmpShieldsLabel).append(enemyShields)
        (uiElements.tmpShieldsLabel).append(enemyShields2)
        (uiElements.tmpShieldsLabel).append(enemyShields3)        # create list of elements to disable if round is in progress
        uiElements.UIElementsList.append(uiElements.gameSpeedScale)
        uiElements.UIElementsList.append(uiElements.startTurnButton)

        (uiElements.RadioElementsList).append(uiElements.shipChoiceRadioButton1)
        (uiElements.RadioElementsList).append(uiElements.shipChoiceRadioButton2)
        (uiElements.RadioElementsList).append(uiElements.shipChoiceRadioButton3)
        (uiElements.staticUi).append(globalVar.uiSystemsLabelFrame)

        uiElementsToPlace = uiElements
        uiElements.playerSPLabelFrame = playerSPLabelFrame
        uiElements.playerSPLabelFrame2 = playerSPLabelFrame2
        uiElements.playerSPLabelFrame3 = playerSPLabelFrame3
        uiElements.enemySPLabelFrame = enemySPLabelFrame
        uiElements.enemySPLabelFrame2 = enemySPLabelFrame2
        uiElements.enemySPLabelFrame3 = enemySPLabelFrame3

        placeBattleUi(uiElementsToPlace,uiMetrics,canvas,globalVar)

        (naglowek.combatSystemInfo).canvas = canvas
        (naglowek.combatSystemInfo).uiMetrics =uiMetrics
        (naglowek.combatSystemInfo).globalVar = globalVar
        (naglowek.combatSystemInfo).gameRules = gameRules
        (naglowek.combatSystemInfo).ammunitionType = ammunitionType
        (naglowek.combatSystemInfo).uiIcons = uiIcons
        (naglowek.combatSystemInfo).shipLookup = shipLookup
        (naglowek.combatSystemInfo).events = events
        (naglowek.combatSystemInfo).uiElements = uiElements
        (naglowek.combatSystemInfo).canvas = canvas
        (naglowek.combatSystemInfo).uiElementsToPlace = uiElementsToPlace
        naglowek.combatUiReady = True
        # clock
    else:
        ((naglowek.combatSystemInfo).globalVar).finished = False
        placeBattleUi((naglowek.combatSystemInfo).uiElementsToPlace,(naglowek.combatSystemInfo).uiMetrics,(naglowek.combatSystemInfo).canvas,(naglowek.combatSystemInfo).globalVar)
    update((naglowek.combatSystemInfo).globalVar,(naglowek.combatSystemInfo).uiElements,(naglowek.combatSystemInfo).uiMetrics,(naglowek.combatSystemInfo).uiIcons,(naglowek.combatSystemInfo).canvas,(naglowek.combatSystemInfo).events,(naglowek.combatSystemInfo).shipLookup,(naglowek.combatSystemInfo).gameRules,(naglowek.combatSystemInfo).ammunitionType,root)
    root.mainloop()
