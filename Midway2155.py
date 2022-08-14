import os
from tabnanny import check
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, Frame, BOTH
from random import randint
import math
from typing import Collection
import PIL
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import inspect

#   Artemis 2021
#   Project by Pawel Golabek
#
#   Used libraries (excluding build-in): Pillow, Pil

root = tk.Tk()

UIScale = 1

rootX = 1600
rootY = 900
"""
rootX = root.winfo_screenwidth()
rootY = root.winfo_screenheight()
root.attributes('-fullscreen', True)
"""
root.geometry(str(rootX*UIScale) + "x" + str(rootY*UIScale))


class global_var():
    radio = IntVar(root, 999)
    radio2 = IntVar(root, 999)
    ammunitionOptionChoice = StringVar(root)
    tmpCounter = 0
    # tmp
    radio.set(0)
    ## INPUT HANDLING ##
    mouseOnUI = FALSE
    mouseWheelUp = FALSE
    mouseWheelDown = FALSE
    mouseButton1 = FALSE
    pointerX = 0.0
    pointerY = 0.0
    ## GAME OPTIONS ##
    fogOfWar = TRUE
    gameSpeed = 1
    turnBased = TRUE
    turnLength = 360
    zoom = 1
    shieldRegen = 20
    shieldMaxState = 1200
    # GAME DATA
    choices = StringVar()
    options = []
    shipChoice = ''
    landmarks = []
    ships = []
    turnInProgress = FALSE
    misslesShot = 0
    currentMissles = []
    img = PhotoImage('1/map.png')
    image = Image.open('1/map.png')
    imageMask = Image.open('1/mapMask.png')
    # ZOOM
    mouseX = 0
    mouseY = 0
    left = 0
    right = 0
    top = 0
    bottom = 0
    yellowX = 0
    yellowY = 0
    zoomChange = 0
    # ICONS
    armorIcon = PhotoImage(file="icons/armor.png")


class ui_metrics:   # change to % for responsible
    canvasX = 200
    canvasY = 100
    canvasWidth = 1000
    canvasHeight = 500
    shipImageFrameHeight = 60
    shipDataX = canvasX
    shipDataY = canvasY + 20
    shipDataWidth = 200
    shipDataHeight = 40


class game_rules:
    movementPenalityHard = 0.9
    movementPenalityMedium = 0.5


class _events:
    enemyDestroyed = False
    playerDestroyed = False


class landmark():
    def __init__(self, xPos=100, yPos=100, cooldown=200, defaultCooldown=200, radius=100, boost='none'):
        self.xPos = xPos
        self.yPos = yPos
        self.cooldown = cooldown
        self.defaultCooldown = defaultCooldown
        self.radius = radius
        self.boost = boost

############################## AMUNITION #############################################


class ammunition():
    def __init__(self, name='', typeName='', owner='', target='', xDir=0, yDir=0, turnRate=2, speed=100, shotsPerTurn=5, damage=10, damageFalloffStart=200, damageFalloffStop=400, defaultAccuracy=90, special=None):
        self.owner = owner
        self.target = target
        self.name = name
        self.typeName = typeName
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.speed = speed
        self.shotsPerTurn = shotsPerTurn
        self.damage = damage
        self.damageFalloffStart = damageFalloffStart
        self.damageFalloffStop = damageFalloffStop
        self.defaultAccuracy = defaultAccuracy
        self.special = special


class ammunition_type:
    type1adefault = ammunition()
    type1adefault.name = 'type1a'
    type1adefault.typeName = 'type1a'
    type1adefault.shotsPerTurn = 8
    type1adefault.damage = 2
    type1adefault.turnRate = 6

    type2adefault = ammunition()
    type2adefault.name = 'type2a'
    type2adefault.typeName = 'type2a'
    type2adefault.shotsPerTurn = 5
    type2adefault.damage = 2
    type2adefault.turnRate = 6

    type3adefault = ammunition()
    type3adefault.name = 'type3a'
    type3adefault.typeName = 'type3a'
    type3adefault.shotsPerTurn = 1
    type3adefault.damage = 2
    type3adefault.turnRate = 10


ammunition_lookup = dict
# ammunition_lookup = {'type1a': type1a,
#                    'type2a': type2a,
#                   'type3a': type3a,
#                  }


class ship():
    def __init__(self, name="USS Artemis", owner="ai2", target='MSS Artemis',
                 hp=200, ap=200, shields=3, xPos=300, yPos=300,
                 typesOfAmmunition=[], ammunitionChoice=0, ammunitionNumberChoice=0,
                 detectionRange=200, xDir=0.0, yDir=1.0, turnRate=0.5, speed=40,
                 outlineColor="red"):
        # Init info
        self.name = name
        self.owner = owner
        self.target = target
        self.xPos = xPos
        self.yPos = yPos
        self.typesOfAmmunition = typesOfAmmunition
        self.ammunitionChoice = ammunitionChoice
        self.ammunitionNumberChoice = ammunitionNumberChoice
        self.detectionRange = detectionRange
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.speed = speed
        self.outlineColor = outlineColor
        self.hp = hp
        self.ap = ap
        self.shields = shields
        self.shieldsState = []
        tmp = 0
        while(tmp < shields):
            self.shieldsState.append(globalVar.shieldMaxState)
            tmp += 1
        # Mid-round info
        self.shotsTaken = 0
        self.shotsNotTaken = 0
        self.visible = FALSE
        self.moveOrderX = None
        self.moveOrderY = None


class playerController():
    a = 10


class aiController():
    def ammunitionChoice(ship):
        ship.ammunitionChoice = 0

    def accuracyChoiceScale(ship):  # virtual choice for AI Controller
        return 3

    def ammunitionChoiceScale(ship):  # virtual choice for AI Controller
        return 1
    a = 10

################################################ STARTUP ######################################


