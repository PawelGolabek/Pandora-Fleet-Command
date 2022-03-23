import os
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
import ctypes
from win32api import GetSystemMetrics

#   Artemis 2021
#   Project by Pawel Golabek
#
#   Used libraries (excluding build-in): Pillow, Pil

root = tk.Tk()

UIScale = 1

rootX = 1600
rootY = 1080

root.geometry(str(rootX*UIScale) + "x" + str(rootY*UIScale))


class global_var():
    # CANVAS OPTIONS
    canvasX = 140
    canvasY = 100
    canvasWidth = 800
    canvasHeight = 600
    ## INPUT HANDLING ##
    mouseWheelUp = FALSE
    mouseWheelDown = FALSE
    mouseButton1 = FALSE
    pointerX = 0
    pointerY = 0
    ## GAME OPTIONS ##
    fogOfWar = TRUE
    gameSpeed = 1
    turnBased = TRUE
    turnLength = 360
    zoom = 1
    # GAME DATA
    turnInProgress = FALSE
    misslesShot = 0
    currentMissles = []
    img = PhotoImage('1/map.png')
    image = Image.open('1/map.png')
    imageMask = Image.open('1/mapMask.png')
    # ZOOM
    mouseX = canvasWidth/2
    mouseY = canvasHeight/2
    left = 0
    right = canvasWidth
    top = 0
    bottom = canvasHeight
    yellowX = 0
    yellowY = 0
    zoomChange = False


class game_rules:
    movementPenalityHard = 0.9
    movementPenalityMedium = 0.5


class _events:
    enemyDestroyed = False
    playerDestroyed = False


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


class type1a(ammunition):
    def __init__(self, name='', typeName='', owner='', target='', xDir=0, yDir=0, turnRate=0, speed=100, shotsPerTurn=5,
                 damage=10, damageFalloffStart=200, damageFalloffStop=400, defaultAccuracy=90, special=None):  # placeholder values
        super(type1a, self).__init__(name, typeName, owner, target, xDir, yDir, turnRate, speed, shotsPerTurn,
                                     damage, damageFalloffStart, damageFalloffStop, defaultAccuracy, special)
    typeName = 'type1a'
    shotsPerTurn = 8
    damage = 6
    turnRate = 5


class type2a(ammunition):
    def __init__(self, name='', typeName='', owner='', target='', xDir=0, yDir=0, turnRate=0, speed=100, shotsPerTurn=5,
                 damage=10, damageFalloffStart=200, damageFalloffStop=400, defaultAccuracy=90, special=None):  # placeholder values
        super(type2a, self).__init__(name, typeName, owner, target, xDir, yDir, turnRate, speed, shotsPerTurn,
                                     damage, damageFalloffStart, damageFalloffStop, defaultAccuracy, special)
    typeName = 'type2a'
    shotsPerTurn = 12
    damage = 2
    turnRate = 6


class type3a(ammunition):
    def __init__(self, name='', typeName='', owner='', target='', xDir=0, yDir=0, turnRate=0, speed=100, shotsPerTurn=5,
                 damage=10, damageFalloffStart=200, damageFalloffStop=400, defaultAccuracy=90, special=None):  # placeholder values
        super(type3a, self).__init__(name, typeName, owner, target, xDir, yDir, turnRate, speed, shotsPerTurn,
                                     damage, damageFalloffStart, damageFalloffStop, defaultAccuracy, special)
    typeName = 'type3a'
    shotsPerTurn = 1
    damage = 2
    turnRate = 10


ammunition_lookup = dict
ammunition_lookup = {"type1a": type1a,
                     'type2a': type2a,
                     'type3a': type3a,
                     }


