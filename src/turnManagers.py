import tkinter as tk
import tkinter.ttk as ttk
from ctypes import pointer
from dis import dis
from ensurepip import bootstrap
from faulthandler import disable
from functools import partial
from tkinter.filedialog import askopenfilename
from src.update import update


def pauseGame(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root):
    if(var.paused):
        var.paused = False
        root.after(1, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root))
    else:
        var.paused = True

def startTurn(uiElements,var,ships,gameRules,uiMetrics):
    if(not var.turnInProgress):
        if(var.debugging):
            print("New Round")
        var.turnInProgress = True
        uiElements.timeElapsedProgressBar['value'] = 0
        for object in uiElements.UIElementsList:
            object.config(state=tk.DISABLED, background="#D0D0D0")
        for object in uiElements.RadioElementsList:
            object.config(state=tk.DISABLED)
        for object in uiElements.uiSystems:
            object.config(state = tk.DISABLED, background="#D0D0D0")
        for object in var.uiSystemsAS:
            object.config(state = tk.DISABLED, style = 'Disabled.TCheckbutton')