def getZoomMetrics():
    globalVar.mouseX = uiMetrics.canvasWidth/2
    globalVar.mouseY = uiMetrics.canvasHeight/2
    globalVar.left = 0
    globalVar.right = uiMetrics.canvasWidth
    globalVar.top = 0
    globalVar.bottom = uiMetrics.canvasHeight
    globalVar.yellowX = 0
    globalVar.yellowY = 0
    globalVar.zoomChange = False

################################################ SHIP #########################################


def updateShips():  # rotate and move the chosen ship
    for ship in globalVar.ships:
        if(ship.moveOrderX):
            # check for terrain
            if(not 0 < ship.xPos < ui_metrics.canvasWidth-5):
                globalVar.ships.remove(ship)
            if(not 0 < ship.yPos < ui_metrics.canvasHeight-5):
                globalVar.ships.remove(ship)
            colors = globalVar.imageMask.getpixel((int(ship.xPos), int(ship.yPos)
                                                   ))

            colorWeight = (colors[0] + colors[1] + colors[2])

            # vector normalisation
            scale = math.sqrt((ship.moveOrderX-ship.xPos)*(ship.moveOrderX-ship.xPos) +
                              (ship.moveOrderY-ship.yPos)*(ship.moveOrderY-ship.yPos))

            # move order into normalised vector
            moveDirX = -(ship.xPos-ship.moveOrderX) / scale
            moveDirY = -(ship.yPos-ship.moveOrderY) / scale

            degree = ship.turnRate
            rotateVector(degree, ship, moveDirX, moveDirY)

            if(colorWeight > 400):
                movementPenality = gameRules.movementPenalityMedium
                """
                canvas.create_rectangle(
                    ship.xPos, ship.yPos, ship.xPos + 10, ship.yPos + 20, fill='orange')"""
            elif(colorWeight < 200):
                movementPenality = gameRules.movementPenalityHard
                dealDamage(ship.name, 1)
                """
                canvas.create_rectangle(
                    ship.xPos, ship.yPos, ship.xPos + 10, ship.yPos + 20, fill='red')"""
            else:
                movementPenality = 0.000001  # change

            xVector = ship.xDir*ship.speed/360
            yVector = ship.yDir*ship.speed/360

            ship.xPos += xVector - xVector * movementPenality
            ship.yPos += yVector - yVector * movementPenality


def drawShips():  # draw ship on the map with all of its accesories
    for ship in globalVar.ships:
        if(ship.visible or not globalVar.fogOfWar or ship.owner == "player1"):
            drawX = (ship.xPos - globalVar.left) * \
                globalVar.zoom   # get coords relative to window
            drawY = (ship.yPos - globalVar.top) * globalVar.zoom

            if(ship.moveOrderX):
                drawOrderX = (ship.moveOrderX - globalVar.left) * \
                    globalVar.zoom    # get order relative to window
                drawOrderY = (ship.moveOrderY - globalVar.top) * globalVar.zoom
                canvas.create_line(drawX, drawY, drawOrderX,
                                   drawOrderY,   fill='white', dash=(3, 2))

            if(ship.owner == "ai1"):
                canvas.create_oval(drawX-ship.detectionRange*globalVar.zoom, drawY - ship.detectionRange*globalVar.zoom,
                                   drawX + ship.detectionRange*globalVar.zoom, drawY+ship.detectionRange*globalVar.zoom, outline=ship.outlineColor)
                canvas.create_line(drawX-5*globalVar.zoom, drawY-5*globalVar.zoom, drawX +
                                   5*globalVar.zoom, drawY+5*globalVar.zoom, width=globalVar.zoom,  fill='red')
            else:
                canvas.create_oval(drawX-ship.detectionRange*globalVar.zoom,
                                   drawY - ship.detectionRange*globalVar.zoom, drawX +
                                   ship.detectionRange*globalVar.zoom,
                                   drawY+ship.detectionRange*globalVar.zoom, outline=ship.outlineColor)
                canvas.create_line(drawX-5*globalVar.zoom, drawY-5*globalVar.zoom,
                                   drawX + 5*globalVar.zoom, drawY+5*globalVar.zoom, width=globalVar.zoom,  fill='white')  # draw ship
            if(ship.owner == "player1" or (not globalVar.fogOfWar or enemy.visible)):
                canvas.create_line(drawX, drawY,   drawX+(ship.xDir*120*globalVar.zoom),
                                   drawY+(ship.yDir*120*globalVar.zoom), fill="black")


def drawLandmarks():
    for landmark in globalVar.landmarks:
        drawX = (landmark.xPos - globalVar.left) * \
            globalVar.zoom   # change ###
        drawY = (landmark.yPos - globalVar.top) * \
            globalVar.zoom    # change ###

        radius = landmark.radius * globalVar.zoom
        canvas.create_text(drawX, drawY+20,
                           text=landmark.cooldown)
        canvas.create_oval(drawX-radius, drawY-radius,
                           drawX+radius, drawY+radius)
        iconX = drawX
        iconY = drawY
        drawLandmarkIcon(iconX, iconY, landmark.boost)


def drawLandmarkIcon(iconX, iconY, boost):
    if(boost == 'armor'):
        canvas.create_image(iconX, iconY, image=globalVar.armorIcon)


