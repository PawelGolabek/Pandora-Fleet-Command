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

#   Artemis 2021
#   Project by Paweł Gołąbek
#
#   Used libraries (excluding build-in): Pillow, Pil


root = tk.Tk()

UIScale = 1

rootX = 1200
rootY = 800

root.geometry(str(rootX*UIScale) + "x" + str(rootY*UIScale))


class global_var():
    a = 0
    canvasX = 200
    canvasY = 100
    # CANVAS OPTIONS
    canvasWidth = 800
    canvasHeight = 600
    ## INPUT HANDLING ##
    mouseButton1 = False
    pointerX = 0
    pointerY = 0
    ## GAME OPTIONS ##
    fogOfWar = TRUE
    gameSpeed = 1
    turnBased = TRUE
    turnLength = 360
    # GAME DATA
    turnInProgress = FALSE
    currentMissles = []


class ammunition():
    def __init__(self, name='type1', shotsPerTurn=5, damage=10, damageFalloffStart=200, damageFalloffStop=400, defaultAccuracy=90, special=None):
        self.name = name
        self.shotsPerTurn = shotsPerTurn
        self.damage = damage
        self.damageFalloffStart = damageFalloffStart
        self.damageFalloffStop = damageFalloffStop
        self.defaultAccuracy = defaultAccuracy
        self.special = special


type1 = ammunition(name='type1', shotsPerTurn=8,
                   damage=20)  # placeholder values
type2 = ammunition(name="type2", shotsPerTurn=2,
                   damage=20)  # placeholder values
type3 = ammunition(name="type3", shotsPerTurn=1,
                   damage=20)  # placeholder values
type4 = ammunition(name="type4", shotsPerTurn=4,
                   damage=20)  # placeholder values


class ship():
    def __init__(self, name="USS Artemis", owner="ai`", xPos=300, yPos=300, health={'section1': 100, 'section2': 100, 'section3': 100, 'section4': 100}, typesOfAmmunition=[type1, type2, type3, type4], ammunitionNumber=[3, 3, 3, 3], ammunitionChoice='', detectionRange=200, moveOrderX=None, moveOrderY=None, xDir=0.0, yDir=1.0, turnRate=0.5, speed=40, outlineColor="red", visible=FALSE):

        self.owner = owner
        self.name = name
        self.xPos = xPos
        self.yPos = yPos
        self.health = health
        self.typesOfAmmunition = typesOfAmmunition
        self.ammunitionNumber = ammunitionNumber
        self.ammunitionChoice = ammunitionChoice
        self.detectionRange = detectionRange
        self.moveOrderX = moveOrderX
        self.moveOrderY = moveOrderY
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.speed = speed
        self.outlineColor = outlineColor
        self.visible = visible


class playerController():
    a = 10


class aiController():
    def ammunitionChoice(ship):
        ship.ammunitionChoice = 'type2'

    a = 10


def update():
    globalVar.gameSpeed = gameSpeedScale.get()
    canvas.delete('all')
    canvas.create_image(0, 0, image=img, anchor='nw')
    getOrders(player)
    getOrders(enemy)
    ticksToEndFrame = 0
    if(not globalVar.turnBased or globalVar.turnInProgress):
        detectionCheck()
        while(ticksToEndFrame < globalVar.gameSpeed):
            updateShip(player)
            updateShip(enemy)
            manageShots(player, enemy)   # check if ship shot
            manageShots(enemy, player)
            manageRockets()   # manage mid-air munitions
            ticksToEndFrame += 1
            timeElapsedProgressBar['value'] += 1
            if(timeElapsedProgressBar['value'] > 359):
                endTurn()
                break
    drawShip(player)
    drawShip(enemy)
    globalVar.mouseButton1 = False
    root.after(10, update)


