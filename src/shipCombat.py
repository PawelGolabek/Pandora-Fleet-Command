import math
from tkinter import DISABLED
import threading
import time
import PIL.Image
from PIL import ImageTk

import src.settings as settings
from src.editor.ammunitionType import ammunition
from src.colorCommands import rgbtohex
from src.rootCommands import updateBattleUi
from src.inputs import mouseOnCanvas,trackMouse
import src.endConditions as endConditions
import src.objects.tracer as tracer
from src.objects.ship import ship,destroyedShip


def updateShields(ship1,var):
    for ship1 in var.ships:
        for tmp, progressBar in enumerate(ship1.shieldsLabel):
            if(var.turnInProgress):
                tmpShieldRegen = var.shieldRegen
                while(ship1.shieldsState[tmp] < var.shieldMaxState and tmpShieldRegen > 0):
                    ship1.shieldsState[tmp] += 1
                    tmpShieldRegen -= 1
                    if(ship1.shieldsState[tmp] == var.shieldMaxState):
                        ship1.shields += 1
            if(ship1.shieldsState[tmp] > var.shieldMaxState-var.turnLength):
                progressBar.config(bootstyle = 'primary')
            else:
                progressBar.config(bootstyle = 'danger')

            progressBar['value'] = ship1.shieldsState[tmp] * 100 \
                / var.shieldMaxState
            
def newWindow(uiMetrics,var,canvas,root):
    canvas.delete(canvas.imageID)
    canPoiX = var.pointerX - uiMetrics.canvasX
    canPoiY = var.pointerY - uiMetrics.canvasY
    var.imgg = ImageTk.PhotoImage(var.resizedImage)
    if(not var.mouseWheelUp and not var.mouseWheelDown and var.mouseButton3 and var.zoom != 1 and mouseOnCanvas(var,uiMetrics)):
        if(var.zoom == 1):
            var.mouseX = ((canPoiX + var.pointerDeltaX) + var.left)
            var.mouseY = ((canPoiY + var.pointerDeltaY) + var.top)
        else:
            var.mouseX = ((canPoiX + var.pointerDeltaX) / (var.zoom-1) + var.left)
            var.mouseY = ((canPoiY + var.pointerDeltaY) / (var.zoom-1) + var.top)
        var.yellowX = (uiMetrics.canvasWidth/var.zoom)/2
        var.yellowY = (uiMetrics.canvasHeight/var.zoom)/2

        if(var.mouseX > uiMetrics.canvasWidth - var.yellowX):  # bumpers on sides
            var.mouseX = var.right - var.yellowX
        if(var.mouseX < var.yellowX):
            var.mouseX = var.left + var.yellowX
        if(var.mouseY > uiMetrics.canvasHeight - var.yellowY):
            var.mouseY = var.bottom - var.yellowY
        if(var.mouseY < var.yellowY):
            var.mouseY = var.top + var.yellowY

        var.left = var.mouseX - var.yellowX
        var.right = var.mouseX + var.yellowX
        var.top = var.mouseY - var.yellowY
        var.bottom = var.mouseY + var.yellowY
        var.mouseX = var.right - var.left
        var.mouseY = var.bottom - var.top

        var.resizedImage = (var.image).crop((var.left, var.top, var.right, var.bottom))
        var.resizedImage = (var.resizedImage).resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight),)

        var.imgg = ImageTk.PhotoImage(var.resizedImage)
        canvas.imageID = canvas.create_image(0, 0, image=var.imgg, anchor='nw')


    if((var.mouseWheelUp or var.mouseWheelDown) and mouseOnCanvas(var,uiMetrics) and var.zoomChange):
        var.imgg = var.image
        if(var.mouseWheelUp and var.zoomChange):
            if(var.zoom == 1):
                var.mouseX = (canPoiX)
                var.mouseY = (canPoiY)
            else:
                var.mouseX = ((canPoiX) / (var.zoom) + var.left)
                var.mouseY = ((canPoiY) / (var.zoom) + var.top)

        elif(var.mouseWheelDown):
            var.zoom = 1
            var.left = 0
            var.top = 0
            var.right = uiMetrics.canvasWidth
            var.bottom = uiMetrics.canvasHeight
            var.resizedImage = var.image
            var.imgg = ImageTk.PhotoImage(var.resizedImage)
    
        var.yellowX = (uiMetrics.canvasWidth/var.zoom)/2
        var.yellowY = (uiMetrics.canvasHeight/var.zoom)/2

        if(var.mouseX > uiMetrics.canvasWidth - var.yellowX):  # bumpers on sides
            var.mouseX = var.right - var.yellowX
        if(var.mouseX < var.yellowX):
            var.mouseX = var.left + var.yellowX
        if(var.mouseY > uiMetrics.canvasHeight - var.yellowY):
            var.mouseY = var.bottom - var.yellowY
        if(var.mouseY < var.yellowY):
            var.mouseY = var.top + var.yellowY

        var.left = var.mouseX - var.yellowX
        var.right = var.mouseX + var.yellowX
        var.top = var.mouseY - var.yellowY
        var.bottom = var.mouseY + var.yellowY
        var.resizedImage = (var.image).crop((var.left, var.top, var.right, var.bottom))
        var.resizedImage = (var.resizedImage).resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight),)

        var.imgg = ImageTk.PhotoImage(var.resizedImage)
        canvas.imageID = canvas.create_image(0, 0, image=var.imgg, anchor='nw')
    else:
        var.imgg = ImageTk.PhotoImage(var.resizedImage)
        canvas.imageID = canvas.create_image(0, 0, image=var.imgg, anchor='nw')


