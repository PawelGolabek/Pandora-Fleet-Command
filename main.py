import configparser
import os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from functools import partial

from battleSystem import run
from missionSelectMenu import missionSelectScreen
from myStyles import *
from naglowek import declareGlobals, dynamic_object, ui_metrics
from rootCommands import hideMenuUi, placeMenuUi
from shipEditorMenu import shipEditor
from systems import declareGlobalSystems
from subSystems import declareGlobalSubsystems
from engines import declareGlobalEngines
from thrusters import declareGlobalThrusters
from radars import declareGlobalRadars
from generators import declareGlobalGenerators

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
    parameter1 = "1.Exiled-To-Make-A-Stand"
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
    
    config = configparser.ConfigParser()
    cwd = os.getcwd()
    filePath = os.path.join(cwd, "maps",parameter1,"level info.ini")
    config.read(filePath)
    
    uiMenuElements = dynamic_object()
    uiMenuElementsList = []
    resumeButtonCommand = partial(run,config,root,uiMenuElements)
    quickBattleCommand1 = partial(run,config,root,uiMenuElements)
    shipEditorCommand = partial(shipEditor,root,config,uiMenuElements,uiMetrics,uiMenuElements)
    hideUiCommand = partial(hideMenuUi,uiMenuElementsList)
    missionSelect1 =  partial(missionSelectScreen,root,config,uiMenuElements)

    resumeButton = tk.Button(text = "Resume", command = resumeButtonCommand)
    quickBattleButton = tk.Button(text = "Quick battle", command = quickBattleCommand1)
    missionSelectButton = tk.Button(text = "Mission select", command = lambda:[hideUiCommand(),missionSelect1()])
    shipEditorButton = tk.Button(text = "Ships Editor", command = lambda:[hideUiCommand(),shipEditorCommand()])
    exitButton = tk.Button(text = "Exit", command = exit)

    uiMenuElements.resumeButton = resumeButton
    uiMenuElements.quickBattleButton = quickBattleButton
    uiMenuElements.missionSelectButton = missionSelectButton
    uiMenuElements.shipEditorButton = shipEditorButton
    uiMenuElements.exitButton = exitButton

    uiMenuElementsList.append(resumeButton)
    uiMenuElementsList.append(quickBattleButton)
    uiMenuElementsList.append(missionSelectButton)
    uiMenuElementsList.append(shipEditorButton)
    uiMenuElementsList.append(exitButton)


  #tmp
    """
    # button 1
    btn1 = ttk.Button(root, text = 'Quit !', command = root.destroy, style = "Custom.TButton")
    btn1.place(x=100,y=200)
    """
    placeMenuUi(uiMenuElements,uiMetrics)
    # button 2
######

    root.mainloop()