from functools import partial
from tkinter import *
import sys,os
import configparser
from functools import partial
from PIL import Image, ImageTk
import PIL.Image
from pathlib import Path
import tkinter.ttk as ttk
import tkinter as tk

from src.loadGame import run
import src.settings as settings
from src.rootCommands import placeMenuUi,hideMenuUi,placeSelectMenuUI


def destroySelectScreenUi(uiElements):
    for uiElement in uiElements:
      uiElement.destroy()

def optionCommand(variable,desLabelVar,objLabelVar,missionCanvas,msmVar,uiMetrics,dateLVar,unitLVar,codeLVar,threatVar,reconLVar,cryptonymLVar):
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    a = str((variable.get()))
    des = configparser.ConfigParser()
    filePath = os.path.join(cwd, "campaignMissions",a,"map description.ini")
    des.read(filePath)
    updateText(desLabelVar,objLabelVar,des,dateLVar,unitLVar,codeLVar,threatVar,reconLVar,cryptonymLVar)
    updateMissionCanvas(missionCanvas,variable,msmVar,uiMetrics)

def updateText(desLabelVar,objLabelVar,des,dateLVar,unitLVar,codeLVar,threatVar,reconLVar,cryptonymLVar):
 #   try:
    desLabelVar.set(des.get("main", "descriptionLong"))
    dateLVar.set(des.get("main", "date"))
    cryptonymLVar.set(des.get("main", "cryptonym"))
    unitLVar.set(des.get("main", "unit"))
    reconLVar.set(des.get("main", "recon"))
    codeLVar.set(des.get("main", "code"))
    threatVar.set(des.get("main", "threat"))
    objLabelVar.set(des.get("main", "ObjectivesLong"))
  #  except:
  #      desLabelVar.set("Lorem ipsum ")
  #      objLabelVar.set("Lorem ipsum ")

def updateMissionCanvas(missionCanvas,variable,msmVar,uiMetrics):
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
    b = b.resize((uiMetrics.msCanvasWidth, uiMetrics.msCanvasHeight), )
    msmVar.img = ImageTk.PhotoImage(b)
    missionCanvas.create_image(0,0,image=msmVar.img,anchor=NW)
    return msmVar.img

