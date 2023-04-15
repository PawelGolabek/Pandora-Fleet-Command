import configparser
import os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from functools import partial

from battleSystem import run, resume
from missionSelectMenu import missionSelectScreen
from myStyles import *
from naglowek import declareGlobals, dynamic_object, ui_metrics
from rootCommands import hideMenuUi, placeMenuUi
from customGameMenu import customGame
from shipEditorMenu import shipEditor
from systems import declareGlobalSystems
from subSystems import declareGlobalSubsystems
from engines import declareGlobalEngines
from thrusters import declareGlobalThrusters
from radars import declareGlobalRadars
from generators import declareGlobalGenerators
from mapInfo import declareGlobalMaps

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
    _style = ttk.Style()
    uiMetrics = ui_metrics()
    loadStyles(root,_style)
    """
    rootX = root.winfo_screenwidth()
    rootY = root.winfo_screenheight()
    root.attributes('-fullscreen', True)
    """
    root.geometry(str(uiMetrics.rootX) + "x" + str(uiMetrics.rootY)+"+0+0")
    root.title("Main Menu")
    
    config = configparser.ConfigParser()
    cwd = os.getcwd()
    filePath = os.path.join(cwd, "campaignMissions",parameter1,"level info.ini")
    config.read(filePath)
    
    uiMenuElements = dynamic_object()
    uiMenuElementsList = []
    resumeButtonCommand = partial(resume,config,root,uiMenuElements)
    quickBattleCommand1 = partial(run,config,root,uiMenuElements)
    shipEditorCommand = partial(shipEditor,root,config,uiMenuElements,uiMetrics,uiMenuElements)
    hideUiCommand = partial(hideMenuUi,uiMenuElementsList)
    missionSelect1 =  partial(missionSelectScreen,root,config,uiMenuElements)
    customGameCommand =  partial(customGame,root,config,uiMenuElements,uiMetrics)

    resumeButton = tk.Button(text = "Resume", command = lambda:[resumeButtonCommand(),hideUiCommand()])
    quickBattleButton = tk.Button(text = "Quick battle", command = lambda:[hideUiCommand(),quickBattleCommand1()])
    missionSelectButton = tk.Button(text = "Mission select", command = lambda:[hideUiCommand(),missionSelect1()])
    shipEditorButton = tk.Button(text = "Ships Editor", command = lambda:[hideUiCommand(),shipEditorCommand()])
    customGameButton = tk.Button(text = "Custom Game", command = lambda:[hideUiCommand(),customGameCommand()])
    exitButton = tk.Button(text = "Exit", command = exit)

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

  #tmp
    """
    # button 1
    btn1 = ttk.Button(root, text = 'Quit !', command = root.destroy, style = "Custom.TButton")
    btn1.place(x=100,y=200)
    """
    placeMenuUi(root,uiMenuElements,uiMetrics)
    # button 2
######
    root.mainloop()