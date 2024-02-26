import configparser
import sys,os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from functools import partial
from pathlib import Path

from src.myStyles import loadStyles,ttk
from src.missionSelectMenu import missionSelectScreen
from src.loadGame import run,resume
from src.naglowek import declareGlobals, dynamic_object, ui_metrics
from src.rootCommands import hideMenuUi, placeMenuUi
from src.customGameMenu import customGame
from src.shipEditorMenu import shipEditor
from src.systems import declareGlobalSystems
from src.subSystems import declareGlobalSubsystems
from src.engines import declareGlobalEngines
from src.thrusters import declareGlobalThrusters
from src.radars import declareGlobalRadars
from src.generators import declareGlobalGenerators
from src.mapInfo import declareGlobalMaps

def resumeCommand():
    x=10

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
    root.geometry(str(uiMetrics.rootX) + "x" + str(uiMetrics.rootY)+"+0+0")
    root.title("Main Menu")
    
    config = configparser.ConfigParser()
    cwd = Path(sys.argv[0])
    cwd = str(cwd.parent)
    filePath = os.path.join(cwd, "campaignMissions"+ "\\" + parameter1 + "\\" +  "level info.ini")
    config.read(filePath)
    
    uiMenuElements = dynamic_object()
    uiMenuElementsList = []
    resumeButtonCommand = partial(resume,config,root,uiMenuElements)
    quickBattleCommand1 = partial(run,config,root,uiMenuElements)
    shipEditorCommand = partial(shipEditor,root,config,uiMenuElements,uiMetrics,uiMenuElements)
    hideUiCommand = partial(hideMenuUi,uiMenuElementsList)
    missionSelect1 =  partial(missionSelectScreen,root,config,uiMenuElements,uiMetrics)
    customGameCommand =  partial(customGame,root,config,uiMenuElements,uiMetrics)

    resumeButton =        tk.Button(text = "Resume", width = 17, height = 2,   font=('Optima',11), state = DISABLED, command = lambda:[resumeButtonCommand(),hideUiCommand()])
    quickBattleButton =   tk.Button(text = "Quick battle", width = 17, height = 2, font=('Optima',11),   command = lambda:[hideUiCommand(),quickBattleCommand1()])
    missionSelectButton = tk.Button(text = "Mission select", width = 17, height = 2, font=('Optima',11),   command = lambda:[hideUiCommand(),missionSelect1()])
    shipEditorButton =    tk.Button(text = "Ships Editor", width = 17, height = 2,  font=('Optima',11),  command = lambda:[hideUiCommand(),shipEditorCommand()])
    customGameButton =    tk.Button(text = "Custom Game", width = 17, height = 2,  font=('Optima',11),  command = lambda:[hideUiCommand(),customGameCommand()])
    exitButton =          tk.Button(text = "Exit", width = 17, height = 2,  font=('Optima',11),  command = exit)

    uiMenuElements.resumeButton = resumeButton
    uiMenuElements.quickBattleButton = quickBattleButton
    uiMenuElements.missionSelectButton = missionSelectButton
    uiMenuElements.shipEditorButton = shipEditorButton
    uiMenuElements.customGameButton = customGameButton
    uiMenuElements.exitButton = exitButton

    uiMenuElementsList.append(resumeButton)
    uiMenuElementsList.append(quickBattleButton)
    uiMenuElementsList.append(missionSelectButton)
    uiMenuElementsList.append(shipEditorButton)
    uiMenuElementsList.append(customGameButton)
    uiMenuElementsList.append(exitButton)

    placeMenuUi(root,uiMenuElements,uiMetrics)
    
    root.mainloop()