def missionSelectScreen(root,config,uiMenuElements,uiMetrics, multiplayerOptions):
    
    uiElements = settings.dynamic_object()
    desLabelVar = StringVar(root)

    uiElements.desLabelFrame = ttk.Labelframe(style = 'GreyBig.TLabelframe', width = 800,height = 350, text = 'Mission Briefing')
    desLabelVar.set("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    uiElements.desLabel = ttk.Label(uiElements.desLabelFrame,style = 'GreyBig.TLabel', textvariable=desLabelVar,anchor='w',justify = LEFT,wraplength=790)
    uiElements.desLabel.place(x=5,y=0)

    cryptonymLVar = StringVar(root)
    uiElements.cryptonymLF = ttk.Labelframe(style = 'GreyBig.TLabelframe', width = 350, height = 70, text = 'Cryptonym')
    cryptonymLVar.set("")
    uiElements.cryptonymL = ttk.Label(uiElements.cryptonymLF,style = 'GreyBig.TLabel', textvariable=cryptonymLVar,anchor='w',justify = LEFT,wraplength=330)
    uiElements.cryptonymL.place(x=5,y=0)

    dateLVar = StringVar(root)
    uiElements.dateLF = ttk.Labelframe(style = 'GreyBig.TLabelframe', width = 350, height = 70, text = 'Date')
    dateLVar.set("")
    uiElements.dateL = ttk.Label(uiElements.dateLF,style = 'GreyBig.TLabel', textvariable=dateLVar,anchor='w',justify = LEFT,wraplength=330)
    uiElements.dateL.place(x=5,y=0)

    unitLVar = StringVar(root)
    uiElements.unitLF = ttk.Labelframe(style = 'GreyBig.TLabelframe', width = 350, height = 140, text = 'Unit')
    unitLVar.set("")
    uiElements.unitL = ttk.Label(uiElements.unitLF,style = 'GreyBig.TLabel', textvariable=unitLVar,anchor='w',justify = LEFT,wraplength=330)
    uiElements.unitL.place(x=5,y=0)

    reconLVar = StringVar(root)
    uiElements.reconLF = ttk.Labelframe(style = 'GreyBig.TLabelframe', width = 350, height = 70, text = 'Recon')
    reconLVar.set("")
    uiElements.reconL = ttk.Label(uiElements.reconLF,style = 'GreyBig.TLabel', textvariable=reconLVar,anchor='w',justify = LEFT,wraplength=330)
    uiElements.reconL.place(x=5,y=0)

    codeLVar = StringVar(root)
    uiElements.codeLF = ttk.Labelframe(style = 'GreyBig.TLabelframe', width = 350, height = 70, text = 'Code')
    codeLVar.set("")
    uiElements.codeL = ttk.Label(uiElements.codeLF,style = 'GreyBig.TLabel', textvariable=codeLVar,anchor='w',justify = LEFT,wraplength=330)
    uiElements.codeL.place(x=5,y=0)

    threatLVar = StringVar(root)
    uiElements.threatLF = ttk.Labelframe(style = 'GreyBig.TLabelframe', width = 350, height = 70, text = 'Threat Level')
    threatLVar.set("")
    uiElements.threatL = ttk.Label(uiElements.threatLF,style = 'GreyBig.TLabel', textvariable=threatLVar,anchor='w',justify = LEFT,wraplength=330)
    uiElements.threatL.place(x=5,y=0)

    objLabelVar = StringVar(root)
    uiElements.objLabelFrame = ttk.Labelframe(style = 'GreyBig.TLabelframe', width = 350, height = 210, text = 'Mission Objectives')
    objLabelVar.set("")
    uiElements.objLabel = ttk.Label(uiElements.objLabelFrame,style = 'GreyBig.TLabel', textvariable=objLabelVar,anchor='w',justify = LEFT,wraplength=330)
    uiElements.objLabel.place(x=5,y=0)

    variable = StringVar(root)
    variable.set(settings.campaignOptions[0])
    uiElementsList = []

    uiElements.missionCanvas = Canvas(root,width = uiMetrics.msCanvasWidth, height = uiMetrics.msCanvasHeight)
   # """
    msmVar = settings.dynamic_object()

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
    uiElements.missionCanvas.create_image(0,0,anchor=NW,image=img)
    uiElements.missionCanvas.config(bg="green")
 
    imageToAvoidTrashCollecting = updateMissionCanvas(uiElements.missionCanvas,variable,msmVar,uiMetrics)
    uiElements.levelOptionMenu = tk.OptionMenu(root, variable, *settings.campaignOptions, command=lambda _: optionCommand(variable,desLabelVar,objLabelVar,uiElements.missionCanvas,msmVar,uiMetrics,dateLVar,unitLVar,codeLVar,threatLVar,reconLVar,cryptonymLVar))
    variable.set(settings.campaignOptions[0])
    uiElements.levelOptionMenu.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
    optionCommand(variable,desLabelVar,objLabelVar,uiElements.missionCanvas,msmVar,uiMetrics,dateLVar,unitLVar,codeLVar,threatLVar,reconLVar,cryptonymLVar)

    a = imageToAvoidTrashCollecting

    uiElementsList = []
    startButtonCommand = partial(start,variable,root,uiMenuElements,uiElementsList, multiplayerOptions)

    uiElements.startBFrame = tk.Frame(root)
    uiElements.startBFrame.config( bg="#4582ec", width=2, height=2,padx=1)
    uiElements.exitToMenuBFrame = tk.Frame(root)
    uiElements.exitToMenuBFrame.config(bg="#4582ec", width=2, height=2,padx=1)
    
    uiElements.startB = tk.Button(uiElements.startBFrame, text="Start", width = 20, height = 3, command= lambda: [destroySelectScreenUi(uiElementsList),root.title("Loading level ..."),startButtonCommand()])        
    uiElements.exitToMenuButton = tk.Button(uiElements.exitToMenuBFrame, width = 20, height = 3, text="Exit to menu", command=lambda:[placeMenuUi(root,uiMenuElements,uiMetrics), hideMenuUi(uiElementsList)])
    
    uiElements.startB.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")         #### no workin
    uiElements.exitToMenuButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")

    uiElementsList.append(uiElements.dateLF)
    uiElementsList.append(uiElements.cryptonymLF)
    uiElementsList.append(uiElements.unitLF)
    uiElementsList.append(uiElements.reconLF)
    uiElementsList.append(uiElements.codeLF)
    uiElementsList.append(uiElements.threatLF)
    uiElementsList.append(uiElements.startB)
    uiElementsList.append(uiElements.levelOptionMenu)
    uiElementsList.append(uiElements.desLabel)
    uiElementsList.append(uiElements.missionCanvas)
    uiElementsList.append(uiElements.objLabelFrame)
    uiElementsList.append(uiElements.objLabel)
    uiElementsList.append(uiElements.desLabelFrame)
    uiElementsList.append(uiElements.desLabel)
    uiElementsList.append(uiElements.exitToMenuButton)

    uiElementsList.append(uiElements.startBFrame)
    uiElementsList.append(uiElements.exitToMenuBFrame)



    placeSelectMenuUI(uiElements,uiMetrics)
    mainloop()

def start(variable,root,uiMenuElements,uiElementsList, multiplayerOptions):
    for element in uiElementsList:
        element.destroy()
    config = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    a = str((variable.get()))
    filePath = os.path.join(cwd, "campaignMissions\\" + a + "\\level info.ini")
    config.read(filePath)
    run(config,root,uiMenuElements, multiplayerOptions)