def manageShots():
    # add amunition scale input
    for ship1 in globalVar.ships:
        for ship2 in globalVar.ships:
            if(ship1.owner == 'player1' and ship2.owner == 'ai1'):
                if(ammunitionChoiceScale.get() != 0):
                    shotInterval = globalVar.turnLength / \
                        ship1.typesOfAmmunition[ship1.ammunitionChoice].shotsPerTurn
                    maxShotsNotTaken = accuracyChoiceScale.get()
                    distance = math.sqrt(
                        abs(pow(ship1.xPos-ship2.xPos, 2)+pow(ship1.yPos-ship2.yPos, 2)))
                    if(timeElapsedProgressBar['value'] % shotInterval == 0 and ship2.visible == TRUE and distance < ship1.detectionRange):
                        if(ship1.shotsNotTaken < maxShotsNotTaken):
                            ship1.shotsNotTaken += 1
                        else:
                            if(ship1.shotsTaken < ammunitionChoiceScale.get()):
                                ship1.shotsTaken += 1
                                createRocket(ship1, ship2)
                                print(ship1.name + " fired " +
                                      str(ship1.typesOfAmmunition[ship1.ammunitionChoice].name))
            elif(ship1.owner == 'ai1' and not ship2.owner == 'ai1'):
                if(aiController.ammunitionChoiceScale != 0):
                    shotInterval = globalVar.turnLength / \
                        ship1.typesOfAmmunition[ship1.ammunitionChoice].shotsPerTurn
                    maxShotsNotTaken = aiController.accuracyChoiceScale(ship1)
                    distance = math.sqrt(
                        abs(pow(ship1.xPos-ship2.xPos, 2)+pow(ship1.yPos-ship2.yPos, 2)))
                    if(timeElapsedProgressBar['value'] % shotInterval == 0 and ship2.visible == TRUE and distance < ship1.detectionRange):
                        if(ship1.shotsNotTaken < maxShotsNotTaken):
                            ship1.shotsNotTaken += 1
                        else:
                            if(ship1.shotsTaken < aiController.ammunitionChoiceScale(ship)):
                                ship1.shotsTaken += 1
                                createRocket(ship1, ship2)
                                print(ship1.name + " fired " +
                                      str(ship1.typesOfAmmunition[ship1.ammunitionChoice].name))


def getOrders(ship):
    if(ship.owner == "player1"):
        if(globalVar.mouseButton1 and mouseOnCanvas() and globalVar.shipChoice == ship.name):
            ship.moveOrderX = globalVar.left + \
                ((globalVar.pointerX-ui_metrics.canvasX)/globalVar.zoom)
            ship.moveOrderY = globalVar.top + \
                ((globalVar.pointerY-ui_metrics.canvasY)/globalVar.zoom)
    elif(ship.owner == "ai1"):
        ship.moveOrderX = 400  # insert ai contrller decision
        ship.moveOrderY = 400


def detectionCheck():

    for ship in globalVar.ships:
        ship.visible = FALSE
        if(ship.owner == 'ai1'):
            for ship2 in globalVar.ships:
                if(ship2.owner == 'player1'):
                    distance = math.sqrt(
                        abs(pow(ship.xPos-ship2.xPos, 2)+pow(ship.yPos-ship2.yPos, 2)))
                    if(distance < ship2.detectionRange):
                        ship.visible = TRUE
                        break
        else:
            for ship2 in globalVar.ships:
                if(ship2.owner == 'ai1'):
                    distance = math.sqrt(
                        abs(pow(ship.xPos-ship2.xPos, 2)+pow(ship.yPos-ship2.yPos, 2)))
                    if(distance < ship2.detectionRange):
                        ship.visible = TRUE
                        break


def manageLandmarks():
    for landmark in globalVar.landmarks:
        if(landmark.cooldown > 0):
            landmark.cooldown -= 1
        for ship in globalVar.ships:
            dist = math.sqrt(math.pow(landmark.xPos - ship.xPos, 2) +
                             math.pow(landmark.yPos - ship.yPos, 2))
            if(dist < landmark.radius and landmark.cooldown == 0):
                getBonus(ship, landmark.boost)
                landmark.cooldown = landmark.defaultCooldown


def getBonus(ship, boost):
    if(boost == 'health'):
        ship.hp += 50
    elif(boost == 'armor'):
        ship.ap += 50
        # add boosts


def dealDamage(shipName, damage):
    ship = ship_lookup[shipName]
    while(damage > 0):
        if(ship.ap > 0):  # armor
            ship.ap -= 1
        else:
            ship.hp -= 1
        damage -= 1

    if(ship.hp < 1 and not events.enemyDestroyed):
        if(ship.owner == 'ai1'):
            events.enemyDestroyed = True
            window = tk.Toplevel()
            label = tk.Label(window, text='yes, you won')
            label.place(x=0, y=0)
        elif(ship.owner == 'player1' and events.playerDestroyed == False):
            events.playerDestroyed = True
            window = tk.Toplevel()
            label = tk.Label(window, text='yes, you looose')
            label.place(x=0, y=0)


############################################## MISSLES ##############################################


def manageRockets():    # manage mid-air munitions
    for missle in globalVar.currentMissles:

        scale = math.sqrt((ship_lookup[missle.target].xPos-missle.xPos) *
                          (ship_lookup[missle.target].xPos-missle.xPos) +
                          (ship_lookup[missle.target].yPos-missle.yPos) *
                          (ship_lookup[missle.target].yPos-missle.yPos))
        if scale == 0:
            scale = 0.01
        # move order into normalised vector
        moveDirX = - (missle.xPos-ship_lookup[missle.target].xPos) / scale
        moveDirY = - \
            (missle.yPos-ship_lookup[missle.target].yPos) / scale

        degree = missle.turnRate
        rotateVector(degree, missle, moveDirX, moveDirY)
        missle.xPos += missle.xDir*missle.speed/360
        missle.yPos += missle.yDir*missle.speed/360
        if((abs(missle.xPos - ship_lookup[missle.target].xPos) *
            abs(missle.xPos - ship_lookup[missle.target].xPos) +
            abs(missle.xPos - ship_lookup[missle.target].xPos) *
            abs(missle.xPos - ship_lookup[missle.target].xPos) +
            abs(missle.yPos - ship_lookup[missle.target].yPos) *
                abs(missle.yPos - ship_lookup[missle.target].yPos)) < 25):
            dealDamage(missle.target, missle.damage)
            globalVar.currentMissles.remove(missle)


def drawRockets():
    for missle in globalVar.currentMissles:
        drawX = (missle.xPos - globalVar.left) * \
            globalVar.zoom   # change ok??? ###
        drawY = (missle.yPos - globalVar.top) * \
            globalVar.zoom    # change ok ??? ###
        canvas.create_line(drawX-5, drawY-5,
                           drawX+5, drawY+5)


