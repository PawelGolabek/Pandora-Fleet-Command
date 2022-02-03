import os
import tkinter
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

#sciezkaPython = os.getcwd()


root = tkinter.Tk()

UIScale = 1

rootX = 1200
rootY = 800

root.geometry(str(rootX*UIScale) + "x" + str(rootY*UIScale))


class ship():
    def __init__(self):
        self.direction = [0, 0]
        self.xPos = 300
        self.yPos = 300
        self.health = {'section1': 100, 'section2': 100,
                       'section3': 100, 'section4': 100}
        self.typesOfAmmunition = {"type1:": 0,
                                  "type2": 0,
                                  "type3": 0,
                                  "type4": 0}
        self.detectionRange = 100
        self.moveOrder = [0, 0]
        self.speed = 100


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
    timeFrame = 0


def update():
    globalVar.timeFrame += 1
    canvas.delete('all')
    canvas.create_image(0, 0, image=img, anchor='nw')
    updateRectangle()
    updateShip(player)
    drawShip(player)
   # drawShip(enemy)
    root.after(10, update)
    globalVar.mouseButton1 = False


def deleteNextFrame():
    for thing in globalVar.toDeleteNextFrame:
        thing.destroy()


def updateRectangle():
    """
    b = (abs(math.sin(globalVar.a/100))) * 120
    canvas.create_oval(b+5, b+5, 205-b, 205-b, outline='white')
    canvas.create_oval(globalVar.a+5, globalVar.a+5, 205 -
                       globalVar.a, 205-globalVar.a, outline='green')
    canvas.create_text(100, 10, text=globalVar.a, font="arial 54")
    canvas.create_text(55, 55, font="arial 54", text=round(b))
    """

    if(globalVar.a > 99):
        globalVar.flag = False
    if(globalVar.a < 1):
        globalVar.flag = True

    if(globalVar.flag):
        globalVar.a += 1
    else:
        globalVar.a -= 1


def updateShip(ship):
    """
    canvas.create_text(1000, 200, text=tempX, font="arial 54")
    canvas.create_text(1000, 100, text=tempY, font="arial 54")
    canvas.create_line(ship.xPos, ship.yPos, ship.xPos+tempX*200,
                       ship.yPos+tempY*200,   fill='white')
                       """
    ship.xPos += ship.direction[0]*ship.speed/360
    ship.yPos += ship.direction[1]*ship.speed/360


def drawShip(ship):
    canvas.create_oval(ship.xPos-ship.detectionRange, ship.yPos - ship.detectionRange,
                       ship.xPos + ship.detectionRange, ship.yPos+ship.detectionRange, outline='white')
    canvas.create_line(ship.xPos-5, ship.yPos-5, ship.xPos +
                       5, ship.yPos+5,   fill='white')

    # movementOrder
    if(globalVar.mouseButton1 and globalVar.pointerX > 0 and globalVar.pointerX < (globalVar.canvasWidth) and globalVar.pointerY > 0 and globalVar.pointerY < (globalVar.canvasHeight)):
        ship.moveOrderX = globalVar.pointerX
        ship.moveOrderY = globalVar.pointerY
        """
    if(ship.direction > ship.orderDirection):  # do zmiany
        ship.direction -= 1
    if(ship.direction < ship.orderDirection):
        ship.direction += 1
        """

    if(ship.moveOrder[0] > 0):
        # direction testing
        moveDir = [ship.xPos - ship.moveOrderX, ship.yPos - ship.moveOrderY]

        # normalise the vector
        scale = math.sqrt(moveDir[0]*moveDir[0] + moveDir[1]*moveDir[1])

        moveDir = -[ship.xPos - ship.moveOrder[0],
                    ship.yPos - ship.moveOrder[1]] / scale  # ok

        if(globalVar.timeFrame % 2000):
            print(moveDir[0], " ", moveDir[1])

        canvas.create_line(ship.xPos, ship.yPos,
                           ship.xPos+moveDir[0]*100, ship.yPos+moveDir[1]*100,   fill='green')
        #canvas.create_text(155, 55, font="arial 54", text=ship.direction)
        canvas.create_text(155, 155, font="arial 54",
                           text=round(ship.orderDirection, 0))
        canvas.create_line(ship.xPos, ship.yPos, ship.moveOrder[0],
                           ship.moveOrder[1],   fill='white')

    # change for click


def motion(event):
    globalVar.pointerX = root.winfo_pointerx() - root.winfo_x() - \
        globalVar.canvasX-7
    globalVar.pointerY = root.winfo_pointery() - root.winfo_y() - \
        globalVar.canvasY - 31
   # print('{}, {}'.format(globalVar.pointerX, globalVar.pointerY))


def mouseButton1(event):
    if event:
        globalVar.mouseButton1 = True
    else:
        globalVar.mouseButton1 = False


root.bind('<Motion>', motion)
root.bind('<Button-1>', mouseButton1)

root.title("USS Artemis")
globalVar = global_var()
player = ship()
enemy = ship()


titleScreen1 = tkinter.LabelFrame(root, text="Ścieżka")  # not working
ammunitionChoice = tkinter.Scale(
    root, orient=HORIZONTAL, length=100, label="Number of shots to take", to=len(player.typesOfAmmunition))
typeOfRounds = tkinter.Button()
pixel = tkinter.PhotoImage(width=1, height=1)
labelFrame1 = tkinter.LabelFrame(root, width=10, text='Witaj')
label1 = tkinter.Label(
    labelFrame1, image=pixel, width=100, height=200, compound=tkinter.CENTER, text="Przykładowy tekst tskjldefgnbdke\njbngkjdfnbgkjsdrbntgkjdrk\ngjdf nbdfkj gbdfk\nj gbdkfjbn gkdf ")

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

canvas.imageList.append(img)
# item with background
# cosmetics


# grid

#root.columnconfigure(0, minsize=100, weight=0)

img = tkinter.PhotoImage(file=r'resized_image.png')
titleScreen1.place(x=0, y=10)
ammunitionChoice.place(x=20, y=20)
labelFrame1.place(x=10, y=10)
canvas.place(x=globalVar.canvasX, y=globalVar.canvasY)

"""
label1.grid(row=4, column=0, rowspan=2)
"""
# clock
update()


root.mainloop()