class ship():
    def __init__(self, name="USS Artemis", owner="ai`", hp=200, xPos=300, yPos=300, health={'section1': 100, 'section2': 100, 'section3': 100, 'section4': 100}, typesOfAmmunition=[type1a, type2a, type3a], ammunitionNumber=[15, 15, 15, 15], ammunitionChoice='type1a', detectionRange=200, xDir=0.0, yDir=1.0, turnRate=0.5, speed=40, outlineColor="red"):
        # Init info
        self.owner = owner
        self.name = name
        self.xPos = xPos
        self.yPos = yPos
        self.health = health
        self.typesOfAmmunition = typesOfAmmunition
        self.ammunitionNumber = ammunitionNumber
        self.ammunitionChoice = ammunitionChoice
        self.detectionRange = detectionRange
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.speed = speed
        self.outlineColor = outlineColor
        self.hp = hp
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
        ship.ammunitionChoice = 'type1a'

    def accuracyChoiceScale(ship):  # virtual choice for AI Controller
        return 3

    def ammunitionChoiceScale(ship):  # virtual choice for AI Controller
        return 1

    a = 10


################################################ SHIP #########################################

def updateShip(ship):  # rotate and move the chosen ship
    if(ship.moveOrderX):
        # check for terrain
        colors = globalVar.imageMask.getpixel((int(ship.xPos), int(ship.yPos)
                                               ))
        print(ship.name + " " + str((colors[0]) +
                                    (colors[1]) + (colors[2])/3))

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


def drawShip(ship):  # draw ship on the map with all of its accesories

    drawX = (ship.xPos - globalVar.left) * \
        globalVar.zoom   # get coords relative to window
    drawY = (ship.yPos - globalVar.top) * globalVar.zoom

    if(ship.moveOrderX):
        drawOrderX = (ship.moveOrderX - globalVar.left) * \
            globalVar.zoom    # get order relative to window
        drawOrderY = (ship.moveOrderY - globalVar.top) * globalVar.zoom
        if(ship.owner == "player1" or (not globalVar.fogOfWar or enemy.visible)):  # draw order
            canvas.create_line(drawX, drawY, drawOrderX,
                               drawOrderY,   fill='white')

    if(ship.owner == "ai1"):
        if(not globalVar.fogOfWar or enemy.visible):
            canvas.create_oval(drawX-ship.detectionRange*globalVar.zoom, drawY - ship.detectionRange*globalVar.zoom,
                               drawX + ship.detectionRange*globalVar.zoom, drawY+ship.detectionRange*globalVar.zoom, outline=ship.outlineColor)
            canvas.create_line(drawX-5*globalVar.zoom, drawY-5*globalVar.zoom, drawX +
                               5*globalVar.zoom, drawY+5*globalVar.zoom, width=globalVar.zoom,  fill='white')
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


def manageShots(ship, ship2):
    # add amunition scale input
    if(ship.owner == 'player1'):
        if(ammunitionChoiceScale.get() != 0):
            shotInterval = globalVar.turnLength / \
                ammunition_lookup[ship.ammunitionChoice].shotsPerTurn
            maxShotsNotTaken = accuracyChoiceScale.get()
            if(timeElapsedProgressBar['value'] % shotInterval == 0 and ship2.visible == TRUE):
                if(ship.shotsNotTaken < maxShotsNotTaken):
                    ship.shotsNotTaken += 1
                else:
                    if(ship.shotsTaken < ammunitionChoiceScale.get()):
                        ship.shotsTaken += 1
                        createRocket(ship, ship2)
                        print(ship.name + " fired " + ship.ammunitionChoice)
    else:
        if(aiController.ammunitionChoiceScale != 0):
            shotInterval = globalVar.turnLength / \
                ammunition_lookup[ship.ammunitionChoice].shotsPerTurn
            maxShotsNotTaken = aiController.accuracyChoiceScale(ship)
            if(timeElapsedProgressBar['value'] % shotInterval == 0 and ship2.visible == TRUE):
                if(ship.shotsNotTaken < maxShotsNotTaken):
                    ship.shotsNotTaken += 1
                else:
                    if(ship.shotsTaken < aiController.ammunitionChoiceScale(ship)):
                        ship.shotsTaken += 1
                        createRocket(ship, ship2)
                        print(ship.name + " fired " + ship.ammunitionChoice)


def getOrders(ship):
    if(ship.owner == "player1"):
        if(globalVar.mouseButton1 and mouseOnCanvas()):
            ship.moveOrderX = globalVar.left + \
                (globalVar.pointerX/globalVar.zoom)
            ship.moveOrderY = globalVar.top+(globalVar.pointerY/globalVar.zoom)
    elif(ship.owner == "ai1"):
        ship.moveOrderX = 400  # insert ai contrller decision
        ship.moveOrderY = 400