def createRocket(ship, target):
    globalVar.misslesShot += 1
    missleClass = ship.typesOfAmmunition[ship.ammunitionChoice]
    # ammunition_lookup[ship.ammunitionChoice]
    # standard for ammunition instead of evaling?
    missle = ammunition()
    globalVar.currentMissles.append(missle)
    missleName = 'missle' + str(globalVar.misslesShot)
    setattr(globalVar.currentMissles[-1], 'name', missleName)
    setattr(globalVar.currentMissles[-1], 'class', missleClass)
    setattr(globalVar.currentMissles[-1], 'xPos', ship.xPos)
    setattr(globalVar.currentMissles[-1], 'yPos', ship.yPos)
    setattr(globalVar.currentMissles[-1], 'xDir', ship.xDir)
    setattr(globalVar.currentMissles[-1], 'yDir', ship.yDir)
    setattr(globalVar.currentMissles[-1], 'owner', ship.owner)
    setattr(globalVar.currentMissles[-1], 'turnRate',
            missleClass.turnRate)
    setattr(globalVar.currentMissles[-1], 'target', target.name)


############################################ INPUTS #############################################

def motion(event):
    globalVar.pointerX = root.winfo_pointerx() - root.winfo_rootx()
    globalVar.pointerY = root.winfo_pointery() - root.winfo_rooty()


def mouseButton1(event):  # get left mouse button and set it in globalvar
    if event:
        globalVar.mouseButton1 = True
    else:
        globalVar.mouseButton1 = False


def mouseWheel(event):
    if event.delta > 0:
        globalVar.mouseWheelUp = True
        if(globalVar.zoom < 7 and mouseOnCanvas()):
            globalVar.zoom += 1
            globalVar.zoomChange = True
    else:
        if(globalVar.zoom > 1 and mouseOnCanvas()):
            globalVar.zoom -= 1
            globalVar.zoomChange = True
        globalVar.mouseWheelDown = True

##################################### IN-GAME EVENTS ################################################


def update():
    canvas.delete('all')
    updateScales()
    globalVar.gameSpeed = gameSpeedScale.get()
    newWindow()
    if(not globalVar.turnInProgress):
        for ship in globalVar.ships:
            getOrders(ship)
    ticksToEndFrame = 0
    if(not globalVar.turnBased or globalVar.turnInProgress):
        while(ticksToEndFrame < globalVar.gameSpeed):
            detectionCheck()
            updateShips()
            manageLandmarks()
            manageShots()   # check ship shot
            manageRockets()   # manage mid-air munitions
            ticksToEndFrame += 1
            timeElapsedProgressBar['value'] += 1
            if(timeElapsedProgressBar['value'] > globalVar.turnLength):
                endTurn()
                break
    drawShips()
    drawLandmarks()
    drawRockets()
    globalVar.mouseOnUI = False
    globalVar.mouseWheelUp = False
    globalVar.mouseWheelDown = False
    globalVar.mouseButton1 = False
    globalVar.zoomChange = False
    root.after(10, update)


def newWindow():
    if(not globalVar.mouseWheelUp and not globalVar.mouseWheelDown):
        canvas.create_image(0, 0, image=globalVar.im, anchor='nw')
    else:
        if((globalVar.mouseWheelUp or globalVar.mouseWheelDown) and mouseOnCanvas()):
            im = Image.open('resized_image.png')
            globalVar.im = ImageTk.PhotoImage(im)

            if(globalVar.mouseWheelUp and globalVar.zoomChange):
                if(globalVar.zoom == 1):
                    globalVar.mouseX = (
                        (globalVar.pointerX - ui_metrics.canvasX) + globalVar.left)
                    globalVar.mouseY = (
                        (globalVar.pointerY - ui_metrics.canvasY) + globalVar.top)
                else:
                    globalVar.mouseX = (
                        (globalVar.pointerX - ui_metrics.canvasX)/(globalVar.zoom-1) + globalVar.left)
                    globalVar.mouseY = (
                        (globalVar.pointerY - ui_metrics.canvasY) / (globalVar.zoom-1) + globalVar.top)

                globalVar.yellowX = (
                    uiMetrics.canvasWidth/globalVar.zoom)/2
                globalVar.yellowY = (
                    uiMetrics.canvasHeight/globalVar.zoom)/2

                if(globalVar.mouseX > uiMetrics.canvasWidth - globalVar.yellowX):  # bumpers on sides
                    globalVar.mouseX = globalVar.right - globalVar.yellowX
                if(globalVar.mouseX < globalVar.yellowX):
                    globalVar.mouseX = globalVar.left + globalVar.yellowX
                if(globalVar.mouseY > uiMetrics.canvasHeight - globalVar.yellowY):
                    globalVar.mouseY = globalVar.bottom - globalVar.yellowY
                if(globalVar.mouseY < globalVar.yellowY):
                    globalVar.mouseY = globalVar.top + globalVar.yellowY

                globalVar.left = globalVar.mouseX - globalVar.yellowX
                globalVar.right = globalVar.mouseX + globalVar.yellowX
                globalVar.top = globalVar.mouseY - globalVar.yellowY
                globalVar.bottom = globalVar.mouseY + globalVar.yellowY
                globalVar.mouseX = globalVar.right - globalVar.left
                globalVar.mouseY = globalVar.bottom - globalVar.top

            if(globalVar.mouseWheelDown):
                globalVar.mouseX = uiMetrics.canvasWidth/2
                globalVar.mouseY = uiMetrics.canvasHeight/2
                globalVar.zoom = 1
                globalVar.left = 0
                globalVar.top = 0
                globalVar.right = uiMetrics.canvasWidth
                globalVar.bottom = uiMetrics.canvasHeight

            if(globalVar.zoom != 1):

                tmp = im.crop((globalVar.left, globalVar.top,
                               globalVar.right, globalVar.bottom))
                im = tmp
                im = im.resize(
                    (uiMetrics.canvasWidth, uiMetrics.canvasHeight), Image.ANTIALIAS)

                globalVar.im = ImageTk.PhotoImage(im)

            canvas.create_image(0, 0, image=globalVar.im, anchor='nw')

        else:
            canvas.create_image(0, 0, image=globalVar.im, anchor='nw')
            canvas.create_rectangle(
                0, 0, globalVar.yellowX, globalVar.yellowY)