def getOrders(ship,var,gameRules,uiMetrics,forced=False):
    tracered = False
    if(ship.owner == "player1"):
        if(var.mouseButton1 and mouseOnCanvas(var,uiMetrics) and var.selection == ship.id):
            ship.moveOrderX = var.left + \
                ((var.pointerX-uiMetrics.canvasX)/var.zoom)
            ship.moveOrderY = var.top + \
                ((var.pointerY-uiMetrics.canvasY)/var.zoom)
            tracered = True
            putTracer(ship,var,gameRules,uiMetrics)
    if(not tracered and ship.owner == "player1" and forced ):
            putTracer(ship,var,gameRules,uiMetrics)


def updateLabel(uiElements,shipLookup,var,shipId):
    t0 = time.time()
    i = 0
    shipCounter = shipId
    ship = shipLookup[shipCounter]
    targetLabels = [uiElements.playerLabels,uiElements.playerLabels2,uiElements.playerLabels3, 
                    uiElements.enemyLabels,uiElements.enemyLabels2,uiElements.enemyLabels3]
    targetLabel = targetLabels[shipId]

  #  if(ship.owner == 'player1'):
  #      uiElements.systemLFs[shipCounter].config(style = 'Grey.TLabelframe')
  #  else:
  #      uiElements.systemLFs[shipCounter].config(style = 'Red.TLabelframe')
    styleToSet = 0
    if(ship.color == 'DarkOrchid1'):
        styleToSet = 'DarkOrchid1.TLabelframe'
    elif(ship.outlineColor == 'DarkOrchid2'):
        styleToSet = 'DarkOrchid2.TLabelframe'
    elif(ship.outlineColor == 'dark slate gray'):
        styleToSet = 'DarkSlateGrey.TLabelframe'
    elif(ship.outlineColor == 'indian red'):
        styleToSet = 'IndianRed.TLabelframe'
    elif(ship.outlineColor == 'Orchid4'):
        styleToSet = 'Orchid4.TLabelframe'
    elif(ship.outlineColor == 'Grey60'):
        styleToSet = 'Grey60.TLabelframe'
    elif(ship.outlineColor == 'white'):
        styleToSet = 'White.TLabelframe'
    elif(ship.outlineColor == 'brown2'):
        styleToSet = 'Brown2.TLabelframe'
    elif(ship.outlineColor == 'brown4'):
        styleToSet = 'Brown4.TLabelframe'
    elif(ship.outlineColor == 'Gold'):
        styleToSet = 'Gold.TLabelframe'
    elif(ship.outlineColor == 'goldenrod3'):
        styleToSet = 'Goldenrod3.TLabelframe'
    elif(ship.outlineColor == 'Yellow'):
        styleToSet = 'Yellow.TLabelframe'
    elif(ship.outlineColor == 'purple'):
        styleToSet = 'Purple.TLabelframe'
    elif(ship.outlineColor == 'purple2'):
        styleToSet = 'Purple2.TLabelframe'
    elif(ship.outlineColor == 'red'):
        styleToSet = 'Red.TLabelframe'
    else:
        styleToSet = 'Goldenrod3.TLabelframe'           #### 


    if(shipCounter == var.shipChoice and ship.owner == 'player1'):
        styleToSet = 'Green.TLabelframe'
        
    uiElements.systemLFs[shipCounter].config(style = styleToSet)

    targetLabel[1].config(text = str(ship.hp))
    targetLabel[3].config(text = str(ship.ap) + "           Max Energy: " + str(ship.energyLimit))

    j = 11
    for i, system in enumerate(ship.systemSlots):
        if(time.time() - t0 > 1):
            return 0
        system = ship.systemSlots[i]
        readiness = round((abs(system.maxCooldown-system.cooldown)/float(system.maxCooldown))*100.0)
        currentStyle = targetLabel[j+1].cget("style")
        styleToSet = 0
        if(readiness == 100):
            styleToSet = "Green.TLabel"
        elif(readiness < 30):
            styleToSet = "Red.TLabel"
        elif(readiness > 70):
            styleToSet = "Blue.TLabel"
        else:
            styleToSet = "Yellow.TLabel"
        if(not styleToSet == currentStyle):
            targetLabel[j+1].config(style = styleToSet)

        integrity = system.integrity
        currentStyle = targetLabel[j+2].cget("style")
        styleToSet = 0
        maxIntegrity = system.maxIntegrity
        if(integrity == maxIntegrity):
            styleToSet = "Green.TLabel"
        elif(integrity < maxIntegrity * 0.3):
            styleToSet = "Red.TLabel"
        elif(integrity > maxIntegrity * 0.7):
            styleToSet = "Blue.TLabel"
        else:
            styleToSet = "Yellow.TLabel"
        if(not styleToSet == currentStyle):
            targetLabel[j+2].config(style = styleToSet)

        heat = system.heat
        currentStyle = targetLabel[j+3].cget("style")
        if(heat < 30):
            styleToSet = "Green.TLabel"
        elif(heat < 70):
            styleToSet = "Blue.TLabel"
        elif(heat > 200):
            styleToSet = "Red.TLabel"
        else:
            styleToSet = "Yellow.TLabel"
        if(not styleToSet == currentStyle):
            targetLabel[j+3].config(style = styleToSet)
        targetLabel[j+1].config(text = str(readiness))
        targetLabel[j+2].config(text = str(integrity))
        targetLabel[j+3].config(text = str(heat))
        targetLabel[j+4].config(text = str(system.energy) + "/" + str(system.maxEnergy))
        i += 1
        j += 6
    return 0

