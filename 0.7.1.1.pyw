from ctypes import pointer
from dis import dis
from email.policy import default
from faulthandler import disable
from tabnanny import check
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, Frame, BOTH
from random import randint
import math
from PIL import Image, ImageTk
import PIL.Image
import tkinter.ttk as ttk
from functools import partial
from shipCombat import *

#   Artemis 2021
#   Project by Pawel Golabek
#
#   Used libraries (excluding build-in): Pillow, Pil

root = tk.Tk()
UIScale = 1

rootX = 1850
rootY = 1000
"""
rootX = root.winfo_screenwidth()
rootY = root.winfo_screenheight()
root.attributes('-fullscreen', True)
"""
root.geometry(str(rootX*UIScale) + "x" + str(rootY*UIScale)+"+0+0")

#s = ttk.Style()
#s.theme_use('xpnative')
##s.configure("red.Horizontal.TProgressbar", foreground='blue', background='red')


def rgbtohex(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

class global_var():
    shipChoiceRadioButtons = []
    radio = IntVar(root, 999)
    radio2 = IntVar(root, 999)
    ammunitionOptionChoice = StringVar(root)
    tmpCounter = 0
    # START CONDITIONS
    radio.set(0)
    ## DYNAMIC UI ##
    uiSystemsLabelFrame = tk.LabelFrame(root,text= "" + " systems",borderwidth=2)
    uiEnergyLabel =  ttk.Label(uiSystemsLabelFrame, width=20, text = "Energy remaining: ", font = "16")
    uiSystems = []
    uiSystemsProgressbars = []
    ## INPUT HANDLING VARIABLES ##
    mouseOnUI = FALSE
    mouseWheelUp = FALSE
    mouseWheelDown = FALSE
    mouseButton1 = FALSE
    mouseButton2 = FALSE
    mouseButton3 = FALSE
    mouseButton3justPressed = FALSE
    mouseButton3released = FALSE
    prevPointerX = 0.0
    prevPointerY = 0.0
    pointerX = 0.0
    pointerX = 0.0
    pointerY = 0.0
    pointerDeltaX = 0.0
    pointerDeltaY = 0.0
    ## GAME OPTIONS ##
    fogOfWar = TRUE
    gameSpeed = 1
    turnLength = 1080
    zoom = 1
    shieldRegen = 1
    shieldMaxState = 400
    # GAME DATA
    choices = StringVar()
    options = []
    shipChoice = ''
    landmarks = []
    ships = []
    turnInProgress = FALSE
    misslesShot = 0
    currentMissles = []
    lasers = []
    img = PhotoImage('1/map.png')
    image = PIL.Image.open('1/map.png')
    imageMask = PIL.Image.open('1/mapMask.png')
    # ZOOM
    mouseX = 0
    mouseY = 0
    left = 0
    right = 0
    top = 0
    bottom = 0
    yellowX = 0
    yellowY = 0
    zoomChange = 0

class ui_icons():
    armorIcon = PhotoImage(file="icons/armor.png")


class ui_metrics:   # change to % for responsible
    canvasWidth = 1300
    canvasHeight = 600
    shipImageFrameHeight = 60
    shipDataWidth = canvasWidth/6
    shipDataHeight = 40
    shipDataOffsetY = 20
    shipDataOffsetBetween = 60
    leftMargin = 10
    systemScalesWidth = 120
    systemScalesMarginTop = 80
    systemScalesHeightOffset = 90
    systemScalesWidth = systemScalesWidth + 40
    systemScalesLabelFrameWidth = systemScalesWidth + 60
    systemProgressbarsHeightOffset = 60
    canvasX = systemScalesLabelFrameWidth + 20
    canvasY = 100
    shipDataX = canvasX
    shipDataY = canvasY + 20

class ui_elements:
    x=1

class game_rules:
    movementPenalityHard = 0.9
    movementPenalityMedium = 0.5


class _events:
    playerDestroyed = False
    showedWin = False


class landmark():
    def __init__(self, xPos=100, yPos=100, cooldown=200, defaultCooldown=200, radius=100, boost='none'):
        self.xPos = xPos
        self.yPos = yPos
        self.cooldown = cooldown
        self.defaultCooldown = defaultCooldown
        self.radius = radius
        self.boost = boost

############################## AMUNITION #############################################


class ammunition():
    def __init__(self, name='', typeName='', sort = '', owner='', target='', xDir=0, yDir=0, turnRate=2, speed=100, \
         shotsPerTurn=5, damage=10, damageFalloffStart=200, damageFalloffStop=400, defaultAccuracy=90, ttl = 10000, color = (rgbtohex(20,255,255)), special=None):
        self.owner = owner
        self.target = target
        self.name = name
        self.typeName = typeName
        self.sort = sort
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.speed = speed
        self.shotsPerTurn = shotsPerTurn
        self.damage = damage
        self.damageFalloffStart = damageFalloffStart
        self.damageFalloffStop = damageFalloffStop
        self.defaultAccuracy = defaultAccuracy
        self.ttl = ttl
        self.color = color
        self.special = special


class ammunition_type:
    type1adefault = ammunition()
    type1adefault.name = 'type1a'
    type1adefault.typeName = 'type1a'
    type1adefault.shotsPerTurn = 8
    type1adefault.damage = 10
    type1adefault.turnRate = 6
    type1adefault.speed = 80
    type1adefault.color = rgbtohex(250,250,20)

    type2adefault = ammunition()
    type2adefault.name = 'type2a'
    type2adefault.typeName = 'type2a'
    type2adefault.damage = 20
    type2adefault.turnRate = 6
    type2adefault.speed = 100

    type3adefault = ammunition()
    type3adefault.name = 'type3a'
    type3adefault.typeName = 'type3a'
    type3adefault.damage = 300
    type3adefault.turnRate = 10
    type3adefault.speed = 50

    laser1adefault = ammunition()
    laser1adefault.name = 'laser1a'
    laser1adefault.typeName = 'laser1a'
    laser1adefault.sort = 'laser'
    laser1adefault.damage = 1
    laser1adefault.turnRate = 25
    laser1adefault.speed = 1000
    laser1adefault.ttl = 600
    laser1adefault.color = rgbtohex(250,250,20)

    highEnergyLaser1 = ammunition()
    highEnergyLaser1.name = 'highEnergyLaser1'
    highEnergyLaser1.typeName = 'highEnergyLaser1'
    highEnergyLaser1.sort = 'laser'
    highEnergyLaser1.damage = 40
    highEnergyLaser1.speed = 1000
    highEnergyLaser1.ttl = 800
    highEnergyLaser1.color = rgbtohex(200,20,125)

    kinetic1 = ammunition()
    kinetic1.name = 'kinetic1'
    kinetic1.typeName = 'kinetic1'
    kinetic1.sort = 'kinetic'
    kinetic1.damage = 1
    kinetic1.speed = 250
    kinetic1.turnRate = 90
    kinetic1.ttl = 800
    kinetic1.color = rgbtohex(50,40,35)

############################## SYSTEMS #############################################
class system(object):
    def __init__(self,name = "system",minEnergy=0,maxEnergy=5,energy=0, maxCooldown = 200, cooldown = 0):
        self.name = name
        self.minEnergy = minEnergy
        self.maxEnergy = maxEnergy
        self.energy = energy
        self.maxCooldown = maxCooldown
        self.cooldown = cooldown
    def trigger(self,ship):
        pass
    def activate(self,ship):
        pass

class throttleBrake1(system):
    def __init__ (self,name = "Throttle Brake I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 300, cooldown = 0):
        super(throttleBrake1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship):
        if(self.cooldown <= 0 and True):
            i=100
            while(ship.hp != ship.maxHp and i>0):
                ship.hp+=1
                i-=1
            self.cooldown=self.maxCooldown
    def activate(self,ship):
        value = ship.maxSpeed/4
        ship.speed = ship.maxSpeed - self.energy*value
        putTracer(ship)
        pass
    

class antiMissleSystem1(system):
    def __init__ (self,name = "Anti Missle System I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 300, cooldown = 0):
        super(antiMissleSystem1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship):
        if(self.cooldown <= 0 and True):
            i=100
            while(ship.hp != ship.maxHp and i>0):
                ship.hp+=1
                i-=1
            self.cooldown=self.maxCooldown

class antiMissleSystem2(system):
    def __init__ (self,name = "Anti Missle System II",minEnergy=0,maxEnergy=10,energy=0, maxCooldown = 200, cooldown = 0):
        super(antiMissleSystem2,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship):
        if(self.cooldown <= 0 and ship.hp != ship.maxHp):
            i=100
            while(ship.hp != ship.maxAp and i>0):
                ship.hp+=1
                i-=1
            self.cooldown=self.maxCooldown

class type1aCannon1(system):
    def __init__ (self,name = "Type1a Cannon I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 1000, cooldown = 0):
        super(type1aCannon1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship1):
        shoot(self,ship1,ammunition_type.type1adefault)

class type2aCannon1(system):
    def __init__ (self,name = "Type2a Cannon I",minEnergy=0,maxEnergy=6,energy=0, maxCooldown = 300, cooldown = 0):
        super(type2aCannon1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship1):
        shoot(self,ship1,ammunition_type.type2adefault)

class type3aCannon1(system):
    def __init__ (self,name = "Type3a Cannon I",minEnergy=0,maxEnergy=3,energy=0, maxCooldown = 1700, cooldown = 0):
        super(type3aCannon1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship1):
        shoot(self,ship1,ammunition_type.type3adefault)

class gattlingLaser1(system):
    def __init__ (self,name = "Gattling Laser I",minEnergy=0,maxEnergy=9,energy=0, maxCooldown = 60, cooldown = 0):
        super(gattlingLaser1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship1):
        shoot(self,ship1,ammunition_type.laser1adefault)

class gattlingLaser2(system):
    def __init__ (self,name = "Gattling Laser II",minEnergy=2,maxEnergy=8,energy=0, maxCooldown = 40, cooldown = 0):
        super(gattlingLaser2,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship1):
        shoot(self,ship1,ammunition_type.laser1adefault)

class highEnergyLaser1(system):
    def __init__ (self,name = "High Energy Laser I",minEnergy=4,maxEnergy=8,energy=0, maxCooldown = 800, cooldown = 0):
        super(highEnergyLaser1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship1):
        shoot(self,ship1,ammunition_type.highEnergyLaser1)

class kinetic1(system):
    def __init__ (self,name = "Kinetic cannon I",minEnergy=0,maxEnergy=7,energy=0, maxCooldown = 5, cooldown = 0):
        super(kinetic1,self).__init__(name,minEnergy,maxEnergy,energy, maxCooldown, cooldown)

    def trigger(self,ship1):
        shoot(self,ship1,ammunition_type.kinetic1)
        shoot(self,ship1,ammunition_type.kinetic1,100,1000) #?
        shoot(self,ship1,ammunition_type.kinetic1,-100,-100)
        shoot(self,ship1,ammunition_type.kinetic1,0,100)


system_lookup = {
    "throttleBrake1": throttleBrake1,
    "type1aCannon1": type1aCannon1,
    "type2aCannon1": type2aCannon1,
    "type3aCannon1": type3aCannon1,
    "antiMissleSystem1": antiMissleSystem1,
    "antiMissleSystem2": antiMissleSystem2,
    "gattlingLaser1": gattlingLaser1,
    "gattlingLaser2": gattlingLaser2,
    "highEnergyLaser1": highEnergyLaser1,
    "kinetic1": kinetic1,
    "system": system,
    }

# ammunition_lookup = dict
# ammunition_lookup = {'type1a': type1a,
#                    'type2a': type2a,
#                   'type3a': type3a,
#                  }


class ship():
    def __init__(self, name="USS Artemis", owner="ai2", target='MSS Artemis',
                 hp=200, maxHp=None, ap=200, maxAp=None, shields=3, xPos=300, yPos=300,energyLimit = 20,
                 typesOfAmmunition=[], ammunitionChoice=0, ammunitionNumberChoice=0, systemSlots = [],
                 detectionRange=200, xDir=0.0, yDir=1.0, turnRate=0.5, ghostPoints = [], speed=40, maxSpeed = 40,
                 outlineColor="red"):  # replace alreadyShot with some clever formula to
        # Init info                                             ## handle shots when more than one enemy in range
        self.name = name
        self.owner = owner
        self.target = target
        self.xPos = xPos
        self.yPos = yPos
        self.energyLimit = energyLimit
        self.tmpEnergyLimit = energyLimit
        self.energy = energyLimit
        self.typesOfAmmunition = typesOfAmmunition
        self.ammunitionChoice = ammunitionChoice
        self.ammunitionNumberChoice = ammunitionNumberChoice

        self.systemSlots = []
        for tmp in systemSlots:
            targetClass =  system_lookup[tmp]
            tmpSystem = targetClass()
            self.systemSlots.append(tmpSystem)

        self.detectionRange = detectionRange
        self.xDir = xDir
        self.yDir = yDir
        self.turnRate = turnRate
        self.ghostPoints = ghostPoints
        self.speed = speed
        self.maxSpeed = maxSpeed
        self.outlineColor = outlineColor
        self.hp = hp
        if(maxHp == None):
            self.maxHp = hp
        else:
            self.maxHp = maxHp
        self.ap = ap
        if(maxAp == None):
            self.maxAp = ap
        else:
            self.maxAp = maxAp
        self.shields = shields
        self.shieldsState = []
        self.alreadyShot = FALSE
        tmp = 0
        while(tmp < shields):
            self.shieldsState.append(globalVar.shieldMaxState)
            tmp += 1
        # Mid-round info
        self.shotsTaken = 0
        self.shotsNotTaken = 0
        self.visible = FALSE
        self.moveOrderX = xPos+0.01
        self.moveOrderY = yPos+0.01

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

class laser():
    def __init__(self, xPos=300, yPos=300, targetXPos=300, targetYPos=300, color = rgbtohex(22,22,22), ttl = 10): 
        self.xPos = xPos
        self.yPos = yPos
        self.targetXPos = targetXPos
        self.targetYPos = targetYPos
        self.color = color
        self.ttl = ttl

class playerController():
    a = 10

class aiController():
    def ammunitionChoice(ship):
        ship.ammunitionChoice = 0

    def accuracyChoiceScale(ship):  # virtual choice for AI Controller
        return 3

    def ammunitionChoiceScale(ship):  # virtual choice for AI Controller
        return 1
    a = 10

################################################ STARTUP ######################################


def getZoomMetrics():
    globalVar.mouseX = uiMetrics.canvasWidth/2
    globalVar.mouseY = uiMetrics.canvasHeight/2
    globalVar.left = 0
    globalVar.right = uiMetrics.canvasWidth
    globalVar.top = 0
    globalVar.bottom = uiMetrics.canvasHeight
    globalVar.yellowX = 0
    globalVar.yellowY = 0
    globalVar.zoomChange = False

################################################ SHIP #########################################




def putLaser(missle):
    target = ship_lookup[missle.target]
    currentLaser = laser()
    currentLaser.xPos = missle.xPos
    currentLaser.yPos = missle.yPos
    currentLaser.targetXPos = target.xPos
    currentLaser.targetYPos = target.yPos
    currentLaser.color = missle.color
    currentLaser.ttl = missle.ttl
    (globalVar.lasers).append(currentLaser)
    
def putTracer(ship): # rotate and move the chosen ship
    ship.ghostPoints = []
    currentTracer = tracer()
    currentTracer.xPos = ship.xPos
    currentTracer.yPos = ship.yPos
    currentTracer.xDir = ship.xDir
    currentTracer.yDir = ship.yDir
    currentTracer.turnRate = ship.turnRate
    currentTracer.speed = ship.speed
    currentTracer.moveOrderX = ship.moveOrderX
    currentTracer.moveOrderY = ship.moveOrderY
    currentTracer.ttl = globalVar.turnLength
    while(currentTracer.ttl>0):
        # check for terrain
        if(not 0 < currentTracer.xPos < ui_metrics.canvasWidth-5):
            currentTracer.ttl = 0
        if(not 0 < currentTracer.yPos < ui_metrics.canvasHeight-5):
            currentTracer.ttl = 0
        colors = globalVar.imageMask.getpixel((int(currentTracer.xPos), int(currentTracer.yPos)))
        colorWeight = (colors[0] + colors[1] + colors[2])
        # vector normalisation
        scale = math.sqrt((currentTracer.moveOrderX-currentTracer.xPos)*(currentTracer.moveOrderX-currentTracer.xPos) +
                            (currentTracer.moveOrderY-currentTracer.yPos)*(currentTracer.moveOrderY-currentTracer.yPos))
        # move order into normalised vector
        moveDirX = -(currentTracer.xPos-currentTracer.moveOrderX) / scale
        moveDirY = -(currentTracer.yPos-currentTracer.moveOrderY) / scale

        degree = currentTracer.turnRate
        rotateVector(degree, currentTracer, moveDirX, moveDirY)

        if(colorWeight < 600 and colorWeight > 200):
            movementPenality = gameRules.movementPenalityMedium
        elif(colorWeight < 200):
            movementPenality = gameRules.movementPenalityHard
        else:
            movementPenality = 0.000001  # change

        xVector = currentTracer.xDir*currentTracer.speed/360
        yVector = currentTracer.yDir*currentTracer.speed/360

        currentTracer.xPos += xVector - xVector * movementPenality
        currentTracer.yPos += yVector - yVector * movementPenality

        if(currentTracer.ttl % 40 == 0):
            createGhostPoint(ship, currentTracer.xPos, currentTracer.yPos)
        currentTracer.ttl -= 1
    del currentTracer

def createGhostPoint(ship, xPos, yPos):
    ghost = ghostPoint()
    ship.ghostPoints.append(ghost)
    setattr(ship.ghostPoints[-1],'xPos',xPos)
    setattr(ship.ghostPoints[-1],'yPos',yPos)


def drawGhostPoints():
    for ship in globalVar.ships:
        for ghost in ship.ghostPoints:
            drawX = (ghost.xPos - globalVar.left) * \
                globalVar.zoom
            drawY = (ghost.yPos - globalVar.top) * globalVar.zoom 
            canvas.create_line(drawX-1*globalVar.zoom, drawY, drawX, drawY, width=globalVar.zoom,  fill='orange')


def shoot(system,ship1,ammunitionType,offsetX=0,offsetY=0):    #newer than manageShots without strange interval system
        if(system.cooldown <= 0 and True):
            for ship2 in globalVar.ships:
                if(ship1.owner == 'player1' and ship2.owner == 'ai1'):
                    distance = math.sqrt(
                        abs(pow(ship1.xPos-ship2.xPos, 2)+pow(ship1.yPos-ship2.yPos, 2)))
                    if(ship2.visible == TRUE and distance < ship1.detectionRange):
                        createRocket(ship1, ship2,ammunitionType,offsetX,offsetY)
                        system.cooldown = system.maxCooldown
                        break
                    #     print(ship1.name + " fired " +
                    #           str(ship1.typesOfAmmunition[ship1.ammunitionChoice].name))

# replace alreadyShot with some clever formula t
def manageShots():
    # add amunition scale input                                 ## handle shots when more than one enemy in range
    for ship1 in globalVar.ships:
        ship1.alreadyShot = FALSE
        for ship2 in globalVar.ships:
            if(ship1.owner == 'player1' and ship2.owner == 'ai1'):
                if(ship1.ammunitionNumberChoice != 0):
                    shotInterval = globalVar.turnLength / \
                        ship1.typesOfAmmunition[ship1.ammunitionChoice].shotsPerTurn
                    # change accuracy to be assigned to ship
                    maxShotsNotTaken = ship1.accuracyChoice
                    distance = math.sqrt(
                        abs(pow(ship1.xPos-ship2.xPos, 2)+pow(ship1.yPos-ship2.yPos, 2)))
                    if(timeElapsedProgressBar['value'] % shotInterval == 0 and ship2.visible == TRUE and distance < ship1.detectionRange and not ship1.alreadyShot):
                        if(ship1.shotsNotTaken < maxShotsNotTaken):
                            ship1.shotsNotTaken += 1
                        else:
                            if(ship1.shotsTaken < ship1.ammunitionNumberChoice):
                                ship1.shotsTaken += 1
                                createRocket(ship1, ship2,ammunition_type(ship1.ammunitionChoice))
                                ship1.alreadyShot = TRUE
                           #     print(ship1.name + " fired " +
                           #           str(ship1.typesOfAmmunition[ship1.ammunitionChoice].name))
            elif(ship1.owner == 'ai1' and not ship2.owner == 'ai1'):
                if(aiController.ammunitionChoiceScale != 0):
                    shotInterval = globalVar.turnLength / \
                        ship1.typesOfAmmunition[ship1.ammunitionChoice].shotsPerTurn
                    maxShotsNotTaken = aiController.accuracyChoiceScale(ship1)
                    distance = math.sqrt(
                        abs(pow(ship1.xPos-ship2.xPos, 2)+pow(ship1.yPos-ship2.yPos, 2)))
                    if(timeElapsedProgressBar['value'] % shotInterval == 0 and ship2.visible == TRUE and distance < ship1.detectionRange and not ship1.alreadyShot):
                        if(ship1.shotsNotTaken < maxShotsNotTaken):
                            ship1.shotsNotTaken += 1
                        else:
                            if(ship1.shotsTaken < aiController.ammunitionChoiceScale(ship)):
                                ship1.shotsTaken += 1
                                createRocket(ship1, ship2,ammunition_type.type1adefault)
                                ship1.alreadyShot = TRUE
                             #   print(ship1.name + " fired " +
                            #          str(ship1.typesOfAmmunition[ship1.ammunitionChoice].name))
def manageSystemActivations(ships):
    for ship in ships:
        for system in ship.systemSlots:
            system.activate(ship)

def manageSystemTriggers(ships):
    for ship in ships:
        for system in ship.systemSlots:
            system.trigger(ship)
                # trigger is activated during round and activation is between
                                    
def getOrders(ship, forced=False):
    tracered = False
    if(ship.owner == "player1"):
        if(globalVar.mouseButton1 and mouseOnCanvas() and globalVar.shipChoice == ship.name):
            ship.moveOrderX = globalVar.left + \
                ((globalVar.pointerX-ui_metrics.canvasX)/globalVar.zoom)
            ship.moveOrderY = globalVar.top + \
                ((globalVar.pointerY-ui_metrics.canvasY)/globalVar.zoom)
            tracered = True
            putTracer(ship)
    if(not tracered and ship.owner == "player1" and forced ):
            putTracer(ship)
    elif(ship.owner == "ai1"):
        ship.moveOrderX = 400  # insert ai controller decision
        ship.moveOrderY = 400

def manageLandmarks(landmarks, ships):
    for landmark in landmarks:
        if(landmark.cooldown > 0):
            landmark.cooldown -= 1
        for ship in ships:
            dist = ((landmark.xPos - ship.xPos)*(landmark.xPos - ship.xPos) +
                    (landmark.yPos - ship.yPos)*(landmark.yPos - ship.yPos))
            if(dist < landmark.radius*landmark.radius and landmark.cooldown == 0):
                getBonus(ship, landmark.boost)
                landmark.cooldown = landmark.defaultCooldown


def getBonus(ship, boost):
    if(boost == 'health'):
        ship.hp += 50
    elif(boost == 'armor'):
        ship.ap += 50
        # add boosts


def killShips(ships,missles,events):
    for ship1 in ships:
        if(ship1.hp < 1):
            ships.remove(ship1)
            for missle in missles:
                if missle.target == ship1:
                    missles.remove(missle)
            noEnemies = TRUE

            for progressBar in ship1.shieldsLabel:
                progressBar['value'] = 0

            for ship in ships:
                if(not ship.owner == "player1"):
                    noEnemies = FALSE
            if noEnemies and not events.showedWin:
                window = tk.Toplevel()
                label = tk.Label(window, text='yes, you win')
                label.place(x=0, y=0)
                events.showedWin = True
            elif(ship1.owner == 'player1' and events.playerDestroyed == False):
                events.playerDestroyed = True
                window = tk.Toplevel()
                label = tk.Label(window, text='yes, you looose')
                label.place(x=0, y=0)


############################################## MISSLES ##############################################


def manageRockets(missles,shipLookup):    # manage mid-air munitions
    for missle in missles:
        if(missle.sort == 'laser'):
            putLaser(missle)
            dealDamage(shipLookup[missle.target], missle.damage,globalVar)
            missles.remove(missle)
            continue
        scale = math.sqrt((shipLookup[missle.target].xPos-missle.xPos) *
                          (shipLookup[missle.target].xPos-missle.xPos) +
                          (shipLookup[missle.target].yPos-missle.yPos) *
                          (shipLookup[missle.target].yPos-missle.yPos))
        if scale == 0:
            scale = 0.01
        # move order into normalised vector
        moveDirX = - (missle.xPos-shipLookup[missle.target].xPos) / scale
        moveDirY = - \
            (missle.yPos-shipLookup[missle.target].yPos) / scale
        degree = missle.turnRate
        rotateVector(degree, missle, moveDirX, moveDirY)
        missle.xPos += missle.xDir*missle.speed/360
        missle.yPos += missle.yDir*missle.speed/360
        if((abs(missle.xPos - shipLookup[missle.target].xPos) *
            abs(missle.xPos - shipLookup[missle.target].xPos) +
            abs(missle.xPos - shipLookup[missle.target].xPos) *
            abs(missle.xPos - shipLookup[missle.target].xPos) +
            abs(missle.yPos - shipLookup[missle.target].yPos) *
                abs(missle.yPos - shipLookup[missle.target].yPos)) < 25):
            dealDamage(shipLookup[missle.target], missle.damage,globalVar)
            missles.remove(missle)




def drawLasers():
    for laser in globalVar.lasers:
        if laser.ttl>0:
            drawX = (laser.xPos - globalVar.left) * \
                globalVar.zoom
            drawY = (laser.yPos - globalVar.top) * \
                globalVar.zoom
            drawX2 = (laser.targetXPos - globalVar.left) * \
                globalVar.zoom
            drawY2 = (laser.targetYPos - globalVar.top) * \
                globalVar.zoom
            canvas.create_line(drawX,drawY,drawX2,drawY2, fill = laser.color)# "yellow")
        else:
            (globalVar.lasers).remove(laser)

def createRocket(ship, target,_type,offsetX=0,offsetY=0):
    globalVar.misslesShot += 1
    missleClass = _type
    # copy standard for ammunition. To be transformed into constructor like in c++ if needed
    missle = ammunition()
    globalVar.currentMissles.append(missle)
    missleName = 'missle' + str(globalVar.misslesShot)
    setattr(globalVar.currentMissles[-1], 'name', missleName)
    setattr(globalVar.currentMissles[-1], 'typeName', missleClass)
    setattr(globalVar.currentMissles[-1], 'sort', missleClass.sort)
    setattr(globalVar.currentMissles[-1], 'damage', missleClass.damage)
    setattr(globalVar.currentMissles[-1], 'ttl', missleClass.ttl)
    setattr(globalVar.currentMissles[-1], 'color', missleClass.color)
    setattr(globalVar.currentMissles[-1], 'xPos', ship.xPos+offsetX)
    setattr(globalVar.currentMissles[-1], 'yPos', ship.yPos+offsetY)
    setattr(globalVar.currentMissles[-1], 'xDir', ship.xDir)
    setattr(globalVar.currentMissles[-1], 'yDir', ship.yDir)
    setattr(globalVar.currentMissles[-1], 'owner', ship.owner)
    setattr(globalVar.currentMissles[-1], 'speed',missleClass.speed)
    setattr(globalVar.currentMissles[-1], 'turnRate',
            missleClass.turnRate)
    setattr(globalVar.currentMissles[-1], 'target', target.name)

############################################ INPUTS #############################################

def motion(event):
    globalVar.pointerX = root.winfo_pointerx() - root.winfo_rootx()
    globalVar.pointerY = root.winfo_pointery() - root.winfo_rooty()


def mouseButton1(event):  # get left mouse button and set it in globalvar
    if event:
        globalVar.mouseButton1 = True
    else:
        globalVar.mouseButton1 = False


def mouseWheel(event):
    if event.delta > 0:
        globalVar.mouseWheelUp = True
        if(globalVar.zoom < 7 and mouseOnCanvas()):
            globalVar.zoom += 1
            globalVar.zoomChange = True
    else:
        if(globalVar.zoom > 1 and mouseOnCanvas()):
            globalVar.zoom -= 1
            globalVar.zoomChange = True
        globalVar.mouseWheelDown = True

def mouseButton3(event):
    if event:
        globalVar.mouseButton3 = True

def mouseButton3up(event):
    if event:
        globalVar.mouseButton3 = False


def trackMouse():
    globalVar.pointerDeltaX = globalVar.pointerX - globalVar.prevPointerX
    globalVar.pointerDeltaY = globalVar.pointerY - globalVar.prevPointerY
    print(str(globalVar.pointerDeltaX) + str(globalVar.pointerDeltaY))
    globalVar.prevPointerX = globalVar.pointerX
    globalVar.prevPointerY = globalVar.pointerY
    globalVar.prevPointerX = globalVar.pointerX
    globalVar.prevPointerY = globalVar.pointerY

##################################### IN-GAME EVENTS ################################################


def update(globalVar,uiElements,canvas):
    canvas.delete('all')
    updateScales(uiElements)
    updateEnergy(globalVar)
    globalVar.gameSpeed = gameSpeedScale.get()
    newWindow(uiMetrics)
    if(not globalVar.turnInProgress):
        manageSystemActivations(globalVar.ships)
        for ship in globalVar.ships:
            getOrders(ship)
    ticksToEndFrame = 0
    if(globalVar.turnInProgress):
        root.title("TURN IN PROGRESS")
        while(ticksToEndFrame < globalVar.gameSpeed):
            detectionCheck(globalVar.ships)
            updateShips(globalVar,uiMetrics,gameRules,ship_lookup,canvas)
            manageLandmarks(globalVar.landmarks,globalVar.ships)
            manageShots()   # check ship shot
            manageRockets(globalVar.currentMissles,ship_lookup)   # manage mid-air munitions
            manageSystemTriggers(globalVar.ships)
            updateCooldowns(globalVar.ships)
            for laser in globalVar.lasers:
                if globalVar.turnInProgress:
                    laser.ttl -= 1
            killShips(globalVar.ships,globalVar.currentMissles,events)
            ticksToEndFrame += 1
            timeElapsedProgressBar['value'] += 1
            if(timeElapsedProgressBar['value'] > globalVar.turnLength):
                endTurn()
                break
    else:
        root.title("Year 2155 Day 23 Turn 20")
    drawShips(canvas,globalVar)
    drawGhostPoints()
    drawLandmarks(globalVar,canvas,uiIcons)
    drawLasers()
    drawRockets(globalVar,ammunitionType,canvas)
    globalVar.mouseOnUI = False
    globalVar.mouseWheelUp = False
    globalVar.mouseWheelDown = False
    globalVar.mouseButton1 = False
    globalVar.mouseButton2 = False
    trackMouse()
    globalVar.zoomChange = False
    root.after(10, partial(update,globalVar,uiElements,canvas))


def newWindow(uiMetrics):
    if(not globalVar.mouseWheelUp and not globalVar.mouseWheelDown and globalVar.mouseButton3 and globalVar.zoom != 1):
        if(mouseOnCanvas()):
            im = PIL.Image.open('resized_image.png')
            globalVar.im = ImageTk.PhotoImage(im)

            if(globalVar.zoom == 1):
                globalVar.mouseX = (
                    (globalVar.pointerX + globalVar.pointerDeltaX- uiMetrics.canvasX) + globalVar.left)
                globalVar.mouseY = (
                    (globalVar.pointerY + globalVar.pointerDeltaY - uiMetrics.canvasY) + globalVar.top)
            else:
                globalVar.mouseX = (
                    (globalVar.pointerX + globalVar.pointerDeltaX - uiMetrics.canvasX)/(globalVar.zoom-1) + globalVar.left)
                globalVar.mouseY = (
                    (globalVar.pointerY + globalVar.pointerDeltaY - uiMetrics.canvasY) / (globalVar.zoom-1) + globalVar.top)

            globalVar.yellowX = (
                uiMetrics.canvasWidth/globalVar.zoom)/2
            globalVar.yellowY = (
                uiMetrics.canvasHeight/globalVar.zoom)/2

            if(globalVar.mouseX > uiMetrics.canvasWidth - globalVar.yellowX):  # bumpers on sides
                globalVar.mouseX = globalVar.right - globalVar.yellowX
            if(globalVar.mouseX < globalVar.yellowX):
                globalVar.mouseX = globalVar.left + globalVar.yellowX
            if(globalVar.mouseY > uiMetrics.canvasHeight - globalVar.yellowY):
                globalVar.mouseY = globalVar.bottom - globalVar.yellowY
            if(globalVar.mouseY < globalVar.yellowY):
                globalVar.mouseY = globalVar.top + globalVar.yellowY

            globalVar.left = globalVar.mouseX - globalVar.yellowX
            globalVar.right = globalVar.mouseX + globalVar.yellowX
            globalVar.top = globalVar.mouseY - globalVar.yellowY
            globalVar.bottom = globalVar.mouseY + globalVar.yellowY
            globalVar.mouseX = globalVar.right - globalVar.left
            globalVar.mouseY = globalVar.bottom - globalVar.top

            tmp = im.crop((globalVar.left, globalVar.top,
                            globalVar.right, globalVar.bottom))
            im = tmp
            im = im.resize(
                (uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

            globalVar.im = ImageTk.PhotoImage(im)

            canvas.create_image(0, 0, image=globalVar.im, anchor='nw')
    else:
        if((globalVar.mouseWheelUp or globalVar.mouseWheelDown) and mouseOnCanvas()):
            im = PIL.Image.open('resized_image.png')
            globalVar.im = ImageTk.PhotoImage(im)

            if(globalVar.mouseWheelUp and globalVar.zoomChange):
                if(globalVar.zoom == 1):
                    globalVar.mouseX = (
                        (globalVar.pointerX - uiMetrics.canvasX) + globalVar.left)
                    globalVar.mouseY = (
                        (globalVar.pointerY - uiMetrics.canvasY) + globalVar.top)
                else:
                    globalVar.mouseX = (
                        (globalVar.pointerX - uiMetrics.canvasX)/(globalVar.zoom-1) + globalVar.left)
                    globalVar.mouseY = (
                        (globalVar.pointerY - uiMetrics.canvasY) / (globalVar.zoom-1) + globalVar.top)

                globalVar.yellowX = (
                    uiMetrics.canvasWidth/globalVar.zoom)/2
                globalVar.yellowY = (
                    uiMetrics.canvasHeight/globalVar.zoom)/2

                if(globalVar.mouseX > uiMetrics.canvasWidth - globalVar.yellowX):  # bumpers on sides
                    globalVar.mouseX = globalVar.right - globalVar.yellowX
                if(globalVar.mouseX < globalVar.yellowX):
                    globalVar.mouseX = globalVar.left + globalVar.yellowX
                if(globalVar.mouseY > uiMetrics.canvasHeight - globalVar.yellowY):
                    globalVar.mouseY = globalVar.bottom - globalVar.yellowY
                if(globalVar.mouseY < globalVar.yellowY):
                    globalVar.mouseY = globalVar.top + globalVar.yellowY

                globalVar.left = globalVar.mouseX - globalVar.yellowX
                globalVar.right = globalVar.mouseX + globalVar.yellowX
                globalVar.top = globalVar.mouseY - globalVar.yellowY
                globalVar.bottom = globalVar.mouseY + globalVar.yellowY
                globalVar.mouseX = globalVar.right - globalVar.left
                globalVar.mouseY = globalVar.bottom - globalVar.top

            elif(globalVar.mouseWheelDown):
                globalVar.mouseX = uiMetrics.canvasWidth/2
                globalVar.mouseY = uiMetrics.canvasHeight/2
                globalVar.zoom = 1
                globalVar.left = 0
                globalVar.top = 0
                globalVar.right = uiMetrics.canvasWidth
                globalVar.bottom = uiMetrics.canvasHeight

            if(globalVar.zoom != 1):

                tmp = im.crop((globalVar.left, globalVar.top,
                               globalVar.right, globalVar.bottom))
                im = tmp
                im = im.resize(
                    (uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

                globalVar.im = ImageTk.PhotoImage(im)

            canvas.create_image(0, 0, image=globalVar.im, anchor='nw')

        else:
            canvas.create_image(0, 0, image=globalVar.im, anchor='nw')


def startTurn():
    print("New Round")
    globalVar.turnInProgress = TRUE
    timeElapsedProgressBar['value'] = 0
    aiController.ammunitionChoice(enemy)
    for ship1 in globalVar.ships:
        ship1.shotsNotTaken = 0
        ship1.shotsTaken = 0
    for object in UIElementsList:
        object.config(state=DISABLED, background="#D0D0D0")
    for object in RadioElementsList:
        object.config(state=DISABLED)
    for object in globalVar.uiSystems:
        object.config(state = DISABLED, background="#D0D0D0")


def endTurn():
    globalVar.turnInProgress = FALSE
    for object in UIElementsList:
        object.config(state=NORMAL, background="#F0F0F0")
    for object in RadioElementsList:
        object.config(state=NORMAL)
    for object in globalVar.uiSystems:
        object.config(state = NORMAL, background="#F0F0F0")
    for ship in globalVar.ships:
        ship.ghostPoints = []
        getOrders(ship,True)


def updateScales(uiElements):
    uiElements.playerAPProgressBar['value'] = player.ap
    uiElements.playerAPProgressBar2['value'] = player2.ap
    uiElements.playerAPProgressBar3['value'] = player3.ap
    enemyAPProgressBar['value'] = enemy.ap
    enemyAPProgressBar2['value'] = enemy2.ap
    enemyAPProgressBar3['value'] = enemy3.ap
    playerHPProgressBar['value'] = player.hp
    playerHPProgressBar2['value'] = player2.hp
    playerHPProgressBar3['value'] = player3.hp
    enemyHPProgressBar['value'] = enemy.hp
    enemyHPProgressBar2['value'] = enemy2.hp
    enemyHPProgressBar3['value'] = enemy3.hp

    for ship1 in globalVar.ships:
        updateShields(ship1)

    globalVar.tmpCounter += 1
    ammunitionNumber = ammunitionChoiceScale.get()
    shipChosen = ship_lookup[globalVar.shipChoice]

    timeElapsedProgressBar.config(maximum=globalVar.turnLength)

    i = 0 
    for system in globalVar.uiSystemsProgressbars:
        (shipChosen.systemSlots[i]).energy = (globalVar.uiSystems[i]).get()
        system1 = shipChosen.systemSlots[i]
        system['value'] = (system1.maxCooldown-system1.cooldown)
        i+=1

def updateCooldowns(ships):
    for ship in ships:
        for system in ship.systemSlots:
            #change if needed
            energyTicks = system.energy
            while( system.cooldown > 0 and energyTicks):
                system.cooldown -= 0.1
                energyTicks -=1

def updateEnergy(var):
    shipChosen = ship_lookup[var.shipChoice]
    tmpEnergy = shipChosen.tmpEnergyLimit
    for system in shipChosen.systemSlots:
        tmpEnergy -= system.energy
    shipChosen.energy = tmpEnergy
    if(tmpEnergy<0):
        (var.uiEnergyLabel).config(foreground = "red")
        for radio in var.shipChoiceRadioButtons:
            radio.configure(state=DISABLED)
            startTurnButton.config(state = DISABLED)

    else:
        (var.uiEnergyLabel).config(foreground = "black")
        for radio in var.shipChoiceRadioButtons:
            radio.configure(state = NORMAL)
            if(not var.turnInProgress):
                startTurnButton.config(state = NORMAL)
    (var.uiEnergyLabel).config(text = "Energy remaining: " + str(shipChosen.energy))
    

def updateShields(ship1):
    for tmp, progressBar in enumerate(ship1.shieldsLabel):
        if(globalVar.turnInProgress):
            tmpShieldRegen = globalVar.shieldRegen
            while(ship1.shieldsState[tmp] < globalVar.shieldMaxState and tmpShieldRegen > 0):
                ship1.shieldsState[tmp] += 1
                tmpShieldRegen -= 1
                if(ship1.shieldsState[tmp] == globalVar.shieldMaxState):
                    ship1.shields += 1
        progressBar['value'] = ship1.shieldsState[tmp] * 100 \
            / globalVar.shieldMaxState
########################################## MULTIPURPOSE #########################################


def radioBox():
    globalVar.selection = int((globalVar.radio).get())
    if(globalVar.selection == 0):
        globalVar.shipChoice = playerName
    if(globalVar.selection == 1):
        globalVar.shipChoice = playerName2
    if(globalVar.selection == 2):
        globalVar.shipChoice = playerName3
    shipChosen = ship_lookup[globalVar.shipChoice]
    ammunitionChoiceScale.config(
        to=(shipChosen.typesOfAmmunition[shipChosen.ammunitionChoice]).shotsPerTurn)
    ammunitionChoiceScale.set(shipChosen.ammunitionNumberChoice)
    updateUtilityChoice()


def updateUtilityChoice():
    shipChosen = ship_lookup[globalVar.shipChoice]
    for widget in (globalVar.uiSystemsLabelFrame).winfo_children():
        widget.destroy()
    (globalVar.uiSystemsLabelFrame).destroy()
    globalVar.uiSystems = []
    globalVar.uiSystemsProgressbars = []
    shipChosen = ship_lookup[globalVar.shipChoice]
    globalVar.uiSystemsLabelFrame = tk.LabelFrame(root,width=ui_metrics.systemScalesLabelFrameWidth, \
                                                    height = (ui_metrics.systemScalesMarginTop*1.5 + (ui_metrics.systemScalesHeightOffset)*len(shipChosen.systemSlots)), text= shipChosen.name + " systems", \
                                                    borderwidth=2, relief="groove")
    (globalVar.uiSystemsLabelFrame).place(x = uiMetrics.leftMargin, y = ui_metrics.canvasY)
    i=0
    globalVar.uiEnergyLabel = ttk.Label(globalVar.uiSystemsLabelFrame, width=20, text = "Energy remaining: " + str(shipChosen.energy), font = "16")
    globalVar.uiEnergyLabel.place(x = 10, y = 20)
    for system in shipChosen.systemSlots:
        scale = tk.Scale(globalVar.uiSystemsLabelFrame, orient=HORIZONTAL, length=ui_metrics.systemScalesWidth, \
                            label=system.name, from_ = system.minEnergy, to=system.maxEnergy, relief=RIDGE)
        scale.set(system.energy)
        if(globalVar.turnInProgress):
            scale.config(state = 'disabled', background="#D0D0D0")
        (globalVar.uiSystems).append(scale)
        progressBar = ttk.Progressbar(globalVar.uiSystemsLabelFrame, maximum=system.maxCooldown, length=(ui_metrics.systemScalesWidth), variable=(system.maxCooldown-system.cooldown))
        (globalVar.uiSystemsProgressbars).append(progressBar)
        scale.place(x=10,y=ui_metrics.systemScalesMarginTop+i*ui_metrics.systemScalesHeightOffset)
        progressBar.place(x=10,y=ui_metrics.systemScalesMarginTop+i*(ui_metrics.systemScalesHeightOffset)+ui_metrics.systemProgressbarsHeightOffset)
        i+=1

def mouseOnCanvas():
    if(globalVar.pointerX > ui_metrics.canvasX and globalVar.pointerX <
       (uiMetrics.canvasX + uiMetrics.canvasWidth) and globalVar.pointerY >
            ui_metrics.canvasY and globalVar.pointerY < (uiMetrics.canvasY + uiMetrics.canvasHeight)):
        return True
    else:
        return False


    # move direviton into normalised vector
    if(scale != 0):
        object.xDir = object.xDir / scale
        object.yDir = object.yDir / scale


######################################################### MAIN ####################################

# main
root.bind('<Motion>', motion)
root.bind('<Button-1>', mouseButton1)
root.bind('<Button-2>', mouseButton3)
root.bind('<ButtonRelease-2>', mouseButton3up)
root.bind('<MouseWheel>', mouseWheel)

root.title("MMS Artemis")
uiMetrics = ui_metrics()
globalVar = global_var()
gameRules = game_rules()
ammunitionType = ammunition_type()
uiIcons = ui_icons()
ship_lookup = dict

getZoomMetrics()

# Ships

playerName = 'MMS Artemis'
playerName2 = 'MMS Scout'
playerName3 = 'MMS Catalyst'

enemyName = 'RDD HellWitch'
enemyName2 = 'RDD Redglower'
enemyName3 = 'RDD Firebath'

player = ship(outlineColor="white", owner="player1", \
              name=playerName, shields=10, xPos=300, \
               typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.laser1adefault, ammunitionType.type3adefault],\
              systemSlots=["throttleBrake1","gattlingLaser1", "antiMissleSystem2", "highEnergyLaser1"], detectionRange=100, ammunitionChoice=0, turnRate = 0.3,maxSpeed = 50)
player2 = ship(outlineColor="white", owner="player1",
                name=playerName2, shields=5, xPos=40, typesOfAmmunition=[ammunitionType.type2adefault, ammunitionType.type2adefault, ammunitionType.type2adefault], \
                systemSlots=["type1aCannon1", "type2aCannon1", "type3aCannon1"],detectionRange=160, ammunitionChoice=1, turnRate = 0.3)
player3 = ship(outlineColor="white", owner="player1",
               systemSlots=["system", "antiMissleSystem1","gattlingLaser2", "antiMissleSystem2", "kinetic1"], name=playerName3, shields=3, xPos=350, \
                    typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type2adefault, ammunitionType.type3adefault], \
                    detectionRange=180, ammunitionChoice=1, turnRate = 0.3, maxSpeed = 50)

enemy = ship(xPos=500, yPos=300, outlineColor="red", shields=10, typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type2adefault, ammunitionType.type2adefault],
             owner="ai1", ammunitionChoice=0, name=enemyName,  turnRate = 0.3)
enemy2 = ship(xPos=550, yPos=300, outlineColor="red", shields=5,
              owner="ai1", ammunitionChoice=0, name=enemyName2, typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type2adefault, ammunitionType.type2adefault], turnRate = 0.3)
enemy3 = ship(xPos=450, yPos=300, outlineColor="red", shields=3, typesOfAmmunition=[ammunitionType.type1adefault, ammunitionType.type2adefault, ammunitionType.type3adefault],
              owner="ai1", ammunitionChoice=0, name=enemyName3, turnRate = 0.3, maxSpeed = 0, speed = 0)

(globalVar.ships).append(player)
(globalVar.ships).append(player2)
(globalVar.ships).append(player3)

(globalVar.ships).append(enemy)
(globalVar.ships).append(enemy2)
(globalVar.ships).append(enemy3)

events = _events()
uiElements = ui_elements()

ship_lookup = {
    playerName: player,
    enemyName: enemy,
    playerName2: player2,
    enemyName2: enemy2,
    playerName3: player3,
    enemyName3: enemy3}

land1 = landmark(200, 200, 200, 200, 50, 'armor')
(globalVar.landmarks).append(land1)

# canvas
img = PIL.Image.open('1/map.png')
img = img.resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight))
img.save('resized_image.png')


canvas = Canvas(root, width=uiMetrics.canvasWidth,
                height=uiMetrics.canvasHeight)

globalVar.img = PhotoImage("resized_image.png")
canvas.imageList = []
# item with background to avoid python bug people were mentioning about disappearing non-anchored images

globalVar.imageMask = PIL.Image.open("1/mapMask.png")
img = PIL.Image.open('1/map.png')
im = img.resize(
    (uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

globalVar.imageMask = globalVar.imageMask.resize(
    (uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

globalVar.im = ImageTk.PhotoImage(im)
canvas.imageList.append(im)
canvas.imageList.append(globalVar.img)

UIElementsList = []
RadioElementsList = []

ammunitionChoiceScale = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Number of shots", to=len(player.typesOfAmmunition), relief=RIDGE)

accuracyChoiceScale = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Time to aim", to=4, relief=RIDGE)
gameSpeedScale = tk.Scale(
    root, orient=HORIZONTAL, length=100, label="Playback speed", from_=1, to=16, resolution=-20, variable=2, relief=RIDGE)
pixel = tk.PhotoImage(width=1, height=1)
img = tk.PhotoImage(file=r'resized_image.png')
gameSpeedScale.set(3)
timeElapsedLabel = tk.Label(root, text="Time elapsed")
timeElapsedProgressBar = ttk.Progressbar(root, maximum=globalVar.turnLength, variable=1,  orient='horizontal',
                                         mode='determinate', length=ui_metrics.shipDataWidth)

startTurnButton = tk.Button(root, text="Start turn", command=startTurn, width = 20, height= 7)
exitButton = tk.Button(root, text="Exit", command=exit)

globalVar.shipChoice = player.name


# ships choice
var = IntVar()
shipChoiceRadioButton1 = ttk.Radiobutton(
    root, text='1. MMS Artemis', variable=globalVar.radio, value=0, command=radioBox)
shipChoiceRadioButton2 = ttk.Radiobutton(
    root, text='2. MMS Scout', variable=globalVar.radio, value=1, command=radioBox)
shipChoiceRadioButton3 = ttk.Radiobutton(
    root, text='3. MMS Catalyst', variable=globalVar.radio, value=2, command=radioBox)

radioBox()
updateUtilityChoice()
detectionCheck(globalVar.ships)
for ship1 in globalVar.ships:
    if(ship1.owner == "player1"):
        putTracer(ship1)

shipChosen = ship_lookup[globalVar.shipChoice]

globalVar.shipChoiceRadioButtons = []
(globalVar.shipChoiceRadioButtons).append(shipChoiceRadioButton1)
(globalVar.shipChoiceRadioButtons).append(shipChoiceRadioButton2)
(globalVar.shipChoiceRadioButtons).append(shipChoiceRadioButton3)
shipImage1 = PIL.Image.open('ship_modules/ship.png')
shipImage = shipImage1.resize(
    (math.floor(uiMetrics.canvasWidth/8), math.floor(uiMetrics.canvasHeight/8)), PIL.Image.ANTIALIAS)
canvas.imageList.append(shipImage)
playerImage = ImageTk.PhotoImage(shipImage)
playerDisplay = tk.Label(root, image=playerImage)

enemyImage = ImageTk.PhotoImage(shipImage)
enemyDisplay = tk.Label(root, image=enemyImage)

distanceLabelFrame = tk.LabelFrame(
    root, text='Distance between ships', width=1000, height=200)
distanceLabel = tk.Label(distanceLabelFrame, text='0000000')

# ship shields
playerSPLabelFrame = tk.LabelFrame(root, text= playerName + " Shields",
                                    borderwidth=2, relief="groove")
playerSPProgressBar = ttk.Progressbar(
    playerSPLabelFrame, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
playerSPLabelFrame2 = tk.LabelFrame(root, text= playerName2 + " Shields",
                                     borderwidth=2, relief="groove")
playerSPProgressBar2 = ttk.Progressbar(
    playerSPLabelFrame2, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
playerSPLabelFrame3 = tk.LabelFrame(root, text= playerName3 + " Shields",
                                     borderwidth=2, relief="groove")
playerSPProgressBar3 = ttk.Progressbar(
    playerSPLabelFrame3, maximum=player.hp, length=(ui_metrics.shipDataWidth-10), variable=100)
enemySPLabelFrame = tk.LabelFrame(root, text=enemyName + " Shields",
                                   borderwidth=2, relief="groove")
enemySPLabelFrame2 = tk.LabelFrame(root, text=enemyName2 + " Shields",
                                    borderwidth=2, relief="groove")
enemySPLabelFrame3 = tk.LabelFrame(root, text= enemyName3 + " Shields",
                                    borderwidth=2, relief="groove")
playerShields = []
playerShields2 = []
playerShields3 = []
enemyShields = []
enemyShields2 = []
enemyShields3 = []

x = player.shields
n = 0
while(n < x):
    playerShields.append(ttk.Progressbar(
        playerSPLabelFrame, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1
x = player2.shields
n = 0
while(n < x):
    playerShields2.append(ttk.Progressbar(
        playerSPLabelFrame2, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1
x = player3.shields
n = 0
while(n < x):
    playerShields3.append(ttk.Progressbar(
        playerSPLabelFrame3, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1

x = enemy.shields
n = 0
while(n < x):
    enemyShields.append(ttk.Progressbar(
        enemySPLabelFrame, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1
x = enemy2.shields
n = 0
while(n < x):
    enemyShields2.append(ttk.Progressbar(
        enemySPLabelFrame2, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1
x = enemy3.shields
n = 0
while(n < x):
    enemyShields3.append(ttk.Progressbar(
        enemySPLabelFrame3, maximum=100, length=math.floor((ui_metrics.shipDataWidth-10)/x * 4/5), variable=100))
    n += 1

# ship armor
playerAPLabelFrame = tk.LabelFrame(root, text=playerName + " Armor",
                                    borderwidth=2, relief="groove")
uiElements.playerAPProgressBar = ttk.Progressbar(
    playerAPLabelFrame, maximum=player.maxAp, length=(ui_metrics.shipDataWidth-10), variable=100)
playerAPLabelFrame2 = tk.LabelFrame(root, text=playerName2 + " Armor",
                                     borderwidth=2, relief="groove")
uiElements.playerAPProgressBar2 = ttk.Progressbar(
    playerAPLabelFrame2, maximum=player2.maxAp, length=(ui_metrics.shipDataWidth-10), variable=100)
playerAPLabelFrame3 = tk.LabelFrame(root, text=playerName3 + " Armor",
                                     borderwidth=2, relief="groove")
uiElements.playerAPProgressBar3 = ttk.Progressbar(
    playerAPLabelFrame3, maximum=player3.maxAp, length=(ui_metrics.shipDataWidth-10), variable=100)
enemyAPLabelFrame = tk.LabelFrame(root, text=enemyName + " Armor",
                                   borderwidth=2, relief="groove")
enemyAPProgressBar = ttk.Progressbar(
    enemyAPLabelFrame, maximum=enemy.maxAp, length=(ui_metrics.shipDataWidth-10), variable=100)
enemyAPLabelFrame2 = tk.LabelFrame(root, text= enemyName2 + " Armor",
                                    borderwidth=2, relief="groove")
enemyAPProgressBar2 = ttk.Progressbar(
    enemyAPLabelFrame2, maximum=enemy.maxAp, length=(ui_metrics.shipDataWidth-10), variable=100)

enemyAPLabelFrame3 = tk.LabelFrame(root, text=enemyName3 + " Armor",
                                    borderwidth=2, relief="groove")
enemyAPProgressBar3 = ttk.Progressbar(
    enemyAPLabelFrame3, maximum=enemy.maxAp, length=(ui_metrics.shipDataWidth-10), variable=100)

# ship hp
playerHPLabelFrame = tk.LabelFrame(root, text= playerName + " HP",
                                    borderwidth=2, relief="groove")
playerHPProgressBar = ttk.Progressbar(
    playerHPLabelFrame, maximum=player.maxHp, length=(ui_metrics.shipDataWidth-10), variable=100)
playerHPLabelFrame2 = tk.LabelFrame(root, text= playerName2 + " HP",
                                     borderwidth=2, relief="groove")
playerHPProgressBar2 = ttk.Progressbar(
    playerHPLabelFrame2, maximum=player2.maxHp, length=(ui_metrics.shipDataWidth-10), variable=100)

playerHPLabelFrame3 = tk.LabelFrame(root, text=playerName3 + " HP",
                                     borderwidth=2, relief="groove")
playerHPProgressBar3 = ttk.Progressbar(
    playerHPLabelFrame3, maximum=player3.maxHp, length=(ui_metrics.shipDataWidth-10), variable=100)

enemyHPLabelFrame = tk.LabelFrame(root, text=enemyName + " HP",
                                   borderwidth=2, relief="groove")
enemyHPProgressBar = ttk.Progressbar(
    enemyHPLabelFrame, maximum=enemy.maxHp, length=(ui_metrics.shipDataWidth-10), variable=100)
enemyHPLabelFrame2 = tk.LabelFrame(root, text= enemyName2 + " HP",
                                    borderwidth=2, relief="groove")
enemyHPProgressBar2 = ttk.Progressbar(
    enemyHPLabelFrame2, maximum=enemy2.maxHp, length=(ui_metrics.shipDataWidth-10), variable=100)
enemyHPLabelFrame3 = tk.LabelFrame(root, text= enemyName3 +" HP",
                                    borderwidth=2, relief="groove")
enemyHPProgressBar3 = ttk.Progressbar(
    enemyHPLabelFrame3, maximum=enemy3.maxHp, length=(ui_metrics.shipDataWidth-10), variable=100)

######################################################### PROGRESSBAR ASSIGNMENT ####################################

player.shieldsLabel = playerShields
player2.shieldsLabel = playerShields2
player3.shieldsLabel = playerShields3
enemy.shieldsLabel = enemyShields
enemy2.shieldsLabel = enemyShields2
enemy3.shieldsLabel = enemyShields3

tmpShieldsLabel = []
tmpShieldsLabel.append(playerShields)
tmpShieldsLabel.append(playerShields2)
tmpShieldsLabel.append(playerShields3)
tmpShieldsLabel.append(enemyShields)
tmpShieldsLabel.append(enemyShields2)
tmpShieldsLabel.append(enemyShields3)
######################################################### PLACE ####################################
# left section
#ammunitionChoiceScale.place(x=20, y=ui_metrics.canvasY+60)     ## delete later 
#accuracyChoiceScale.place(x=20, y=ui_metrics.canvasY+140)     ## delete later 
# upper section
shipChoiceRadioButton1.place(
    x=ui_metrics.canvasX + 540, y=ui_metrics.canvasY - 60)
shipChoiceRadioButton2.place(
    x=ui_metrics.canvasX + 700, y=ui_metrics.canvasY - 60)
shipChoiceRadioButton3.place(
    x=ui_metrics.canvasX + 860, y=ui_metrics.canvasY - 60)

gameSpeedScale.place(x=ui_metrics.canvasX, y=ui_metrics.canvasY - 80)
canvas.place(x=ui_metrics.canvasX, y=ui_metrics.canvasY)
timeElapsedProgressBar.place(
    x=ui_metrics.canvasX+120, y=ui_metrics.canvasY - 60)
timeElapsedLabel.place(x=ui_metrics.canvasX+140, y=ui_metrics.canvasY - 80)
gameSpeedScale.place(x=ui_metrics.canvasX, y=ui_metrics.canvasY - 80)

# ship displays
# playerDisplay.place(x=ui_metrics.canvasX,
#                   y=ui_metrics.canvasY + ui_metrics.canvasHeight)
# enemyDisplay.place(x=ui_metrics.canvasX+400,
#                   y=ui_metrics.canvasY + ui_metrics.canvasHeight)

# ship shields                                                                              1
playerSPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + ui_metrics.shipDataOffsetY, anchor="nw")
playerSPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + ui_metrics.shipDataOffsetY, anchor="nw")
playerSPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 2*ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + ui_metrics.shipDataOffsetY, anchor="nw")
enemySPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 3*ui_metrics.shipDataWidth,
                        y=ui_metrics.canvasY + ui_metrics.canvasHeight + ui_metrics.shipDataOffsetY, anchor="nw")
enemySPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 4*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + ui_metrics.shipDataOffsetY, anchor="nw")
enemySPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 5*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + ui_metrics.shipDataOffsetY, anchor="nw")
# place shields
tmp = 0
for tmpShip,shieldArray in zip(globalVar.ships,tmpShieldsLabel):
    tmp = 0
    for progressBar in shieldArray:
        progressBar.place(x=tmp + 5, y=5)
        tmp += ((ui_metrics.shipDataWidth-10) /
                (tmpShip.shields*4+(tmpShip.shields-1)))*5
# ship armor   player
playerAPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween, anchor="nw")
uiElements.playerAPProgressBar.place(x=2, y=5)
playerAPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween, anchor="nw")
uiElements.playerAPProgressBar2.place(x=2, y=5)
playerAPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 2*ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween, anchor="nw")
uiElements.playerAPProgressBar3.place(x=2, y=5)

enemyAPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 3*ui_metrics.shipDataWidth,
                        y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween, anchor="nw")
enemyAPProgressBar.place(x=2, y=5)
enemyAPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 4*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween, anchor="nw")
enemyAPProgressBar2.place(x=2, y=5)
enemyAPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 5*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween, anchor="nw")
enemyAPProgressBar3.place(x=2, y=5)

# ship hp      player                                                                        1
playerHPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween * 2, anchor="nw")
playerHPProgressBar.place(x=2, y=5)
playerHPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween * 2, anchor="nw")
playerHPProgressBar2.place(x=2, y=5)
playerHPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 2*ui_metrics.shipDataWidth,
                          y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween * 2, anchor="nw")
playerHPProgressBar3.place(x=2, y=5)
enemyHPLabelFrame.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX + 3*ui_metrics.shipDataWidth,
                        y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween * 2, anchor="nw")
enemyHPProgressBar.place(x=2, y=5)
enemyHPLabelFrame2.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX+4*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween * 2, anchor="nw")
enemyHPProgressBar2.place(x=2, y=5)
enemyHPLabelFrame3.place(width=ui_metrics.shipDataWidth, height=54, x=ui_metrics.canvasX+5*ui_metrics.shipDataWidth,
                         y=ui_metrics.canvasY + ui_metrics.canvasHeight + uiMetrics.shipDataOffsetY + ui_metrics.shipDataOffsetBetween * 2, anchor="nw")
enemyHPProgressBar3.place(x=2, y=5)


######################### right section ###################################
startTurnButton.place(x=(ui_metrics.canvasX+ui_metrics.canvasWidth + 20),
                      y=ui_metrics.canvasY+ui_metrics.canvasHeight-20)

distanceLabel.place(x=ui_metrics.canvasX +
                    ui_metrics.canvasWidth - 160, y=ui_metrics.canvasY - 20)
# create list of elements to disable if round is in progress
UIElementsList.append(ammunitionChoiceScale)
UIElementsList.append(accuracyChoiceScale)
UIElementsList.append(gameSpeedScale)
UIElementsList.append(startTurnButton)

RadioElementsList.append(shipChoiceRadioButton1)
RadioElementsList.append(shipChoiceRadioButton2)
RadioElementsList.append(shipChoiceRadioButton3)
# clock
update(globalVar,uiElements,canvas)


root.mainloop()