def detectionCheck():
    globalVar.distance = math.sqrt(
        abs(pow(player.xPos-enemy.xPos, 2)+pow(player.yPos-enemy.yPos, 2)))

    if(globalVar.distance < player.detectionRange):
        enemy.visible = TRUE
    else:
        enemy.visible = FALSE
    if(globalVar.distance < enemy.detectionRange):
        player.visible = TRUE
    else:
        player.visible = FALSE


def dealDamage(ship, damage):
    ship_lookup[ship].hp -= damage
    if(ship_lookup[ship].hp < 1 and not events.enemyDestroyed):
        if(ship_lookup[ship].owner == 'ai1'):
            events.enemyDestroyed = True
            window = tk.Toplevel()
            label = tk.Label(window, text='yes, you won')
            label.place(x=0, y=0)
        elif(ship_lookup[ship].owner == 'player1' and events.playerDestroyed == False):
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
        drawX = (missle.xPos - globalVar.left) * globalVar.zoom   # change ###
        drawY = (missle.yPos - globalVar.top)*globalVar.zoom    # change ###
        canvas.create_line(drawX-5, drawY-5,
                           drawX+5, drawY+5)


def createRocket(ship, target):
    globalVar.misslesShot += 1
    missleClass = ammunition_lookup[ship.ammunitionChoice]
    missle = missleClass()
    globalVar.currentMissles.append(missle)
    missleName = 'missle' + str(globalVar.misslesShot)
    setattr(globalVar.currentMissles[-1], 'name', missleName)
    setattr(globalVar.currentMissles[-1], 'class', missleClass)
    setattr(globalVar.currentMissles[-1], 'xPos', ship.xPos)
    setattr(globalVar.currentMissles[-1], 'yPos', ship.yPos)
    setattr(globalVar.currentMissles[-1], 'xDir', ship.xDir)  # change later
    setattr(globalVar.currentMissles[-1], 'yDir', ship.yDir)
    setattr(globalVar.currentMissles[-1], 'owner', ship.owner)
    setattr(globalVar.currentMissles[-1], 'turnRate',
            ammunition_lookup[ship.ammunitionChoice].turnRate)
    setattr(globalVar.currentMissles[-1], 'target', target.name)


############################################ INPUTS #############################################