def updateShip(ship):  # rotate and move the chosen ship
    if(ship.moveOrderX):
        # vector normalisation
        scale = math.sqrt((ship.moveOrderX-ship.xPos)*(ship.moveOrderX-ship.xPos) +
                          (ship.moveOrderY-ship.yPos)*(ship.moveOrderY-ship.yPos))

        # move order into normalised vector
        moveDirX = -(ship.xPos-ship.moveOrderX) / scale
        moveDirY = -(ship.yPos-ship.moveOrderY) / scale

        # x is same quadrant y same
        degree = ship.turnRate
        rotateVector(degree, ship, moveDirX, moveDirY)
        # print(ship.xDir)
    ship.xPos += ship.xDir*ship.speed/360
    ship.yPos += ship.yDir*ship.speed/360


def drawShip(ship):  # draw ship on the map with all of its accesories
    if(ship.moveOrderX):
        if(ship.owner == "player1" or (not globalVar.fogOfWar or enemy.visible)):  # draw order
            canvas.create_line(ship.xPos, ship.yPos, ship.moveOrderX,
                               ship.moveOrderY,   fill='white')

        scale = math.sqrt((ship.moveOrderX-ship.xPos)*(ship.moveOrderX-ship.xPos) +  # normalise vector of order
                          (ship.moveOrderY-ship.yPos)*(ship.moveOrderY-ship.yPos))
        moveDirX = -(ship.xPos-ship.moveOrderX) / scale
        moveDirY = -(ship.yPos-ship.moveOrderY) / scale
        if(ship.owner == "player1" or (not globalVar.fogOfWar or enemy.visible)):
            canvas.create_line(ship.xPos, ship.yPos,   ship.xPos +
                               (moveDirX*120), ship.yPos + (moveDirY*120),   fill='green')

    # move order into normalised vector
    if(ship.owner == "ai1"):
        if(not globalVar.fogOfWar or enemy.visible):
            canvas.create_oval(ship.xPos-ship.detectionRange, ship.yPos - ship.detectionRange,
                               ship.xPos + ship.detectionRange, ship.yPos+ship.detectionRange, outline=ship.outlineColor)
            canvas.create_line(ship.xPos-5, ship.yPos-5, ship.xPos +
                               5, ship.yPos+5,   fill='white')
    else:
        canvas.create_oval(ship.xPos-ship.detectionRange, ship.yPos - ship.detectionRange, ship.xPos +
                           ship.detectionRange, ship.yPos+ship.detectionRange, outline=ship.outlineColor)
        canvas.create_line(ship.xPos-5, ship.yPos-5,
                           ship.xPos + 5, ship.yPos+5,   fill='white')
    if(ship.owner == "player1" or (not globalVar.fogOfWar or enemy.visible)):
        canvas.create_line(ship.xPos, ship.yPos,   ship.xPos+(ship.xDir*200),
                           ship.yPos+(ship.yDir*200), fill="black")


def manageShots(ship, enemy):
    if(ship.ammunitionChoice == 'type1'):
        shotInterval = globalVar.turnLength/type1.shotsPerTurn
    if(ship.ammunitionChoice == 'type2'):
        shotInterval = globalVar.turnLength/type2.shotsPerTurn
    if(ship.ammunitionChoice == 'type3'):
        shotInterval = globalVar.turnLength/type3.shotsPerTurn
    if(ship.ammunitionChoice == 'type4'):
        shotInterval = globalVar.turnLength/type4.shotsPerTurn

    if(timeElapsedProgressBar['value'] % shotInterval == 0 and enemy.visible == TRUE):
        globalVar.currentMissles.append(ship.ammunitionChoice)
        print(ship.name + " fired " + ship.ammunitionChoice)


def manageRockets():    # mid-air munitions
    x = 1


def getOrders(ship):
    if(ship.owner == "player1"):
        if(globalVar.mouseButton1 and globalVar.pointerX > 0 and globalVar.pointerX < (globalVar.canvasWidth) and globalVar.pointerY > 0 and globalVar.pointerY < (globalVar.canvasHeight)):
            ship.moveOrderX = globalVar.pointerX
            ship.moveOrderY = globalVar.pointerY
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


def motion(event):
    globalVar.pointerX = root.winfo_pointerx() - root.winfo_x() - \
        globalVar.canvasX-7
    globalVar.pointerY = root.winfo_pointery() - root.winfo_y() - \
        globalVar.canvasY - 31
  #  print(str(globalVar.pointerX) + " " + str(globalVar.pointerY))