class laser():
    def __init__(self, xPos=300, yPos=300, targetXPos=300, targetYPos=300, color = rgbtohex(22,22,22), ttl = 10): 
        self.xPos = xPos
        self.yPos = yPos
        self.targetXPos = targetXPos
        self.targetYPos = targetYPos
        self.color = color
        self.ttl = ttl

def closeWindow(window):
    window.destroy()

def getZoomMetrics(var,uiMetrics):
    var.mouseX = uiMetrics.canvasWidth/2
    var.mouseY = uiMetrics.canvasHeight/2
    var.left = 0
    var.right = uiMetrics.canvasWidth
    var.top = 0
    var.bottom = uiMetrics.canvasHeight
    var.yellowX = 0
    var.yellowY = 0
    var.zoomChange = False


def detectionCheck(globalVar,uiMetrics):
    for ship in globalVar.ships:
        ship.visible = False
        for ship2 in globalVar.ships:
            if(not ship2.owner == ship.owner):
                list = []
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos
                ghostShip.y = ship2.yPos
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos + uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos - uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos
                ghostShip.y = ship2.yPos + uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos
                ghostShip.y = ship2.yPos - uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos - uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos - uiMetrics.canvasHeight 
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos + uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos - uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos - uiMetrics.canvasWidth 
                ghostShip.y = ship2.yPos + uiMetrics.canvasHeight 
                list.append(ghostShip)
                ghostShip = settings.dynamic_object()
                ghostShip.x = ship2.xPos + uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos + uiMetrics.canvasHeight
                list.append(ghostShip)
                for element in list:
                    distance = abs((ship.xPos-element.x)*(ship.xPos-element.x) +
                                    (ship.yPos-element.y)*(ship.yPos-element.y))
                    if(distance < ship2.detectionRange * ship2.detectionRange):
                        ship.visible = True
                        break
       