def motion(event):
    globalVar.pointerX = root.winfo_pointerx() - root.winfo_x() - \
        globalVar.canvasX-7
    globalVar.pointerY = root.winfo_pointery() - root.winfo_y() - \
        globalVar.canvasY - 31


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
        getOrders(player)
        getOrders(enemy)
    ticksToEndFrame = 0
    player.ammunitionChoice = (choices.get())
    if(not globalVar.turnBased or globalVar.turnInProgress):
        while(ticksToEndFrame < globalVar.gameSpeed):
            detectionCheck()
            updateShip(player)
            updateShip(enemy)
            manageShots(player, enemy)   # check if ship shot
            manageShots(enemy, player)
            manageRockets()   # manage mid-air munitions
            ticksToEndFrame += 1
            timeElapsedProgressBar['value'] += 1
            if(timeElapsedProgressBar['value'] > globalVar.turnLength):
                endTurn()
                break
    drawShip(player)
    drawShip(enemy)
    drawRockets()
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
                    globalVar.mouseX = (globalVar.pointerX + globalVar.left)
                    globalVar.mouseY = (globalVar.pointerY + globalVar.top)
                else:
                    globalVar.mouseX = (
                        globalVar.pointerX/(globalVar.zoom-1) + globalVar.left)
                    globalVar.mouseY = (
                        globalVar.pointerY/(globalVar.zoom-1) + globalVar.top)

                globalVar.yellowX = (
                    globalVar.canvasWidth/globalVar.zoom)/2
                globalVar.yellowY = (
                    globalVar.canvasHeight/globalVar.zoom)/2

                if(globalVar.mouseX > globalVar.canvasWidth - globalVar.yellowX):  # bumpers on sides
                    globalVar.mouseX = globalVar.right - globalVar.yellowX
                if(globalVar.mouseX < globalVar.yellowX):
                    globalVar.mouseX = globalVar.left + globalVar.yellowX
                if(globalVar.mouseY > globalVar.canvasHeight - globalVar.yellowY):
                    globalVar.mouseY = globalVar.bottom - globalVar.yellowY
                if(globalVar.mouseY < globalVar.yellowY):
                    globalVar.mouseY = globalVar.top + globalVar.yellowY

                globalVar.left = globalVar.mouseX - globalVar.yellowX
                globalVar.right = globalVar.mouseX + globalVar.yellowX
                globalVar.top = globalVar.mouseY - globalVar.yellowY
                globalVar.bottom = globalVar.mouseY + globalVar.yellowY
                globalVar.mouseX = globalVar.right - globalVar.left
                globalVar.mouseY = globalVar.bottom - globalVar.top

                canvas.create_oval(globalVar.mouseX, globalVar.mouseY, globalVar.mouseX +
                                   20, globalVar.mouseY + 20)
            if(globalVar.mouseWheelDown):
                globalVar.mouseX = globalVar.canvasWidth/2
                globalVar.mouseY = globalVar.canvasHeight/2
                globalVar.zoom = 1
                globalVar.left = 0
                globalVar.top = 0
                globalVar.right = globalVar.canvasWidth
                globalVar.bottom = globalVar.canvasHeight

            if(globalVar.zoom != 1):

                tmp = im.crop((globalVar.left, globalVar.top,
                               globalVar.right, globalVar.bottom))
                im = tmp
                im = im.resize(
                    (globalVar.canvasWidth, globalVar.canvasHeight), Image.ANTIALIAS)

                im.save('sadgfsd.png')  # testing delete later

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
    player.ammunitionChoice = (choices.get())
    aiController.ammunitionChoice(enemy)
    player.shotsNotTaken = 0
    enemy.shotsNotTaken = 0
    player.shotsTaken = 0
    enemy.shotsTaken = 0
    for object in UIElementsList:
        object.config(state=DISABLED, background="#D0D0D0")


def endTurn():
    globalVar.turnInProgress = FALSE
    for object in UIElementsList:
        object.config(state=NORMAL, background="#F0F0F0")


def updateScales():
    playerHPProgressBar['value'] = player.hp
    enemyHPProgressBar['value'] = enemy.hp
    ammunitionChoiceScale.config(
        to=ammunition_lookup[player.ammunitionChoice].shotsPerTurn)
    if(ammunitionChoiceScale.get() == 0):
        accuracyChoiceScale.set(0)
        accuracyChoiceScale.config(state="disabled", bg='#D0D0D0')
    else:
        if(not globalVar.turnInProgress):
            accuracyChoiceScale.config(state=NORMAL, background="#F0F0F0")

    accuracyChoiceScale.config(
        to=ammunition_lookup[player.ammunitionChoice].shotsPerTurn - ammunitionChoiceScale.get())


########################################## MULTIPURPOSE #########################################
def mouseOnCanvas():
    if(globalVar.pointerX > 0 and globalVar.pointerX < (globalVar.canvasWidth) and globalVar.pointerY > 0 and globalVar.pointerY < (globalVar.canvasHeight)):
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

root.title("USS Artemis")
globalVar = global_var()
gameRules = game_rules()
ship_lookup = dict

playerName = 'USS Artemis'
enemyName = 'RDD HellWitch'

player = ship(outlineColor="white", owner="player1", name=playerName)
enemy = ship(xPos=43, outlineColor="red",
             owner="ai1", ammunitionChoice='type1a', name=enemyName)

events = _events()

ship_lookup = {playerName: player,
               enemyName: enemy}

# canvas
# choose image
img = Image.open('1/map.png')
# resize image
img = img.resize((globalVar.canvasWidth, globalVar.canvasHeight))
# save image
img.save('resized_image.png')


canvas = Canvas(root, width=globalVar.canvasWidth,
                height=globalVar.canvasHeight)

globalVar.img = PhotoImage("resized_image.png")
canvas.imageList = []
# item with background to avoid python bug people were mentioning about disappearing non-anchored images

globalVar.imageMask = Image.open("1/mapMask.png")
img = Image.open('1/map.png')
im = img.resize(
    (globalVar.canvasWidth, globalVar.canvasHeight), Image.ANTIALIAS)

