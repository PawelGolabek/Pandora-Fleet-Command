from dis import dis
from email.policy import default
from faulthandler import disable
from platform import system_alias
from tabnanny import check
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, Frame, BOTH
from random import randint
import PIL.Image
import tkinter.ttk as ttk
import sys,os

import maps

class global_var():
    def __init__(self,config,root):
        self.finished = False
        self.shipChoiceRadioButtons = []
        self.radio = IntVar(root, 999)
        self.radio2 = IntVar(root, 999)
        self.ammunitionOptionChoice = StringVar(root)
        self.tmpCounter = 0
        # START CONDITIONS
        self.radio.set(0)
        ## DYNAMIC UI ##
        self.uiSystems = []
        self.uiSystemsProgressbars = []
        ## INPUT HANDLING VARIABLES ##
        self.mouseOnUI = FALSE
        self.mouseWheelUp = FALSE
        self.mouseWheelDown = FALSE
        self.mouseButton1 = FALSE
        self.updateTimer = -1
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
        self.fogOfWar = True
        self.gameSpeed = 1
        self.turnLength = 1080
        self.zoom = 1
        self.shieldRegen = 1
        self.shieldMaxState = 1000
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
        self.radio0hidden = False
        self.radio1hidden = False
        self.radio2hidden = False
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
        self.image = PIL.Image.open(config.get("Images", "image"))
        self.imageMask = PIL.Image.open(config.get("Images", "imageMask"))
        pass


class ui_metrics():
    rootX = 1600
    rootY = 1000
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
    systemScalesLabelFrameWidth = systemScalesWidth+60
    systemProgressbarsHeightOffset = 60
    canvasX = systemScalesLabelFrameWidth + 20
    canvasY = 100
    shipDataX = canvasX
    shipDataY = canvasY + 20
    #editor
    editorSystemsFrameX = 100
    editorSystemsFrameY = 500
    editorSystemsX = 10
    editorSystemsY = 20
    editorSystemsYOffset = 50
    editorSystemsLOffsetX = 150
    editorSubsystemsXOffset = 400
    editorSystemsWidth = 350
    editorSaveButtonX = 1000
    editorSaveButtonY = 700
    editorChoiceMenuLFWidth = editorSystemsWidth
    editorChoiceMenuLFHeight = 80
    editorChoiceMenuOffset = 80
    editorChoiceMenuY = 150
    shipStatsLFHeight = 430
    shipStatsLFWidth = 350
    customRedShipX = 1000
    customBlueShipX = 200
    customBlueShipY = 600
    cgShipYoffset = 100
    cgStartButton = customBlueShipY + cgShipYoffset *2
    cgMapChoiceY = cgStartButton - cgShipYoffset *1.5
    

class game_rules():
    movementPenalityHard = 0.9
    movementPenalityMedium = 0.7

class dynamic_object():
    x=10

class landmark():
    def __init__(self, xPos=100, yPos=100, cooldown=800, defaultCooldown=800, radius=100, boost='none'):
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
        self.ttl = 0

class ghost_point():
    def __init__(self, xPos=300, yPos=300,number = 0): 
        self.xPos = xPos
        self.yPos = yPos
        self.number = number
        
def declareGlobals():
    global combatUiReady
    global missionSelectUiReady
    global editorUiReady
    global customGameUiReady
    global combatSystemInfo
    global customGameInfo
    global editorInfo
    global shipEditorInfo
    global mainInfo
    global gameMenuInfo
    global uiMetrics
    global allSystemsList
    global allSubsystemsList
    global allEnginesList
    global allRadarsList
    global allThrustersList
    global allGeneratorsList
    global systemStats 
    global engineStats 
    global thrustersStats
    global radarStats
    global generatorStats
    global subsystemStats
    global systemStatsBlueprints
    global subsystemStatsBlueprints
    global engineStatsBlueprints
    global thrustersStatsBlueprints
    global radarStatsBlueprints
    global generatorStatsBlueprints
    global systemLookup
    global mapOptions
    global campaignOptions
    combatSystemInfo = dynamic_object()
    shipEditorInfo = dynamic_object()
    editorInfo = dynamic_object()
    mainInfo = dynamic_object()
    gameMenuInfo = dynamic_object()
    uiMetrics = ui_metrics()
    systemStats = dynamic_object()
    systemStatsBlueprints = dynamic_object()
    engineStats = dynamic_object()
    thrustersStats = dynamic_object()
    radarStats = dynamic_object()
    generatorStats = dynamic_object()
    subsystemStats = dynamic_object()
    engineStatsBlueprints = dynamic_object()
    subsystemStatsBlueprints = dynamic_object()
    thrustersStatsBlueprints = dynamic_object()
    radarStatsBlueprints = dynamic_object()
    generatorStatsBlueprints = dynamic_object()
    systemLookup = dynamic_object()
    customGameInfo = dynamic_object()
    campaignOptions = dynamic_object()
    allSystemsList = []
    allSubsystemsList = []
    allEnginesList = []
    allRadarsList = []
    allThrustersList = []
    allGeneratorsList = []
    mapOptions = []
    combatUiReady = False
    editorUiReady = False
    missionSelectUiReady = False
    customGameUiReady = False