def startTurn():
    print("New Round")
    globalVar.turnInProgress = TRUE
    timeElapsedProgressBar['value'] = 0
    aiController.ammunitionChoice(enemy)
    player.shotsNotTaken = 0
    enemy.shotsNotTaken = 0
    player.shotsTaken = 0
    enemy.shotsTaken = 0
    for object in UIElementsList:
        object.config(state=DISABLED, background="#D0D0D0")
    for object in RadioElementsList:
        object.config(state=DISABLED)


def endTurn():
    globalVar.turnInProgress = FALSE
    for object in UIElementsList:
        object.config(state=NORMAL, background="#F0F0F0")
    for object in RadioElementsList:
        object.config(state=NORMAL)


def updateScales():
    playerAPProgressBar['value'] = player.hp
    playerHPProgressBar['value'] = player.hp

    enemyAPProgressBar['value'] = enemy.ap
    enemyHPProgressBar['value'] = enemy.hp
    tmp = 0
    for progressBar in playerShields:
        player.shieldsState[tmp] += globalVar.shieldRegen  # copy
        progressBar['value'] = player.shieldsState[tmp]
        tmp += 1
    for progressBar in playerShields2:
        progressBar['value'] = 100
    for progressBar in playerShields3:
        progressBar['value'] = 100
    for progressBar in enemyShields:
        progressBar['value'] = 100
    for progressBar in enemyShields2:
        progressBar['value'] = 100
    for progressBar in enemyShields3:
        progressBar['value'] = 100

    globalVar.tmpCounter += 1

    ammunitionNumber = ammunitionChoiceScale.get()
    shipChosen = ship_lookup[globalVar.shipChoice]
    shipChosen.ammunitionNumberChoice = ammunitionNumber

    if(ammunitionNumber == 0):
        accuracyChoiceScale.set(0)
        accuracyChoiceScale.config(state="disabled", bg='#D0D0D0')
    else:
        if(not globalVar.turnInProgress):
            accuracyChoiceScale.config(state=NORMAL, background="#F0F0F0")
    timeElapsedProgressBar.config(maximum=globalVar.turnLength)


########################################## MULTIPURPOSE #########################################


def radioBox():
    globalVar.selection = int((globalVar.radio).get())
    label.config(text=globalVar.selection)
    if(globalVar.selection == 0):
        globalVar.shipChoice = playerName
    if(globalVar.selection == 1):
        globalVar.shipChoice = playerName2
    if(globalVar.selection == 2):
        globalVar.shipChoice = playerName3
    updateAmmunitionChoiceOptions()
    shipChosen = ship_lookup[globalVar.shipChoice]
    ammunitionChoiceScale.config(
        to=(shipChosen.typesOfAmmunition[shipChosen.ammunitionChoice]).shotsPerTurn)
    ammunitionChoiceScale.set(shipChosen.ammunitionNumberChoice)


def radioBox2():
    globalVar.selection2 = (globalVar.radio2).get()
    label2.config(text=globalVar.selection2)
    shipChosen = ship_lookup[globalVar.shipChoice]
    shipChosen.ammunitionChoice = globalVar.selection2
    ammunitionChoiceScale.config(
        to=(shipChosen.typesOfAmmunition[shipChosen.ammunitionChoice]).shotsPerTurn)
    ammunitionChoiceScale.set(shipChosen.ammunitionNumberChoice)


def updateAmmunitionChoiceOptions():

    (globalVar.radio2).set(ship_lookup[globalVar.shipChoice].ammunitionChoice)
    ammunitionChoiceRadioButton1.config(
        text=ship_lookup[(globalVar.shipChoice)].typesOfAmmunition[0].typeName)
    ammunitionChoiceRadioButton2.config(
        text=ship_lookup[(globalVar.shipChoice)].typesOfAmmunition[1].typeName)
    ammunitionChoiceRadioButton3.config(
        text=ship_lookup[(globalVar.shipChoice)].typesOfAmmunition[2].typeName)


def mouseOnCanvas():
    if(globalVar.pointerX > ui_metrics.canvasX and globalVar.pointerX <
       (uiMetrics.canvasX + uiMetrics.canvasWidth) and globalVar.pointerY >
            ui_metrics.canvasY and globalVar.pointerY < (uiMetrics.canvasY + uiMetrics.canvasHeight)):
        return True
    else:
        return False


def rotateVector(degree, object, moveDirX, moveDirY):
    if((object.xDir > moveDirX and object.yDir > -moveDirY) or object.xDir < moveDirX and object.yDir < -moveDirY):
        degree = object.turnRate
        object.xDir = math.cos((degree/360)*math.pi)*object.xDir - \
            math.sin((degree/360)*math.pi)*object.yDir
        object.yDir = math.sin((degree/360)*math.pi)*object.xDir + \
            math.cos((degree/360)*math.pi)*object.yDir
    else:
        degree = -object.turnRate  # change direction
        object.xDir = math.cos((degree/360)*math.pi)*object.xDir -  \
            math.sin((degree/360)*math.pi)*object.yDir
        object.yDir = math.sin((degree/360)*math.pi)*object.xDir + \
            math.cos((degree/360)*math.pi)*object.yDir

    scale = math.sqrt(abs(object.xDir*object.xDir+object.yDir*object.yDir))

    # move direviton into normalised vector
    if(scale != 0):
        object.xDir = object.xDir / scale
        object.yDir = object.yDir / scale


######################################################### MAIN ####################################