globalVar.imageMask = globalVar.imageMask.resize(
    (globalVar.canvasWidth, globalVar.canvasHeight), Image.ANTIALIAS)

globalVar.im = ImageTk.PhotoImage(im)
canvas.imageList.append(im)
canvas.imageList.append(globalVar.img)

UIElementsList = []

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
                                         mode='determinate', length=400)

startTurnButton = tk.Button(root, text="Start turn", command=startTurn)

options = [
    type1a.typeName,
    type2a.typeName,
    type3a.typeName,
]

choices = StringVar()
choices.set(options[0])

ammunitionChoiceDropdown = tk.OptionMenu(
    root, choices, *options)
ammunitionChoiceDropdown.config(width=10)

shipImage1 = Image.open('ship_modules/ship.png')
shipImage = shipImage1.resize(
    (math.floor(globalVar.canvasWidth/2), math.floor(globalVar.canvasHeight/4)), Image.ANTIALIAS)
canvas.imageList.append(shipImage)
playerImage = ImageTk.PhotoImage(shipImage)
playerDisplay = tk.Label(root, image=playerImage)

enemyImage = ImageTk.PhotoImage(shipImage)
enemyDisplay = tk.Label(root, image=enemyImage)

distanceLabelFrame = ttk.LabelFrame(
    root, text='Distance between ships', width=1000, height=200)
distanceLabel = tk.Label(distanceLabelFrame, text='0000000')
playerHPLabelFrame = ttk.LabelFrame(root, text="Player HP",
                                    borderwidth=2, relief="groove")
playerHPProgressBar = ttk.Progressbar(
    playerHPLabelFrame, maximum=player.hp, length=390, variable=100)
enemyHPLabelFrame = ttk.LabelFrame(root, text="Enemy HP",
                                   borderwidth=2, relief="groove")
enemyHPProgressBar = ttk.Progressbar(
    enemyHPLabelFrame, maximum=enemy.hp, length=390, variable=100)


######################################################### PLACE ####################################
# left section
ammunitionChoiceScale.place(x=20, y=globalVar.canvasY+60)
accuracyChoiceScale.place(x=20, y=globalVar.canvasY+140)
gameSpeedScale.place(x=globalVar.canvasX, y=globalVar.canvasY - 80)
canvas.place(x=globalVar.canvasX, y=globalVar.canvasY)
timeElapsedProgressBar.place(
    x=globalVar.canvasX+120, y=globalVar.canvasY - 60)
timeElapsedLabel.place(x=globalVar.canvasX+140, y=globalVar.canvasY - 80)
startTurnButton.place(x=(globalVar.canvasX+globalVar.canvasWidth + 80),
                      y=globalVar.canvasY+globalVar.canvasHeight-20)
# ship displays
playerDisplay.place(x=globalVar.canvasX,
                    y=globalVar.canvasY + globalVar.canvasHeight)
enemyDisplay.place(x=globalVar.canvasX+400,
                   y=globalVar.canvasY + globalVar.canvasHeight)

# ship hp
playerHPLabelFrame.place(width=400, height=54, x=globalVar.canvasX,
                         y=globalVar.canvasY + globalVar.canvasHeight + 160, anchor="nw")
playerHPProgressBar.place(x=2, y=5)
enemyHPLabelFrame.place(width=400, height=54, x=globalVar.canvasX+400,
                        y=globalVar.canvasY + globalVar.canvasHeight + 160, anchor="nw")
enemyHPProgressBar.place(x=2, y=5)

# right section
ammunitionChoiceDropdown.place(
    x=globalVar.canvasX + globalVar.canvasWidth + 20, y=globalVar.canvasY)

distanceLabel.place(x=globalVar.canvasX +
                    globalVar.canvasWidth - 160, y=globalVar.canvasY - 20)
# create list of elements to disable if round is in progress
UIElementsList.append(ammunitionChoiceScale)
UIElementsList.append(accuracyChoiceScale)
UIElementsList.append(gameSpeedScale)
UIElementsList.append(startTurnButton)
UIElementsList.append(ammunitionChoiceDropdown)
# clock
update()


root.mainloop()
