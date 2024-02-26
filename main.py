import configparser
import sys,os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from functools import partial
from pathlib import Path
import ctypes
import PIL.Image
from PIL import ImageTk


from src.myStyles import loadStyles,ttk
from src.missionSelectMenu import missionSelectScreen
from src.loadGame import run,resume
from src.settings import declareGlobals, dynamic_object, ui_metrics
from src.rootCommands import hideMenuUi, placeMenuUi
from src.customGameMenu import customGame
from src.shipEditorMenu import shipEditor
from src.editor.systems import declareGlobalSystems
from src.editor.subSystems import declareGlobalSubsystems
from src.editor.engines import declareGlobalEngines
from src.editor.thrusters import declareGlobalThrusters
from src.editor.radars import declareGlobalRadars
from src.editor.generators import declareGlobalGenerators
from src.mapInfo import declareGlobalMaps
from src.multiplayer.menu import multiplayerMenu

def resumeCommand():
    x=10


def rgb(r, g, b):
   return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0")
      for c in (r, g, b)])


if __name__ == '__main__':
    declareGlobals()
    declareGlobalSystems()
    declareGlobalSubsystems()
    declareGlobalEngines()
    declareGlobalThrusters()
    declareGlobalRadars()
    declareGlobalGenerators()
    declareGlobalMaps()
    parameter1 = "2.Warcries-That-Shred-The-Clouds"
    root = tk.Tk()
  #  root = ttk.Window(themename="cyborg")
    _style = ttk.Style()
    uiMetrics = ui_metrics()
    loadStyles(root,_style)
    #root.attributes('-alpha',0.5)
    """
    rootX = root.winfo_screenwidth()
    rootY = root.winfo_screenheight()
    root.attributes('-fullscreen', True)
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root.geometry(str(uiMetrics.rootX) + "x" + str(uiMetrics.rootY)+"+0+0")
    root.minsize(uiMetrics.rootX,uiMetrics.rootY)
    root.maxsize(uiMetrics.rootX, uiMetrics.rootY)
    root.title("Main Menu")
    root.resizable(False, False)
    # Define gradient
    # # gradient = Canvas(root, width=uiMetrics.rootX, height=str(uiMetrics.rootY))         # gradient doesn't work with labelframes. Not worth effort to change all
    # # gradient.place(x = 0, y= 0)
    #
    #   # Iterate through the color and fill the rectangle with colors(r,g,0)
    #   X = 0
    #   for y in range(0, uiMetrics.rootY):
    #     r = (int(255 - X/64)-230) if (int(255 - X/64)-230)>0 else 0
    #     g = r + 1 if r + 1 < 255 else 255
    #     gradient.create_rectangle(0, X * 2, str(uiMetrics.rootY)*2,  y * 2 + 2, fill=rgb(r, g, r), outline=rgb(r, g, r))
    #     X += 1
    #     print(X)
    # root.attributes('-alpha', 0.5)
    #root.wm_attributes("-transparentcolor", '#202020')
    config = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    filePath = os.path.join(cwd, "campaignMissions"+ "\\" + parameter1 + "\\" +  "level info.ini")
    config.read(filePath)
    root.resizable(False, False)
    
    uiMenuElements = dynamic_object()
    multiplayerOptions = dynamic_object()
    multiplayerOptions.multiplayerGame = False
    uiMenuElementsList = []
    resumeButtonCommand = partial(resume,config,root,uiMenuElements,multiplayerOptions)
    quickBattleCommand1 = partial(run,config,root,uiMenuElements, multiplayerOptions)
    shipEditorCommand = partial(shipEditor,root,config,uiMenuElements,uiMetrics,uiMenuElements)
    hideUiCommand = partial(hideMenuUi,uiMenuElementsList)
    missionSelect1 =  partial(missionSelectScreen,root,config,uiMenuElements,uiMetrics, multiplayerOptions)
    customGameCommand =  partial(customGame,root,config,uiMenuElements,uiMetrics,multiplayerOptions)
    multiplayerGameCommand =  partial(multiplayerMenu, root,config,uiMenuElements,uiMetrics, multiplayerOptions)

    image = PIL.Image.open('maps\\mainMenu.png')
    resizedImage = (image).resize((uiMetrics.rootX, uiMetrics.rootY))
    uiMenuElements.menuCanvas = tk.Canvas(width = uiMetrics.rootX, height = uiMetrics.rootY)
    img = ImageTk.PhotoImage(resizedImage)
    uiMenuElements.menuCanvas.imageID = uiMenuElements.menuCanvas.create_image(0, 0, image=img, anchor='nw')
    

    uiMenuElements.resumeButtonFrame = tk.Frame(root)
    uiMenuElements.quickBattleButtonFrame = tk.Frame(root)
    uiMenuElements.missionSelectButtonFrame = tk.Frame(root)
    uiMenuElements.shipEditorButtonFrame = tk.Frame(root)
    uiMenuElements.customGameButtonFrame = tk.Frame(root)
    uiMenuElements.exitButtonFrame = tk.Frame(root)
    uiMenuElements.multiplayerButtonFrame = tk.Frame(root)
    uiMenuElements.resumeButtonFrame.config( bg="#4582ec", width=2, height=2,padx=1)
    uiMenuElements.missionSelectButtonFrame.config( bg="#4582ec", width=2, height=2,padx=1)
    uiMenuElements.shipEditorButtonFrame.config( bg="#4582ec", width=2, height=2,padx=1)
    uiMenuElements.customGameButtonFrame.config( bg="#4582ec", width=2, height=2,padx=1)
    uiMenuElements.exitButtonFrame.config( bg="#4582ec", width=2, height=2,padx=1)
    uiMenuElements.multiplayerButtonFrame.config( bg="#4582ec", width=2, height=2,padx=1)

    resumeButton =        tk.Button(uiMenuElements.resumeButtonFrame, text = "Resume", width = 20, height = 2, state = DISABLED, command = lambda:[resumeButtonCommand(),hideUiCommand()])
    missionSelectButton = tk.Button(uiMenuElements.missionSelectButtonFrame, text = "Campaign", width = 20, height = 2,   command = lambda:[hideUiCommand(),missionSelect1()])
    shipEditorButton =    tk.Button(uiMenuElements.shipEditorButtonFrame, text = "Ships Editor", width = 20, height = 2,  command = lambda:[hideUiCommand(),shipEditorCommand()])
    customGameButton =    tk.Button(uiMenuElements.customGameButtonFrame, text = "Custom Game", width = 20, height = 2,  command = lambda:[hideUiCommand(),customGameCommand()])
    multiplayerButton =   tk.Button(uiMenuElements.multiplayerButtonFrame,text  = "LAN Multiplayer", width = 20, height = 2,  command = lambda:[hideUiCommand(),multiplayerGameCommand()])
    exitButton =          tk.Button(uiMenuElements.exitButtonFrame,text  = "Exit", width = 20, height = 2,  command = exit)
    resumeButton.config(background='#1c1c1c',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
    missionSelectButton.config(background='#1c1c1c',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
    shipEditorButton.config(background='#1c1c1c',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
    customGameButton.config(background='#1c1c1c',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
    multiplayerButton.config(background='#1c1c1c',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
    exitButton.config(background='#1c1c1c',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec")
    
    uiMenuElements.resumeButton = resumeButton
    uiMenuElements.missionSelectButton = missionSelectButton
    uiMenuElements.shipEditorButton = shipEditorButton
    uiMenuElements.customGameButton = customGameButton
    uiMenuElements.multiplayerButton = multiplayerButton
    uiMenuElements.exitButton = exitButton


    uiMenuElementsList.append(uiMenuElements.resumeButtonFrame)
    uiMenuElementsList.append(uiMenuElements.missionSelectButtonFrame)
    uiMenuElementsList.append(uiMenuElements.shipEditorButtonFrame)
    uiMenuElementsList.append(uiMenuElements.customGameButtonFrame)
    uiMenuElementsList.append(uiMenuElements.multiplayerButtonFrame)
    uiMenuElementsList.append(uiMenuElements.exitButtonFrame)
    uiMenuElementsList.append(uiMenuElements.menuCanvas)

    placeMenuUi(root,uiMenuElements,uiMetrics)
    
    root.mainloop()