# main
root.bind('<Motion>', motion)
root.bind('<Button-1>', mouseButton1)
root.bind('<MouseWheel>', mouseWheel)

root.title("MMS Artemis")
uiMetrics = ui_metrics()
globalVar = global_var()
gameRules = game_rules()
ammunitionType = ammunition_type()
ship_lookup = dict

getZoomMetrics()

# Ships

playerName = 'MMS Artemis'
playerName2 = 'MMS Scout'
playerName3 = 'MMS Catalyst'

enemyName = 'RDD HellWitch'
enemyName2 = 'RDD Redglower'
enemyName3 = 'RDD Firebath'

player = ship(outlineColor="white", owner="player1",
              name=playerName, shields=10, xPos=20, typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type3adefault, ammunitionType.type3adefault], detectionRange=100, ammunitionChoice=0)
player2 = ship(outlineColor="white", owner="player1",
               name=playerName2, shields=5, xPos=40, typesOfAmmunition=[ammunitionType.type2adefault, ammunitionType.type2adefault, ammunitionType.type2adefault], detectionRange=160, ammunitionChoice=1)
player3 = ship(outlineColor="white", owner="player1",
               name=playerName3, shields=3, xPos=900, typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type2adefault, ammunitionType.type3adefault], detectionRange=180, ammunitionChoice=1)

enemy = ship(xPos=300, yPos=100, outlineColor="red", shields=10, typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type2adefault, ammunitionType.type2adefault],
             owner="ai1", ammunitionChoice=0, name=enemyName)
enemy2 = ship(xPos=600, yPos=100, outlineColor="red", shields=5,
              owner="ai1", ammunitionChoice=0, name=enemyName2, typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type2adefault, ammunitionType.type2adefault])
enemy3 = ship(xPos=50, yPos=100, outlineColor="red", shields=3, typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type2adefault, ammunitionType.type3adefault],
              owner="ai1", ammunitionChoice=0, name=enemyName3)

(globalVar.ships).append(player)
(globalVar.ships).append(player2)
(globalVar.ships).append(player3)

(globalVar.ships).append(enemy)
(globalVar.ships).append(enemy2)
(globalVar.ships).append(enemy3)

events = _events()

ship_lookup = {
    playerName: player,
    enemyName: enemy,
    playerName2: player2,
    enemyName2: enemy2,
    playerName3: player3,
    enemyName3: enemy3}

land1 = landmark(200, 200, 200, 200, 50, 'armor')
(globalVar.landmarks).append(land1)

# canvas
img = Image.open('1/map.png')
img = img.resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight))
# img.save('resized_image.png')


canvas = Canvas(root, width=uiMetrics.canvasWidth,
                height=uiMetrics.canvasHeight)

globalVar.img = PhotoImage("resized_image.png")
canvas.imageList = []
# item with background to avoid python bug people were mentioning about disappearing non-anchored images

globalVar.imageMask = Image.open("1/mapMask.png")
img = Image.open('1/map.png')
im = img.resize(
    (uiMetrics.canvasWidth, uiMetrics.canvasHeight), Image.ANTIALIAS)

globalVar.imageMask = globalVar.imageMask.resize(
    (uiMetrics.canvasWidth, uiMetrics.canvasHeight), Image.ANTIALIAS)

globalVar.im = ImageTk.PhotoImage(im)
canvas.imageList.append(im)
canvas.imageList.append(globalVar.img)

UIElementsList = []
RadioElementsList = []

ammunitionChoiceScale = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Number of shots", to=len(player.typesOfAmmunition), relief=RIDGE)
accuracyChoiceScale = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Time to aim", to=4, relief=RIDGE)
gameSpeedScale = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Playback speed", from_=1, to=16, resolution=-20, variable=2, relief=RIDGE)
pixel = tk.PhotoImage(width=1, height=1)
img = tk.PhotoImage(file=r'resized_image.png')
gameSpeedScale.set(3)
timeElapsedLabel = tk.Label(root, text="Time elapsed")
timeElapsedProgressBar = ttk.Progressbar(root, maximum=globalVar.turnLength, variable=1,  orient='horizontal',
                                         mode='determinate', length=ui_metrics.shipDataWidth)

startTurnButton = tk.Button(root, text="Start turn", command=startTurn)
exitButton = tk.Button(root, text="Exit", command=exit)

globalVar.shipChoice = player.name


# ship choice
label = Label(root)
var = IntVar()
shipChoiceRadioButton1 = ttk.Radiobutton(
    root, text='1. MMS Artemis', variable=globalVar.radio, value=0, command=radioBox)
shipChoiceRadioButton2 = ttk.Radiobutton(
    root, text='2. MMS Scout', variable=globalVar.radio, value=1, command=radioBox)
shipChoiceRadioButton3 = ttk.Radiobutton(
    root, text='3. MMS Catalyst', variable=globalVar.radio, value=2, command=radioBox)

label2 = Label(root)
var = IntVar()
ammunitionChoiceRadioButton1 = ttk.Radiobutton(
    root, text='1. Type 1a', variable=globalVar.radio2, value=0, command=radioBox2)
ammunitionChoiceRadioButton2 = ttk.Radiobutton(
    root, text='2. Type 2a', variable=globalVar.radio2, value=1, command=radioBox2)
ammunitionChoiceRadioButton3 = ttk.Radiobutton(
    root, text='3. Type 3a', variable=globalVar.radio2, value=2, command=radioBox2)

radioBox()

shipImage1 = Image.open('ship_modules/ship.png')
shipImage = shipImage1.resize(
    (math.floor(uiMetrics.canvasWidth/8), math.floor(uiMetrics.canvasHeight/8)), Image.ANTIALIAS)
canvas.imageList.append(shipImage)
playerImage = ImageTk.PhotoImage(shipImage)
playerDisplay = tk.Label(root, image=playerImage)

enemyImage = ImageTk.PhotoImage(shipImage)
enemyDisplay = tk.Label(root, image=enemyImage)

