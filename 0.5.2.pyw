import os
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, Frame, BOTH
from random import randint
import math
from typing import Collection

#sciezkaPython = os.getcwd()


root = tkinter.Tk()

UIScale = 1

rootX = 1200
rootY = 800

root.geometry(str(rootX*UIScale) + "x" + str(rootY*UIScale))


class ship():
    def __init__(self):
        self.xPos = 100
        self.yPos = 100
        self.health = {'section1': 100, 'section2': 100,
                       'section3': 100, 'section4': 100}
        self.typesOfAmmunition = {"type1:": 0,
                                  "type2": 0,
                                  "type3": 0,
                                  "type4": 0}
        self.detectionRange = 100


class playerController():
    a = 10


class aiController():
    a = 10


class main():
    a = 0
    flag = FALSE
    canvasX = 100
    canvasY = 100
    pointerX = 0
    pointerY = 0
    canvasLength = 800
    canvasHeight = 600


def update():
    canvas.delete('all')
    updateRectangle()
    updateShip(globalVar.a, globalVar.a)
    drawShip(player)
    drawShip(enemy)
    root.after(10, update)


def updateRectangle():
    b = (abs(math.sin(globalVar.a/100))) * 120
    canvas.create_rectangle(5, 5, 800, 800, fill='blue')
    canvas.create_oval(b+5, b+5, 205-b, 205-b, outline='white')
    canvas.create_oval(globalVar.a+5, globalVar.a+5, 205 -
                       globalVar.a, 205-globalVar.a, outline='green')
    canvas.create_text(100, 10, text=globalVar.a, font="arial 54")
    canvas.create_text(55, 55, font="arial 54", text=round(b))

    if(globalVar.a > 99):
        globalVar.flag = False
    if(globalVar.a < 1):
        globalVar.flag = True

    if(globalVar.flag):
        globalVar.a += 1
    else:
        globalVar.a -= 1


def updateShip(x, y):
    x = 0


def drawShip(ship):

    realY = 0
    realX = 0
    realX = globalVar.canvasX + ship.xPos
    realY = globalVar.canvasY + ship.yPos
    canvas.create_oval(realX-ship.detectionRange, realY - ship.detectionRange,
                       realX + ship.detectionRange, realY+ship.detectionRange, outline='white')

    canvas.create_line(realX-5, realY-5, realX + 5, realY+5,   fill='white')

    # movement
    canvas.create_line(realX, realY, globalVar.pointerX,
                       globalVar.pointerY,   fill='white')
    # change for click


def motion(event):
    globalVar.pointerX = root.winfo_pointerx() - root.winfo_x() - \
        globalVar.canvasX-7
    globalVar.pointerY = root.winfo_pointery() - root.winfo_y() - \
        globalVar.canvasY - 31
# NIE DZIALA
    if(globalVar.pointerX > globalVar.canvasX and globalVar.pointerX < (globalVar.canvasLength+globalVar.canvasX) and globalVar.pointerY > globalVar.canvasY and globalVar.pointerY < (globalVar.canvasHeight+globalVar.canvasY)):
        print('{}, {}'.format(globalVar.pointerX, globalVar.pointerY))


root.bind('<Motion>', motion)

root.title("USS Artemis")
globalVar = main()
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
x = canvas = Canvas(root, width=globalVar.canvasHeight,
                    height=globalVar.canvasHeight)


# cosmetics


# grid

#root.columnconfigure(0, minsize=100, weight=0)

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
