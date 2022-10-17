from functools import partial
from rootCommands import *
from tkinter import *
import os
import configparser
from functools import partial

from battleSystem import run

def hideSelectScreenUi(uiElements):
    for uiElement in uiElements:
      uiElement.place_forget()

def missionSelectScreen(root,config):
    root.deiconify()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    OPTIONS = [
    "1.Exiled-To-Make-A-Stand",
    "2.Warcries-That-Shred-The-Clouds",
    "3.Destination-For-The-Homeworld-To-Regain"
    ]

    variable = StringVar(root)
    variable.set(OPTIONS[0])
    uiElements = []

    w = OptionMenu(root, variable, *OPTIONS)

    startButtonCommand = partial(start,variable,root)
    button = Button(root, text="Start", command= lambda: [hideSelectScreenUi(uiElements),startButtonCommand()])
    uiElements.append(button)
    uiElements.append(w)

    w.place(x=50,y=100)
    button.place(x=100,y=150)

    mainloop()

def start(variable,root):
    config = configparser.ConfigParser()
    cwd = os.getcwd()
    filePath = os.path.join(cwd, "maps",variable.get(),"level info.ini")
    config.read(filePath)
    run(config,root)
