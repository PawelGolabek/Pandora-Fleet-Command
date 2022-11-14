import configparser
import os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from functools import partial

from battleSystem import run
from missionSelectMenu import missionSelectScreen
from myStyles import *
from naglowek import declareGlobals
from rootCommands import hideMenuUi,showMenuUi

def resumeCommand():
    x=10


if __name__ == '__main__':
    declareGlobals()
    parameter1 = "1.Exiled-To-Make-A-Stand"
    root = tk.Tk()
    _style = ttk.Style()
    loadStyles(root,_style)
    rootX = 1600
    rootY = 1000
    """
    rootX = root.winfo_screenwidth()
    rootY = root.winfo_screenheight()
    root.attributes('-fullscreen', True)
    """
    UIScale = 1
    root.geometry(str(rootX*UIScale) + "x" + str(rootY*UIScale)+"+0+0")
    
    config = configparser.ConfigParser()
    cwd = os.getcwd()
    filePath = os.path.join(cwd, "maps",parameter1,"level info.ini")
    config.read(filePath)
    
    uiMenuElements = []

    resumeButtonCommand =  partial(run,config,root,uiMenuElements)
    resumeButton = tk.Button(text = "Resume", command = resumeButtonCommand)
    quickBattleCommand1 =  partial(run,config,root,uiMenuElements)
    quickBattleButton = tk.Button(text = "Quick battle", command = quickBattleCommand1)
    missionSelect1 =  partial(missionSelectScreen,root,config,uiMenuElements)
    hideUiCommand = partial(hideMenuUi,uiMenuElements)
    missionSelectButton = tk.Button(text = "Mission select", command = lambda:[hideUiCommand(),missionSelect1()])
    exitButton = tk.Button(text = "Exit", command = exit)

    uiMenuElements.append(resumeButton)
    uiMenuElements.append(quickBattleButton)
    uiMenuElements.append(missionSelectButton)
    uiMenuElements.append(exitButton)

    resumeButton.place(x=rootX/2-30,y = 200)
    quickBattleButton.place(x=rootX/2-30,y = 300)
    missionSelectButton.place(x=rootX/2-30,y = 400)
    exitButton.place(x=rootX/2-30,y = 500)

  #tmp
    # button 1
    btn1 = ttk.Button(root, text = 'Quit !', command = root.destroy, style = "Custom.TButton")
    btn1.place(x=100,y=200)
    
    # button 2
######

    root.mainloop()