def createGhostPoint(ship, xPos, yPos,number = 0):
    ghost = settings.ghost_point()
    ship.ghostPoints.append(ghost)
    setattr(ship.ghostPoints[-1],'xPos',xPos)
    setattr(ship.ghostPoints[-1],'yPos',yPos)
    setattr(ship.ghostPoints[-1],'number',number)

def createSignature(ship, xPos, yPos,ttl = 1200,number = 0):
    signature = settings.ghost_point()
    ship.signatures.append(signature)
    setattr(ship.signatures[-1],'xPos',xPos)
    setattr(ship.signatures[-1],'yPos',yPos)
    setattr(ship.signatures[-1],'number',number)
    setattr(ship.signatures[-1],'ttl',ttl)

def updateSignatures(ships):
    for ship in ships:
        if(ship.visible):
            for signature in ship.signatures:
                ship.signatures.remove(signature)
        for signature in ship.signatures:
            if(signature.ttl):
                signature.ttl -= 1
            else:
                ship.signatures.remove(signature)

def putTracer(ship,var,gameRules,uiMetrics): # rotate and move the chosen ship
    if(ship.owner == 'player1' and ship.killed == False):
        ship.ghostPoints = []
        currentTracer = tracer.tracer()
        currentTracer.xPos = ship.xPos
        currentTracer.yPos = ship.yPos
        currentTracer.xDir = ship.xDir
        currentTracer.yDir = ship.yDir
        currentTracer.turnRate = ship.turnRate
        currentTracer.speed = ship.speed
        currentTracer.moveOrderX = ship.moveOrderX
        currentTracer.moveOrderY = ship.moveOrderY
        currentTracer.ttl = var.turnLength
        while(currentTracer.ttl>0):
            colorWeight = var.mask[int(currentTracer.xPos)][ int(currentTracer.yPos)]
            
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
                movementPenality = 0.000001  # so no division by 0. Minimal friction in vacuum

            xVector = currentTracer.xDir*currentTracer.speed/360
            yVector = currentTracer.yDir*currentTracer.speed/360

            currentTracer.xPos += xVector - xVector * movementPenality
            currentTracer.yPos += yVector - yVector * movementPenality
            if(0 > currentTracer.xPos):
                currentTracer.xPos += uiMetrics.canvasWidth
            if(currentTracer.xPos >= uiMetrics.canvasWidth):
                currentTracer.xPos -= uiMetrics.canvasWidth
            if(0 > currentTracer.yPos):
                currentTracer.yPos += uiMetrics.canvasHeight
            if(currentTracer.yPos >= uiMetrics.canvasHeight):
                currentTracer.yPos -= uiMetrics.canvasHeight

            if(currentTracer.ttl % 40 == 0):
                createGhostPoint(ship, currentTracer.xPos, currentTracer.yPos)
            currentTracer.ttl -= 1
        del currentTracer
         
