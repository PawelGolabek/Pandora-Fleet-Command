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

#   Artemis 2021
#   Project by Paweł Gołąbek
#
#   Used libraries: Pillow, Pil

# sciezkaPython = os.getcwd()


root = tk.Tk()

UIScale = 1

rootX = 1200
rootY = 800

root.geometry(str(rootX*UIScale) + "x" + str(rootY*UIScale))


class ship():
    def __init__(self, owner="ai`", xPos=300, yPos=300, health={'section1': 100, 'section2': 100, 'section3': 100, 'section4': 100}, typesOfAmmunition={"type1:": 0, "type2": 0, "type3": 0, "type4": 0}, detectionRange=200, moveOrderX=None, moveOrderY=None, xDir=0.0, yDir=1.0, turnRate=0.5, speed=40, outlineColor="red", visible=FALSE):

        self.owner = owner
        self.xPos = xPos
        self.yPos = yPos
        self.health = health
        self.typesOfAmmunition = typesOfAmmunition
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
    a = 10


class global_var():
    a = 0
    flag = FALSE
    canvasX = 200
    canvasY = 100
    pointerX = 0
    pointerY = 0
    canvasWidth = 800
    canvasHeight = 600
    mouseButton1 = False
    toDeleteNextFrame = []
    ## GAME OPTIONS ##
    fogOfWar = TRUE
    gameSpeed = 1
    turnBased = False


def update():
    globalVar.gameSpeed = gameSpeedScale.get()
    canvas.delete('all')
    canvas.create_image(0, 0, image=img, anchor='nw')
    detectionCheck()
    updateShip(player)
    drawShip(player)
    updateShip(enemy)
    drawShip(enemy)
    print(gameSpeedScale.get())
    root.after(10, update)
    globalVar.mouseButton1 = False


def deleteNextFrame():
    for thing in globalVar.toDeleteNextFrame:
        thing.destroy()


"""
def updateRectangle(): ######## testing purpose function to delete later

    b = (abs(math.sin(globalVar.a/100))) * 120
    canvas.create_oval(b+5, b+5, 205-b, 205-b, outline='white')
    canvas.create_oval(globalVar.a+5, globalVar.a+5, 205 -
                       globalVar.a, 205-globalVar.a, outline='green')
    # canvas.create_text(100, 10, text=globalVar.a, font="arial 54")
    # canvas.create_text(55, 55, font="arial 54", text=round(b))

    if(globalVar.a > 99):
        globalVar.flag = False
    if(globalVar.a < 1):
        globalVar.flag = True

    if(globalVar.flag):
        globalVar.a += 1
    else:
        globalVar.a -= 1"""


def updateShip(ship):  # rotate and move the chosen ship

    if(ship.owner == "player1"):
        if(globalVar.mouseButton1 and globalVar.pointerX > 0 and globalVar.pointerX < (globalVar.canvasWidth) and globalVar.pointerY > 0 and globalVar.pointerY < (globalVar.canvasHeight)):
            ship.moveOrderX = globalVar.pointerX
            ship.moveOrderY = globalVar.pointerY
    elif(ship.owner == "ai1"):
        ship.moveOrderX = 400  # insert ai contrller decision
        ship.moveOrderY = 400

    if(ship.moveOrderX):
        if(ship.owner == "player1" or (not globalVar.fogOfWar or enemy.visible)):
            canvas.create_line(ship.xPos, ship.yPos, ship.moveOrderX,
                               ship.moveOrderY,   fill='white')
        # vector normalisation
        scale = math.sqrt((ship.moveOrderX-ship.xPos)*(ship.moveOrderX-ship.xPos) +
                          (ship.moveOrderY-ship.yPos)*(ship.moveOrderY-ship.yPos))

        # move order into normalised vector
        moveDirX = -(ship.xPos-ship.moveOrderX) / scale
        moveDirY = -(ship.yPos-ship.moveOrderY) / scale

        if(ship.owner == "player1" or (not globalVar.fogOfWar or enemy.visible)):
            canvas.create_line(ship.xPos, ship.yPos,   ship.xPos +
                               (moveDirX*120), ship.yPos + (moveDirY*120),   fill='green')

        # x is same quadrant y same
        degree = ship.turnRate*globalVar.gameSpeed
        if((ship.xDir > moveDirX and ship.yDir > -moveDirY) or ship.xDir < moveDirX and ship.yDir < -moveDirY):

            degree = ship.turnRate*globalVar.gameSpeed
            ship.xDir = math.cos((degree/360)*math.pi)*ship.xDir - \
                math.sin((degree/360)*math.pi)*ship.yDir
            ship.yDir = math.sin((degree/360)*math.pi)*ship.xDir + \
                math.cos((degree/360)*math.pi)*ship.yDir
        else:
            degree = -ship.turnRate*globalVar.gameSpeed  # change direction
            ship.xDir = math.cos((degree/360)*math.pi)*ship.xDir -  \
                math.sin((degree/360)*math.pi)*ship.yDir
            ship.yDir = math.sin((degree/360)*math.pi)*ship.xDir + \
                math.cos((degree/360)*math.pi)*ship.yDir

        scale = math.sqrt(abs(ship.xDir*ship.xDir+ship.yDir*ship.yDir))

        # move direviton into normalised vector
        if(scale != 0):
            ship.xDir = ship.xDir / scale
            ship.yDir = ship.yDir / scale

            if(ship.owner == "player1" or (not globalVar.fogOfWar or enemy.visible)):
                canvas.create_line(ship.xPos, ship.yPos,   ship.xPos+(ship.xDir*200),
                                   ship.yPos+(ship.yDir*200), fill="black")

    ship.xPos += ship.xDir*ship.speed/360*globalVar.gameSpeed
    ship.yPos += ship.yDir*ship.speed/360*globalVar.gameSpeed


def drawShip(ship):  # draw ship on the map with all of its accesories
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


# main
root.bind('<Motion>', motion)
root.bind('<Button-1>', mouseButton1)

root.title("USS Artemis")
globalVar = global_var()

player = ship(outlineColor="white", owner="player1")
enemy = ship(xPos=43, outlineColor="red", owner="ai1")


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

ammunitionChoice = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Number of shots", to=len(player.typesOfAmmunition), relief=RIDGE)

accuracyChoice = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Time to aim", to=4, relief=RIDGE)

gameSpeedScale = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Playback speed", from_=1, to=16, resolution=-20, variable=2, relief=RIDGE)

typeOfRounds = tk.Button()
pixel = tk.PhotoImage(width=1, height=1)
img = tk.PhotoImage(file=r'resized_image.png')
gameSpeedScale.set(3)

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
gameSpeedScale.place(x=globalVar.canvasX, y=globalVar.canvasY - 80)
canvas.place(x=globalVar.canvasX, y=globalVar.canvasY)
"""
label1.grid(row=4, column=0, rowspan=2)
"""
# clock
update()


root.mainloop()