distanceLabelFrame = ttk.LabelFrame(
    root, text='Distance between ships', width=1000, height=200)
distanceLabel = tk.Label(distanceLabelFrame, text='0000000')

# ship shields
playerSPLabelFrame = ttk.LabelFrame(root, text="Player Shields",
                                    borderwidth=2, relief="groove")
playerSPProgressBar = ttk.Progressbar(
    playerSPLabelFrame, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
playerSPLabelFrame2 = ttk.LabelFrame(root, text="Player Shields 2",
                                     borderwidth=2, relief="groove")
playerSPProgressBar2 = ttk.Progressbar(
    playerSPLabelFrame2, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
playerSPLabelFrame3 = ttk.LabelFrame(root, text="Player Shields 3",
                                     borderwidth=2, relief="groove")
playerSPProgressBar3 = ttk.Progressbar(
    playerSPLabelFrame3, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
enemySPLabelFrame = ttk.LabelFrame(root, text="Enemy Shields",
                                   borderwidth=2, relief="groove")
enemySPLabelFrame2 = ttk.LabelFrame(root, text="Enemy Shields 2",
                                    borderwidth=2, relief="groove")
enemySPLabelFrame3 = ttk.LabelFrame(root, text="Enemy Shields 3",
                                    borderwidth=2, relief="groove")
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
        playerSPLabelFrame, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1
x = player2.shields
n = 0
while(n < x):
    playerShields2.append(ttk.Progressbar(
        playerSPLabelFrame2, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1
x = player3.shields
n = 0
while(n < x):
    playerShields3.append(ttk.Progressbar(
        playerSPLabelFrame3, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1

x = enemy.shields
n = 0
while(n < x):
    enemyShields.append(ttk.Progressbar(
        enemySPLabelFrame, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1
x = enemy2.shields
n = 0
while(n < x):
    enemyShields2.append(ttk.Progressbar(
        enemySPLabelFrame2, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1
x = enemy3.shields
n = 0
while(n < x):
    enemyShields3.append(ttk.Progressbar(
        enemySPLabelFrame3, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1

label.place(x=1000, y=900)
# ship armor
playerAPLabelFrame = ttk.LabelFrame(root, text="Player Armor",
                                    borderwidth=2, relief="groove")
playerAPProgressBar = ttk.Progressbar(
    playerAPLabelFrame, maximum=player.ap, length=(ui_metrics.shipDataWidth-10), variable=100)
playerAPLabelFrame2 = ttk.LabelFrame(root, text="Player Armor 2",
                                     borderwidth=2, relief="groove")
playerAPProgressBar2 = ttk.Progressbar(
    playerAPLabelFrame2, maximum=player.ap, length=(ui_metrics.shipDataWidth-10), variable=100)
playerAPLabelFrame3 = ttk.LabelFrame(root, text="Player Armor 3",
                                     borderwidth=2, relief="groove")
playerAPProgressBar3 = ttk.Progressbar(
    playerAPLabelFrame3, maximum=player.ap, length=(ui_metrics.shipDataWidth-10), variable=100)
enemyAPLabelFrame = ttk.LabelFrame(root, text="Enemy Armor",
                                   borderwidth=2, relief="groove")
enemyAPProgressBar = ttk.Progressbar(
    enemyAPLabelFrame, maximum=enemy.ap, length=(ui_metrics.shipDataWidth-10), variable=100)
enemyAPLabelFrame2 = ttk.LabelFrame(root, text="Enemy Armor 2",
                                    borderwidth=2, relief="groove")
enemyAPProgressBar2 = ttk.Progressbar(
    enemyAPLabelFrame2, maximum=enemy.ap, length=(ui_metrics.shipDataWidth-10), variable=100)

enemyAPLabelFrame3 = ttk.LabelFrame(root, text="Enemy Armor 3",
                                    borderwidth=2, relief="groove")
enemyAPProgressBar3 = ttk.Progressbar(
    enemyAPLabelFrame3, maximum=enemy.ap, length=(ui_metrics.shipDataWidth-10), variable=100)

# ship hp
playerHPLabelFrame = ttk.LabelFrame(root, text="Player HP",
                                    borderwidth=2, relief="groove")
playerHPProgressBar = ttk.Progressbar(
    playerHPLabelFrame, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
playerHPLabelFrame2 = ttk.LabelFrame(root, text="Player HP 2",
                                     borderwidth=2, relief="groove")
playerHPProgressBar2 = ttk.Progressbar(
    playerHPLabelFrame2, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)

playerHPLabelFrame3 = ttk.LabelFrame(root, text="Player HP 3",
                                     borderwidth=2, relief="groove")
playerHPProgressBar3 = ttk.Progressbar(
    playerHPLabelFrame3, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)

enemyHPLabelFrame = ttk.LabelFrame(root, text="Enemy HP",
                                   borderwidth=2, relief="groove")
enemyHPProgressBar = ttk.Progressbar(
    enemyHPLabelFrame, maximum=enemy.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
enemyHPLabelFrame2 = ttk.LabelFrame(root, text="Enemy HP 2",
                                    borderwidth=2, relief="groove")
enemyHPProgressBar2 = ttk.Progressbar(
    enemyHPLabelFrame2, maximum=enemy.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
enemyHPLabelFrame3 = ttk.LabelFrame(root, text="Enemy HP 3",
                                    borderwidth=2, relief="groove")
enemyHPProgressBar3 = ttk.Progressbar(
    enemyHPLabelFrame3, maximum=enemy.hp, length=(ui_metrics.shipDataWidth-10), variable=100)

######################################################### PLACE ####################################
# left section
ammunitionChoiceScale.place(x=20, y=ui_metrics.canvasY+60)
accuracyChoiceScale.place(x=20, y=ui_metrics.canvasY+140)
# upper section
shipChoiceRadioButton1.place(
    x=ui_metrics.canvasX + 540, y=ui_metrics.canvasY - 60)
shipChoiceRadioButton2.place(
    x=ui_metrics.canvasX + 700, y=ui_metrics.canvasY - 60)
shipChoiceRadioButton3.place(
    x=ui_metrics.canvasX + 860, y=ui_metrics.canvasY - 60)

ammunitionChoiceRadioButton1.place(
    x=ui_metrics.canvasX + ui_metrics.canvasWidth + 20, y=ui_metrics.canvasY - 60)
ammunitionChoiceRadioButton2.place(
    x=ui_metrics.canvasX + ui_metrics.canvasWidth + 20, y=ui_metrics.canvasY - 40)
ammunitionChoiceRadioButton3.place(
    x=ui_metrics.canvasX + ui_metrics.canvasWidth + 20, y=ui_metrics.canvasY - 20)

gameSpeedScale.place(x=ui_metrics.canvasX, y=ui_metrics.canvasY - 80)
canvas.place(x=ui_metrics.canvasX, y=ui_metrics.canvasY)
timeElapsedProgressBar.place(
    x=ui_metrics.canvasX+120, y=ui_metrics.canvasY - 60)
timeElapsedLabel.place(x=ui_metrics.canvasX+140, y=ui_metrics.canvasY - 80)
gameSpeedScale.place(x=ui_metrics.canvasX, y=ui_metrics.canvasY - 80)

# ship displays
# playerDisplay.place(x=ui_metrics.canvasX,
#                   y=ui_metrics.canvasY + ui_metrics.canvasHeight)
# enemyDisplay.place(x=ui_metrics.canvasX+400,
#                   y=ui_metrics.canvasY + ui_metrics.canvasHeight)

# ship shields                                                                              1
playerSPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 80, anchor="nw")
playerSPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + 80, anchor="nw")
playerSPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 2*ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + 80, anchor="nw")
enemySPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 3*ui_metrics.shipDataWidth,
                        y=ui_metrics.canvasY + ui_metrics.canvasHeight + 80, anchor="nw")
enemySPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 4*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 80, anchor="nw")
enemySPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 5*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 80, anchor="nw")

tmp = 0
for progressBar in playerShields:
    progressBar.place(x=tmp + 5, y=5)
    tmp += ((ui_metrics.shipDataWidth-10) /
            (player.shields*4+(player.shields-1)))*5
tmp = 0
for progressBar in playerShields2:
    progressBar.place(x=tmp + 5, y=5)
    tmp += ((ui_metrics.shipDataWidth-10) /
            (player2.shields*4+(player2.shields-1)))*5
tmp = 0
for progressBar in playerShields3:
    progressBar.place(x=tmp + 5, y=5)
    tmp += ((ui_metrics.shipDataWidth-10) /
            (player3.shields*4+(player3.shields-1)))*5

tmp = 0
for progressBar in enemyShields:
    progressBar.place(x=tmp + 5, y=5)
    tmp += ((ui_metrics.shipDataWidth-10) /
            (enemy.shields*4+(enemy.shields-1)))*5
tmp = 0
for progressBar in enemyShields2:
    progressBar.place(x=tmp + 5, y=5)
    tmp += ((ui_metrics.shipDataWidth-10) /
            (enemy2.shields*4+(enemy2.shields-1)))*5
tmp = 0
for progressBar in enemyShields3:
    progressBar.place(x=tmp + 5, y=5)
    tmp += ((ui_metrics.shipDataWidth-10) /
            (enemy3.shields*4+(enemy3.shields-1)))*5

# ship armor   player
playerAPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 140, anchor="nw")
playerAPProgressBar.place(x=2, y=5)
playerAPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + 140, anchor="nw")
playerAPProgressBar2.place(x=2, y=5)
playerAPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 2*ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + 140, anchor="nw")
playerAPProgressBar3.place(x=2, y=5)

enemyAPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 3*ui_metrics.shipDataWidth,
                        y=ui_metrics.canvasY + ui_metrics.canvasHeight + 140, anchor="nw")
enemyAPProgressBar.place(x=2, y=5)
enemyAPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 4*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 140, anchor="nw")
enemyAPProgressBar2.place(x=2, y=5)
enemyAPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 5*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 140, anchor="nw")
enemyAPProgressBar3.place(x=2, y=5)

# ship hp      player                                                                        1
playerHPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 200, anchor="nw")
playerHPProgressBar.place(x=2, y=5)
playerHPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + 200, anchor="nw")
playerHPProgressBar2.place(x=2, y=5)
playerHPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 2*ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + 200, anchor="nw")
playerHPProgressBar3.place(x=2, y=5)
enemyHPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 3*ui_metrics.shipDataWidth,
                        y=ui_metrics.canvasY + ui_metrics.canvasHeight + 200, anchor="nw")