def updateLabels(uiElements,shipLookup,var,root):
    updateLabel(uiElements,shipLookup,var,0)
    i = 0
    n = 6
    var.t1 = []
    while(i<n):
        var.t1.append(threading.Thread(target=updateLabel, args=(uiElements,shipLookup,var,i,)))
        i+=1

    for t in var.t1:
        t.start()
    i = 0


def rotateVector(degree, object, moveDirX, moveDirY):
    if((object.xDir > moveDirX and object.yDir > -moveDirY) or object.xDir < moveDirX and object.yDir < -moveDirY):
        degree = object.turnRate
        object.xDir = math.cos((degree/360)*math.pi)*object.xDir - \
            math.sin((degree/360)*math.pi)*object.yDir
        object.yDir = math.sin((degree/360)*math.pi)*object.xDir + \
            math.cos((degree/360)*math.pi)*object.yDir
    else:
        degree = -object.turnRate  # change direction
        object.xDir = math.cos((degree/360)*math.pi)*object.xDir -  \
            math.sin((degree/360)*math.pi)*object.yDir
        object.yDir = math.sin((degree/360)*math.pi)*object.xDir + \
            math.cos((degree/360)*math.pi)*object.yDir
    scale = math.sqrt(abs(object.xDir*object.xDir+object.yDir*object.yDir))
    if(scale != 0):
        object.xDir = object.xDir / scale
        object.yDir = object.yDir / scale
      
def dealDamage(ship, dmg, var, targetSystem, heatDamage,uiElements,shipLookup,root,events):
    toUpdate = False
    if(dmg):
        toUpdate = True
    ship.uiHeatBuildup += heatDamage
    if(ship.uiHeatBuildup > 30):
        toUpdate = True
        ship.uiHeatBuildup = 0
    if(ship.shields > 0 and dmg > 0):               ## hit shield
        tmp = 0
        while (tmp < len(ship.shieldsState)):
            if(ship.shieldsState[tmp] == var.shieldMaxState):
                ship.shieldsState[tmp] = 0
                break
            tmp += 1
        ship.shields -= 1
    else:
        armorEffect = math.ceil(ship.ap/10) + 3
        if(dmg <= armorEffect):                     # all armor
            if(ship.ap <= dmg):
                dmg -= ship.ap
                ship.ap = 0
            else:
                ship.ap -= dmg
                dmg = 0
        else:
            if(dmg <= ship.ap):                     # some hit armor and pass
                if(ship.ap >= armorEffect):
                    ship.ap -= armorEffect
                    dmg -= armorEffect
                else:
                    dmg -= ship.ap
                    ship.ap = 0
            else:
                dmg -= ship.ap
                ship.ap = 0
        totalMaxIntegrity = 0
        totalIntegrity = 0
        numOfSystems = len(ship.systemSlots)
        if(targetSystem >= 0 and not targetSystem == 'no target'):
            system = ship.systemSlots[targetSystem]
            damageParts = 2 + numOfSystems
            damagePerSystem = math.floor(dmg/damageParts)
            system.heat += heatDamage
            system.heat += heatDamage
            system.heat += heatDamage
            if(system.integrity > 0):
                if(system.integrity > damagePerSystem * 2):
                    system.integrity -= damagePerSystem * 2
                    dmg -= damagePerSystem * 2
                else:
                    dmg -= system.integrity
                    system.integrity = 0
        for system1 in ship.systemSlots:                        # calculate system values
            numOfSystems += 1
            totalMaxIntegrity += system1.maxIntegrity
            totalIntegrity += system1.integrity
        if(totalIntegrity == 0):                                # deal damage to hull if no systems
            ship.hp -= dmg
            return
        damageBeforeSystems = dmg
        for system3 in ship.systemSlots:                        # deal damage according to standard values
            system3.heat += heatDamage
            system3.heat = round(system3.heat*100)/100
            dmgToSystem = (system3.maxIntegrity)/(totalMaxIntegrity)  * damageBeforeSystems
            if(system3.integrity > dmgToSystem):
                system3.integrity -= math.floor(dmgToSystem)
                dmg -= math.floor(dmgToSystem)
            else:
                dmgToSystem -= system3.integrity
                system3.integrity = 0
                dmg -= math.floor(dmgToSystem)
        ship.hp -= dmg
        endConditions.disabledShips(var,events)
        if(toUpdate):
            updateLabel(uiElements,shipLookup,var,ship.id)
        return