def mouseButton1(event):  # get left mouse button and set it in globalvar
    if event:
        globalVar.mouseButton1 = True
    else:
        globalVar.mouseButton1 = False


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


def startTurn():
    globalVar.turnInProgress = TRUE
    timeElapsedProgressBar['value'] = 0
    player.ammunitionChoice = (choices.get())
    aiController.ammunitionChoice(enemy)
    for object in UIElementsList:
        object.config(state=DISABLED, background="#D0D0D0")


def endTurn():
    globalVar.turnInProgress = FALSE
    for object in UIElementsList:
        object.config(state=NORMAL, background="#F0F0F0")


# main
root.bind('<Motion>', motion)
root.bind('<Button-1>', mouseButton1)

root.title("USS Artemis")
globalVar = global_var()

player = ship(outlineColor="white", owner="player1")
enemy = ship(xPos=43, outlineColor="red",
             owner="ai1", ammunitionChoice='type2', name="RDD HellWitch")


# canvas
# choose image
img = Image.open('map.jpg')
# resize image
img = img.resize(
    (globalVar.canvasWidth, globalVar.canvasHeight), Image.ANTIALIAS)
# save image
img.save('resized_image.jpg')

canvas = Canvas(root, width=globalVar.canvasWidth,
                height=globalVar.canvasHeight)

img = PhotoImage("resized_image.png")
canvas.imageList = []
# item with background to avoid python bug people were mentioning about disappearing non-anchored images

canvas.imageList.append(img)

UIElementsList = []
ammunitionChoice = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Number of shots", to=len(player.typesOfAmmunition), relief=RIDGE)

accuracyChoice = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Time to aim", to=4, relief=RIDGE)

gameSpeedScale = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Playback speed", from_=1, to=16, resolution=-20, variable=2, relief=RIDGE)

pixel = tk.PhotoImage(width=1, height=1)
img = tk.PhotoImage(file=r'resized_image.png')
gameSpeedScale.set(3)
timeElapsedProgressBar = ttk.Progressbar(root, maximum=globalVar.turnLength, variable=1,  orient='horizontal',
                                         mode='determinate', length=400)

startTurnButton = tk.Button(root, text="Start turn", command=startTurn)

options = [
    type1.name,
    type2.name,
    type3.name
]
choices = StringVar()
choices.set(options[0])

ammunitionChoiceDropdown = tk.OptionMenu(
    root, choices, *options)

"""
scrollbar = Scrollbar(root)

consoleFrame = tk.Frame(root, width=globalVar.canvasWidth, height=20)

Label_middle = tk.Text(consoleFrame, height=5, font="COURIER 10", width=10,
                       bg="black", fg="white", highlightthickness=2, highlightcolor="grey")

consoleFrame.place(x=globalVar.canvasX,  # don't know how it works ... Tkinter mysteries ...
                   y=(globalVar.canvasY+globalVar.canvasHeight+44), anchor='center')

Label_middle.insert(tk.END, "Welcome aboard, captain!\n")
Label_middle.config(state=DISABLED)
scrollbar.place(in_=Label_middle, relx=1.0, rely=0,
                height=80)
scrollbar.config(command=Label_middle.yview)
"""

ammunitionChoice.place(x=20, y=20)
accuracyChoice.place(x=20, y=100)
ammunitionChoiceDropdown.place(x=20, y=180)
gameSpeedScale.place(x=globalVar.canvasX, y=globalVar.canvasY - 80)
canvas.place(x=globalVar.canvasX, y=globalVar.canvasY)
timeElapsedProgressBar.place(
    x=globalVar.canvasX+160, y=globalVar.canvasY - 80)
startTurnButton.place(x=(globalVar.canvasX+globalVar.canvasWidth + 80),
                      y=globalVar.canvasY+globalVar.canvasHeight-20)

# create list of elements to disable if round is in progress
UIElementsList.append(ammunitionChoice)
UIElementsList.append(accuracyChoice)
UIElementsList.append(gameSpeedScale)
UIElementsList.append(startTurnButton)
UIElementsList.append(ammunitionChoiceDropdown)
# clock
update()


root.mainloop()
