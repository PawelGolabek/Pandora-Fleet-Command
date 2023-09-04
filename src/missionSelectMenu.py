from functools import partial
from tkinter import *
import sys,os
import configparser
from functools import partial
from PIL import Image, ImageTk
import PIL.Image
from pathlib import Path

from src.battleSystem import run
import src.naglowek as naglowek
from src.rootCommands import *


def hideSelectScreenUi(uiElements):
    for uiElement in uiElements:
      uiElement.place_forget()

def optionCommand(variable,desLabelVar,objLabelVar,missionCanvas,msmVar):
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
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
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    a = str((variable.get()))
    config1 = configparser.ConfigParser()
    filePath = os.path.join(cwd, "campaignMissions" + "\\" + a + "\\" +  "level info.ini")
    config1.read(filePath)
    a1 = config1.get("Images","map")
    miniaturePath = os.path.join(cwd, "maps" + "\\" + a1 + "\\" + "mapMiniature.png")
    b = PIL.Image.open(miniaturePath)
    b = b.resize((800, 500), PIL.Image.ANTIALIAS)
    msmVar.img = ImageTk.PhotoImage(b)
    missionCanvas.create_image(0,0,image=msmVar.img,anchor=NW)
    return msmVar.img

def missionSelectScreen(root,config,uiMenuElements):

    desLabelVar = StringVar(root)
    desLabelFrame = ttk.Labelframe(style = 'Grey.TLabelframe', width = 800,height = 300)
    desLabelVar.set("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    desLabel = ttk.Label(desLabelFrame,style = 'Grey.TLabel', textvariable=desLabelVar,anchor='w',justify = LEFT,wraplength=500)
    desLabel.place(x=0,y=0)

    objLabelVar = StringVar(root)
    objLabelFrame = ttk.Labelframe(style = 'Grey.TLabelframe', width = 350,height = 700)
    objLabelVar.set("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    objLabel = ttk.Label(objLabelFrame,style = 'Grey.TLabel', textvariable=objLabelVar,anchor='w',justify = LEFT,wraplength=330)
    objLabel.place(x=0,y=0)

    variable = StringVar(root)
    variable.set(naglowek.campaignOptions[0])

    missionCanvas = Canvas(root,width = 800, height = 500)
   # """
    msmVar = naglowek.dynamic_object()

    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    a = str((variable.get()))
    config1 = configparser.ConfigParser()
    filePath = os.path.join(cwd, "campaignMissions" + "\\" + a + "\\" + "level info.ini")
    config1.read(filePath)
    a1 = config1.get("Images","map")
    c = os.path.join(cwd, "maps" + "\\" + a1 + "\\" + "mapMiniature.png")
    b = PIL.Image.open(c)
    img = ImageTk.PhotoImage(b)
    missionCanvas.create_image(0,0,anchor=NW,image=img)
    missionCanvas.config(bg="green")
 
    imageToAvoidTrashCollecting = updateMissionCanvas(missionCanvas,variable,msmVar)
    levelOptionMenu = OptionMenu(root, variable, *naglowek.campaignOptions, command=lambda _: optionCommand(variable,desLabelVar,objLabelVar,missionCanvas,msmVar))
    optionCommand(variable,desLabelVar,objLabelVar,missionCanvas,msmVar)

    a = imageToAvoidTrashCollecting

    uiElements = []

    startButtonCommand = partial(start,variable,root,uiMenuElements)
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

def start(variable,root,uiMenuElements):
    config = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    a = str((variable.get()))
    filePath = os.path.join(cwd, "campaignMissions\\" + a + "\\level info.ini")
    config.read(filePath)
    run(config,root,uiMenuElements)
