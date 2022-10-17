from dis import dis
from email.policy import default
from faulthandler import disable
from tabnanny import check
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, Frame, BOTH
from random import randint
import PIL.Image
import tkinter.ttk as ttk


def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

class global_var():
    def __init__(self,config,root):
        self.shipChoiceRadioButtons = []
        self.radio = IntVar(root, 999)
        self.radio2 = IntVar(root, 999)
        self.ammunitionOptionChoice = StringVar(root)
        self.tmpCounter = 0
        # START CONDITIONS
        self.radio.set(0)
        ## DYNAMIC UI ##
        self.uiSystemsLabelFrame = tk.LabelFrame(root,text= "" + " systems",borderwidth=2)
        self.uiEnergyLabel =  ttk.Label(self.uiSystemsLabelFrame, width=20, text = "Energy remaining: ", font = "16")
        self.uiSystems = []
        self.uiSystemsProgressbars = []
        ## INPUT HANDLING VARIABLES ##
        self.mouseOnUI = FALSE
        self.mouseWheelUp = FALSE
        self.mouseWheelDown = FALSE
        self.mouseButton1 = FALSE
        self.mouseButton2 = FALSE
        self.mouseButton3 = FALSE
        self.mouseButton3justPressed = FALSE
        self.mouseButton3released = FALSE
        self.prevPointerX = 0.0
        self.prevPointerY = 0.0
        self.pointerX = 0.0
        self.pointerX = 0.0
        self.pointerY = 0.0
        self.pointerDeltaX = 0.0
        self.pointerDeltaY = 0.0
        ## GAME OPTIONS ##
        self.fogOfWar = TRUE
        self.gameSpeed = 1
        self.turnLength = 1080
        self.zoom = 1
        self.shieldRegen = 1
        self.shieldMaxState = 400
        # GAME DATA
        self.choices = StringVar()
        self.options = []
        self.shipChoice = ''
        self.landmarks = []
        self.ships = []
        self.turnInProgress = FALSE
        self.misslesShot = 0
        self.currentMissles = []
        self.lasers = []
        # ZOOM
        self.mouseX = 0
        self.mouseY = 0
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.yellowX = 0
        self.yellowY = 0
        self.zoomChange = 0
        self.img = PhotoImage((config.get("Images", "img")))
        self.image = PIL.Image.open((config.get("Images", "image")))
        self.imageMask = PIL.Image.open(config.get("Images", "imageMask"))
        pass


class ui_metrics():   # change to % for responsible
    canvasWidth = 1120
    canvasHeight = 640
    shipImageFrameHeight = 60
    shipDataWidth = canvasWidth/6
    shipDataHeight = 40
    shipDataOffsetY = 20
    shipDataOffsetBetween = 60
    leftMargin = 10
    systemScalesWidth = 160
    systemScalesMarginTop = 80
    systemScalesHeightOffset = 90
    systemScalesLabelFrameWidth = 220 #systemScalesWidth + 60
    systemProgressbarsHeightOffset = 60
    canvasX = systemScalesLabelFrameWidth + 20
    canvasY = 100
    shipDataX = canvasX
    shipDataY = canvasY + 20

class ui_elements():
    x=1

class game_rules():
    movementPenalityHard = 0.9
    movementPenalityMedium = 0.7



class landmark():
    def __init__(self, xPos=100, yPos=100, cooldown=200, defaultCooldown=200, radius=100, boost='none'):
        self.xPos = xPos
        self.yPos = yPos
        self.cooldown = cooldown
        self.defaultCooldown = defaultCooldown
        self.radius = radius
        self.boost = boost
class tracer():
    def __init__(self, xPos=300, yPos=300, xDir=0.0, yDir=1.0, turnRate=0.5, speed=40): 
        self.xPos = xPos
        self.yPos = yPos
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.speed = speed
        self.moveOrderX = None
        self.moveOrderY = None

class ghostPoint():
    def __init__(self, xPos=300, yPos=300): 
        self.xPos = xPos
        self.yPos = yPos