def putLaser(missle,var,shipLookup):
    target = shipLookup[missle.target]
    currentLaser = laser()
    currentLaser.xPos = missle.xPos
    currentLaser.yPos = missle.yPos
    currentLaser.targetXPos = target.xPos
    currentLaser.targetYPos = target.yPos
    currentLaser.color = missle.color
    currentLaser.ttl = missle.ttl
    (var.lasers).append(currentLaser)
    

def createRocket(var,ship,target,targetSystem,_type,offsetX=0,offsetY=0):
    var.misslesShot += 1
    missleClass = _type
    # copy standard for ammunition. To be transformed into constructor if needed
    missle = ammunition()
    var.currentMissles.append(missle)
    missleName = 'missle' + str(var.misslesShot)
    setattr(var.currentMissles[-1], 'name', missleName)
    setattr(var.currentMissles[-1], 'typeName', missleClass)
    setattr(var.currentMissles[-1], 'sort', missleClass.sort)
    setattr(var.currentMissles[-1], 'damage', missleClass.damage)
    setattr(var.currentMissles[-1], 'ttl', missleClass.ttl)
    setattr(var.currentMissles[-1], 'color', missleClass.color)
    setattr(var.currentMissles[-1], 'xPos', ship.xPos+offsetX)
    setattr(var.currentMissles[-1], 'yPos', ship.yPos+offsetY)
    setattr(var.currentMissles[-1], 'xDir', ship.xDir)
    setattr(var.currentMissles[-1], 'yDir', ship.yDir)
    setattr(var.currentMissles[-1], 'owner', ship.owner)
    setattr(var.currentMissles[-1], 'speed', missleClass.speed)
    setattr(var.currentMissles[-1], 'turnRate', missleClass.turnRate)
    setattr(var.currentMissles[-1], 'target', target.id)
    setattr(var.currentMissles[-1], 'heat', missleClass.heat)
    setattr(var.currentMissles[-1], 'targetSystem', targetSystem)



def checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas,multiplayerOptions):
    shipsToKill = []
    for ship1 in var.ships:
        if(ship1.hp < 1 and not ship1.killed): 
            shipsToKill.append(ship1)
    for ship2 in shipsToKill:
        killShip(ship2.id,var,events,shipLookup,uiElements,uiMetrics,root,canvas,multiplayerOptions)