enemyHPProgressBar.place(x=2, y=5)
enemyHPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX+4*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 200, anchor="nw")
enemyHPProgressBar2.place(x=2, y=5)
enemyHPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX+5*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + 200, anchor="nw")
enemyHPProgressBar3.place(x=2, y=5)


######################### right section ###################################
startTurnButton.place(x=(ui_metrics.canvasX+ui_metrics.canvasWidth + 80),
                      y=ui_metrics.canvasY+ui_metrics.canvasHeight-20)

distanceLabel.place(x=ui_metrics.canvasX +
                    ui_metrics.canvasWidth - 160, y=ui_metrics.canvasY - 20)
# create list of elements to disable if round is in progress
UIElementsList.append(ammunitionChoiceScale)
UIElementsList.append(accuracyChoiceScale)
UIElementsList.append(gameSpeedScale)
UIElementsList.append(startTurnButton)

RadioElementsList.append(shipChoiceRadioButton1)
RadioElementsList.append(shipChoiceRadioButton2)
RadioElementsList.append(shipChoiceRadioButton3)
RadioElementsList.append(ammunitionChoiceRadioButton1)
RadioElementsList.append(ammunitionChoiceRadioButton2)
RadioElementsList.append(ammunitionChoiceRadioButton3)
# clock
update()


root.mainloop()
