from functools import partial
from rootCommands import *
from tkinter import *
import os
import configparser
from functools import partial
from PIL import Image, ImageTk
import PIL.Image

from battleSystem import run

class tmpobject():  #class only to save images from this menu from beng trash collected
    x=10

def hideSelectScreenUi(uiElements):
    for uiElement in uiElements:
      uiElement.place_forget()

def optionCommand(variable,desLabelVar,objLabelVar,missionCanvas,msmVar):
    cwd = os.getcwd()
    a = str((variable.get()))
    des = configparser.ConfigParser()
    filePath = os.path.join(cwd, "maps",a,"map description.ini")
    des.read(filePath)
    updateText(desLabelVar,objLabelVar,des)
    updateMissionCanvas(missionCanvas,variable,msmVar)

def updateText(desLabelVar,objLabelVar,des):
    try:
        desLabelVar.set(des.get("Main", "descriptionLong"))
        objLabelVar.set(des.get("Main", "ObjectivesLong"))
    except:
        desLabelVar.set("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam quis orci bibendum, pellentesque nibh nec, consequat erat. Nam lorem sapien, euismod ut velit sed, venenatis consectetur justo. Donec purus ante, ullamcorper vel augue non, gravida tincidunt lorem. Sed at eros eget sapien molestie facilisis non quis lectus. Donec vel ante ut massa finibus elementum interdum in ligula. Sed mollis placerat cursus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")
        objLabelVar.set("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam quis orci bibendum, pellentesque nibh nec, consequat erat. Nam lorem sapien, euismod ut velit sed, venenatis consectetur justo. Donec purus ante, ullamcorper vel augue non, gravida tincidunt lorem. Sed at eros eget sapien molestie facilisis non quis lectus. Donec vel ante ut massa finibus elementum interdum in ligula. Sed mollis placerat cursus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")

def updateMissionCanvas(missionCanvas,variable,msmVar):
    missionCanvas.delete("all")
    cwd = os.getcwd()
    a = str((variable.get()))
    c = os.path.join(cwd, "maps",a,"mapMiniature.png")
    b = PIL.Image.open(c)
    b = b.resize((800, 500), PIL.Image.ANTIALIAS)
    msmVar.img = ImageTk.PhotoImage(b)
    missionCanvas.create_image(0,0,image=msmVar.img,anchor=NW)
    return msmVar.img

def missionSelectScreen(root,config):
    root.deiconify()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    OPTIONS = [
    "1.Exiled-To-Make-A-Stand",
    "2.Warcries-That-Shred-The-Clouds",
    "3.Destination-For-The-Homeworld-To-Regain"
    ]
    desLabelVar = StringVar(root)
    desLabelFrame = LabelFrame(width = 800,height = 300)
    desLabelVar.set("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    desLabel = Label(desLabelFrame,textvariable=desLabelVar,anchor='w',justify = LEFT,wraplength=500)
    desLabel.place(x=0,y=0)

    objLabelVar = StringVar(root)
    objLabelFrame = LabelFrame(width = 350,height = 700)
    objLabelVar.set("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    objLabel = Label(objLabelFrame,textvariable=objLabelVar,anchor='w',justify = LEFT,wraplength=330)
    objLabel.place(x=0,y=0)

    variable = StringVar(root)
    variable.set(OPTIONS[0])

    missionCanvas = Canvas(root,width = 800, height = 500)
   # """
    msmVar = tmpobject()
    cwd = os.getcwd()
    a = str((variable.get()))
    c = os.path.join(cwd, "maps",a,"mapMiniature.png")
    b = PIL.Image.open(c)
    img = ImageTk.PhotoImage(b)
    missionCanvas.create_image(0,0,anchor=NW,image=img)
    missionCanvas.config(bg="green")

    imageToAvoidTrashCollecting = updateMissionCanvas(missionCanvas,variable,msmVar)
    levelOptionMenu = OptionMenu(root, variable, *OPTIONS, command=lambda _: optionCommand(variable,desLabelVar,objLabelVar,missionCanvas,msmVar))
    optionCommand(variable,desLabelVar,objLabelVar,missionCanvas,msmVar)

    a = imageToAvoidTrashCollecting

    uiElements = []

    startButtonCommand = partial(start,variable,root)
    button = Button(root, text="Start", command= lambda: [hideSelectScreenUi(uiElements),startButtonCommand()])

    uiElements.append(button)
    uiElements.append(levelOptionMenu)
    uiElements.append(desLabel)
    uiElements.append(missionCanvas)
    uiElements.append(objLabelFrame)
    uiElements.append(objLabel)
    uiElements.append(desLabelFrame)
    uiElements.append(desLabel)

    levelOptionMenu.place(x=40,y=100)
    button.place(x=40,y=150)
    desLabelFrame.place(x=440,y=650)
    objLabelFrame.place(x=40,y=250)
    missionCanvas.place(x=440,y=100)

    mainloop()

def start(variable,root):
    config = configparser.ConfigParser()
    cwd = os.getcwd()
    filePath = os.path.join(cwd, "maps",variable.get(),"level info.ini")
    config.read(filePath)
    run(config,root)