def killShip(shipId,var,events,shipLookup,uiElements,uiMetrics,root,canvas,multiplayerOptions):
    ship1 = shipLookup[shipId]
    respawned = False
    x = int(ship1.xPos)
    y = int(ship1.yPos)
    name = str(ship1.name)
    var.destroyedShips.append(destroyedShip(x,y,name))
    if(ship1.owner == 'player1'):
        if(var.respawns and not ship1.name.startswith('>Not Available')):
            ship1.respawn(var,var.respawns,uiMetrics)
            respawned = True
            var.respawns-=1
    else:
        if(var.enemyRespawns and not ship1.name.startswith('>Not Available')):
            ship1.respawn(var,var.enemyRespawns,uiMetrics)
            respawned = True
            var.enemyRespawns-=1
    if(respawned):
        return
    ship1.visible = False
    ship1.killed = True
    ship1.optionMenus = []
    for missle in var.currentMissles:
        if missle.target == ship1.id:
            missle.looseTarget()
    for progressBar in ship1.shieldsLabel:
        progressBar['value'] = 0
    if(ship1.id == 0):
        uiElements.RadioElementsList[0].config(state = DISABLED)
        uiElements.RadioElementsList[0].config(text = "Destroyed")
        var.radio0Hidden = True
        choiceMade = False
        for ship in var.ships:
            if(not ship.killed):
                var.shipChosen = ship.id
                choiceMade = True
                break
        if(not choiceMade):
            var.shipChosen = 10

    elif(ship1.id == 1):
        uiElements.RadioElementsList[1].config(state = DISABLED)
        uiElements.RadioElementsList[1].config(text = "Destroyed")
        var.radio1Hidden = True
        choiceMade = False
        for ship in var.ships:
            if(not ship.killed):
                var.shipChosen = ship.id
                choiceMade = True
                break
        if(not choiceMade):
            var.shipChosen = 10

    elif(ship1.id == 2):
        uiElements.RadioElementsList[2].config(state = DISABLED)
        uiElements.RadioElementsList[2].config(text = "Destroyed")
        var.radio2Hidden = True
        choiceMade = False
        for ship in var.ships:
            if(not ship.killed):
                var.shipChosen = ship.id
                choiceMade = True
                break
        if(not choiceMade):
            var.shipChosen = 10

        ### elimination win condition to put in another file later if needed
    endConditions.killedShips(var,events)
    for element in var.ships:
        if element.id == shipId:
            (var.ships).remove(element)
            break
    setattr(var, f"wonByEliminating{ship1.id}", 1)
    setattr(var, f"lostByEliminating{ship1.id}", 1)
    updateBattleUi(shipLookup,uiMetrics,var,root,uiElements,canvas,uiElements.UIElementsList,multiplayerOptions)



def updateShipsStatus(var,uiMetrics,gameRules,shipLookup,events,uiElements,root,canvas):
    for ship in var.ships:
        if(ship.stealth):
         #   ship.visible = False
            ship.stealth -= 1


def updateShipsLocation(var,uiMetrics,gameRules,shipLookup,events,uiElements,root,canvas,multiplayerOptions):  # rotate and move the chosen ship
    for ship in var.ships:
        # check for terrain
        if(0 > ship.xPos):
            ship.xPos += uiMetrics.canvasWidth
        if(ship.xPos > uiMetrics.canvasWidth):
            ship.xPos -= uiMetrics.canvasWidth
        if(0 > ship.yPos):
            ship.yPos += uiMetrics.canvasHeight
        if(ship.yPos > uiMetrics.canvasHeight):
            ship.yPos -= uiMetrics.canvasHeight
        colorWeight = var.mask[int(ship.xPos)][int(ship.yPos)]
        # vector normalisation
        scale = math.sqrt((ship.moveOrderX-ship.xPos)*(ship.moveOrderX-ship.xPos) +
                            (ship.moveOrderY-ship.yPos)*(ship.moveOrderY-ship.yPos))
        # move order into normalised vector
        moveDirX = -(ship.xPos-ship.moveOrderX) / scale
        moveDirY = -(ship.yPos-ship.moveOrderY) / scale

        degree = ship.turnRate
        rotateVector(degree, ship, moveDirX, moveDirY)

        if(colorWeight < 600 and colorWeight > 200):
            movementPenality = gameRules.movementPenalityMedium
            dealDamage(shipLookup[ship.id], 0, var,-1, 0.035,uiElements,shipLookup,root,events)
        elif(colorWeight < 200):
            movementPenality = gameRules.movementPenalityHard
            dealDamage(shipLookup[ship.id], 1, var,-1, 1,uiElements,shipLookup,root,events)
            checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas,multiplayerOptions)
        else:
            movementPenality = 0.000001  # avoid division by 0. Minimal friction in vacuum 

        xVector = ship.xDir*ship.speed/360
        yVector = ship.yDir*ship.speed/360

        ship.xPos += xVector - xVector * movementPenality
        ship.yPos += yVector - yVector * movementPenality
        if(ship.signatureCounter >= 1200 and not ship.visible):
            createSignature(ship, ship.xPos, ship.yPos)
            ship.signatureCounter = 0
        else:
            ship.signatureCounter += 1
