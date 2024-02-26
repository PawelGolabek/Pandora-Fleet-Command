import math
import time
from functools import partial
from tkinter import NORMAL,DISABLED
import PIL.Image
from PIL import ImageTk

import src.canvasCalls as canvasCalls
import src.naglowek as naglowek
import src.endConditions as endConditions
from src.shipCombat import checkForKilledShips,dealDamage,putTracer,updateBattleUi,detectionCheck,updateLabels,putLaser, \
    updateShipsLocation,rotateVector,updateShipsStatus,updateSignatures
from src.aiControllers import aiController
from src.inputs import mouseOnCanvas,trackMouse
from src.rootCommands import hidePausedText,showPausedText

def stop_drag(var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements):
    var.drag = ''
    root.after(1, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements))


def dragging(event,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements):
    if event.widget is root:
        if not var.drag == '':
            root.after_cancel(var.drag)
        var.drag = root.after(100, partial(stop_drag,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements))



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

def radioBox(shipLookup,uiElements,var,uiMetrics,root,canvas,uiElementsList):
    var.selection = int((var.radio).get())
    if(var.selection == 0):
        var.shipChoice = shipLookup[0].id
    if(var.selection == 1):
        var.shipChoice = shipLookup[1].id
    if(var.selection == 2):
        var.shipChoice = shipLookup[2].id
    updateBattleUi(shipLookup,uiMetrics,var,root,uiElements,canvas,uiElementsList)
    updateLabels(uiElements,shipLookup,var,root)



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
        var.resizedImage = (var.resizedImage).resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

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
        var.resizedImage = (var.resizedImage).resize((uiMetrics.canvasWidth, uiMetrics.canvasHeight), PIL.Image.ANTIALIAS)

        var.imgg = ImageTk.PhotoImage(var.resizedImage)
        canvas.imageID = canvas.create_image(0, 0, image=var.imgg, anchor='nw')
    else:
        var.imgg = ImageTk.PhotoImage(var.resizedImage)
        canvas.imageID = canvas.create_image(0, 0, image=var.imgg, anchor='nw')
  #  root.update()

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
            
def endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root): 
    var.turnInProgress = False
    for object in uiElements.UIElementsList:
        object.config(state = NORMAL, bg="#4582ec",highlightcolor = "white",fg = "white",highlightbackground = "#bfbfbf")
    if(not var.radio0Hidden):
        uiElements.RadioElementsList[0].config(state = NORMAL)
    if(not var.radio1Hidden):
        uiElements.RadioElementsList[1].config(state = NORMAL)
    if(not var.radio2Hidden):
        uiElements.RadioElementsList[2].config(state = NORMAL)
    for object in uiElements.uiSystems:
        object.config(state = NORMAL, bg="#4582ec",highlightcolor = "white")
    for object in var.uiSystemsAS:
        object.config(state = NORMAL, style = 'Red.TCheckbutton')
    uiElements.gameSpeedScale.config(bg="#4582ec",highlightcolor = "white",fg = "white")
    for ship in var.ships:
        ship.ghostPoints = []
    for ship1 in var.ships:
        if(ship1.owner == "ai1"):
            aiController.moveOrderChoice(ship1,var.ships,var,gameRules,uiMetrics)

            aiController.systemChoice(ship1,var.ships,shipLookup)
        getOrders(ship1,var,gameRules,uiMetrics,True)
    var.updateTimer = 3
    newWindow(uiMetrics,var,canvas,root)
    detectionCheck(var,uiMetrics)
    canvasCalls.drawShips(canvas,var,uiMetrics)
    canvasCalls.drawGhostPoints(canvas,var)
    canvasCalls.drawSignatures(canvas,var)
    canvasCalls.drawLandmarks(var,canvas,uiIcons,uiMetrics)
    canvasCalls.drawLasers(var,canvas,uiMetrics)
    canvasCalls.drawRockets(var,ammunitionType,canvas)
    updateShields(var.ships,var)
    updateLabels(uiElements,shipLookup,var,root)


def updateScales(uiElements,var,shipLookup):
    var.tmpCounter += 1
    shipChosen = shipLookup[var.shipChoice]
    uiElements.timeElapsedProgressBar.config(maximum=var.turnLength)
    i = 0 
    for system in uiElements.uiSystemsProgressbars:
        if(i>=len(shipChosen.systemSlots)):
            break
        system1 = shipChosen.systemSlots[i]
        if(system1.integrity < 1):
            uiElements.uiSystems[i].config(state=DISABLED, background="#D0D0D0")
            system1.energy = 0
            i+=1
            continue
        (shipChosen.systemSlots[i]).energy = (uiElements.uiSystems[i]).get()
        system['value'] = (system1.maxCooldown-system1.cooldown)
        cldwn = round((abs(system1.maxCooldown-system1.cooldown)/float(system1.maxCooldown))*100.0)
        if(cldwn == 100):
            system.config(bootstyle = 'success')
        elif(cldwn < 30):
            system.config(bootstyle = 'danger')
        elif(cldwn > 70):
            system.config(bootstyle = 'primary')
        else:
            system.config(bootstyle = 'warning')
        i+=1

def updateEnergy(var,uiElements,shipLookup):
    shipChosen = shipLookup[var.shipChoice]
    tmpEnergy = shipChosen.tmpEnergyLimit
    for system in shipChosen.systemSlots:
        tmpEnergy -= system.energy
    shipChosen.energy = tmpEnergy
    if(tmpEnergy<0):
        (var.uiEnergyLabel).config(foreground = "red")
        for radio in var.shipChoiceRadioButtons:
            radio.configure(state=DISABLED)
            (uiElements.startTurnButton).config(state = DISABLED)
    else:
        (var.uiEnergyLabel).config(foreground = "white")
        for radio in var.shipChoiceRadioButtons:
            radio.configure(state = NORMAL)
        disable = var.radio0Hidden
        if(disable):
            uiElements.RadioElementsList[0].config(state = DISABLED)
        
        disable = var.radio1Hidden
        if(disable):
            uiElements.RadioElementsList[1].config(state = DISABLED)
    
        disable = var.radio2Hidden
        if(disable):
            uiElements.RadioElementsList[2].config(state = DISABLED)

        if(not var.turnInProgress):
            (uiElements.startTurnButton).config(state = NORMAL)
    (var.uiEnergyLabel).config(text = "Energy left: " + str(shipChosen.energy))
    

def manageSystemActivations(ships,var,gameRules,uiMetrics,shipLookup):
    for ship in ships:
        for system in ship.systemSlots:
            system.activate(ship,var,gameRules,uiMetrics)

def manageSystemTriggers(ships,var,shipLookup,uiMetrics):
    for ship1 in ships:
        if(ship1.hp > 0):
            for system in ship1.systemSlots:
                system.trigger(var,ship1,ships,shipLookup,uiMetrics)
                    # trigger is activated during round and activation is between
    for ship1 in ships:
        for system in ship1.systemSlots:
            if(system.category == 'weapon'):
                system.shotThisTurn = False
 
def manageLandmarks(landmarks, ships,uiMetrics):
    for landmark in landmarks:
        landmark.wasContested = False
    for landmark in landmarks:
        if(landmark.cooldown > 0):
            landmark.cooldown -= 1
        for ship in ships:
            list = []
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos
            ghostlandmark.y = landmark.yPos
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos + uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos - uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos
            ghostlandmark.y = landmark.yPos + uiMetrics.canvasHeight
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos
            ghostlandmark.y = landmark.yPos - uiMetrics.canvasHeight
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos - uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos - uiMetrics.canvasHeight 
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos + uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos - uiMetrics.canvasHeight
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos - uiMetrics.canvasWidth 
            ghostlandmark.y = landmark.yPos + uiMetrics.canvasHeight 
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = landmark.xPos + uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos + uiMetrics.canvasHeight
            list.append(ghostlandmark)
            for element in list:
                dist = ((element.x - ship.xPos)*(element.x - ship.xPos) +
                        (element.y - ship.yPos)*(element.y - ship.yPos))
                if(dist < landmark.radius*landmark.radius):
                    if(landmark.cooldown == 0):
                        if(ship.owner == 'player1'):
                            landmark.visible = True
                        getBonus(ship, landmark.boost)
                        landmark.cooldown = landmark.defaultCooldown
                    if(not landmark.owner == ship.owner and landmark.boost == 'control'):
                        landmark.owner = ship.owner
                        if(landmark.wasContested):
                            landmark.owner = 'none'
                        landmark.wasContested = True


def getBonus(ship, boost):
    if(boost == 'health'):
        ship.hp += 50
    elif(boost == 'armor'):
        ship.ap += 50
        # add boosts

def manageRockets(missles,shipLookup,var,events,uiElements,uiMetrics,root,canvas):    # manage mid-air munitions
    for missle in missles:
        if(missle.ttl <= 0):
            missles.remove(missle)
            continue
        if(missle.sort == 'laser'):
            if(not missle.owner == 'none'):
                putLaser(missle,var,shipLookup)
                dealDamage(shipLookup[missle.target], missle.damage,var,missle.targetSystem, missle.heat,uiElements,shipLookup,root,events)
                checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas)
            missles.remove(missle)
            continue
        
        # check for terrain
        if(missle.ttl % 30 == 0):
            colorWeight = var.mask[int(missle.xPos)][int(missle.yPos)]
            if(colorWeight <= 200):
                missles.remove(missle)
                continue
        
        targetShipX = missle.xPos + missle.xDir
        targetShipY = missle.yPos + missle.yDir

        if(not missle.owner == 'none'):
            targetShipX = shipLookup[missle.target].xPos
            targetShipY = shipLookup[missle.target].yPos

        if(missle.xPos == max(missle.xPos,targetShipX)):
            aroundDistance = uiMetrics.canvasWidth - missle.xPos + targetShipX
            straightDistance = missle.xPos - targetShipX
        else:
            aroundDistance = uiMetrics.canvasWidth + missle.xPos - targetShipX
            straightDistance = targetShipX - missle.xPos

        if (straightDistance < aroundDistance):
            minDistX = targetShipX - missle.xPos        
        else:
            minDistX = missle.xPos - targetShipX
        ##
        if(missle.yPos == max(missle.yPos,targetShipY)):
            aroundDistance = uiMetrics.canvasHeight - missle.yPos + targetShipY
            straightDistance = missle.yPos - targetShipY
        else:
            aroundDistance = uiMetrics.canvasHeight + missle.yPos - targetShipY
            straightDistance = targetShipY - missle.yPos

        if (straightDistance < aroundDistance):
            minDistY = targetShipY - missle.yPos          
        else:
            minDistY = missle.yPos - targetShipY  
        scale = math.sqrt((minDistX) * (minDistX) + minDistY * minDistY)
        if scale == 0:
            scale = 0.01
        minDistX /= scale
        minDistY /= scale
        degree = missle.turnRate
        rotateVector(degree, missle, minDistX, minDistY)
        
        missle.xPos += missle.xDir*missle.speed/360         ### normalise
        missle.yPos += missle.yDir*missle.speed/360
        
        if(not missle.owner == 'none'):
            if((abs(missle.xPos - targetShipX) *
                abs(missle.xPos - targetShipX) +
                abs(missle.yPos - targetShipY) *
                abs(missle.yPos - targetShipY)) < 25):
                dealDamage(shipLookup[missle.target], missle.damage,var,missle.targetSystem,missle.heat,uiElements,shipLookup,root,events)
                missles.remove(missle)
                continue
        if(0 > missle.xPos):
            missle.xPos += uiMetrics.canvasWidth
        if(missle.xPos > uiMetrics.canvasWidth):
            missle.xPos -= uiMetrics.canvasWidth
        if(0 > missle.yPos):
            missle.yPos += uiMetrics.canvasHeight
        if(missle.yPos > uiMetrics.canvasHeight):
            missle.yPos -= uiMetrics.canvasHeight
        missle.ttl -= 1



def updateCooldowns(ships,var,shipLookup,uiMetrics):
    for ship in ships:
        for system in ship.systemSlots:
            #change if needed
            energyTicks = system.energy
            while(system.cooldown > 0 and energyTicks):
                cooldownReduction = 2
                if(system.heat < 70):
                    cooldownReduction -= 0.3
                elif(system.heat < 30):
                    cooldownReduction -= 0
                elif(system.heat > 200):
                    cooldownReduction -= 0.9
                else:
                    cooldownReduction -= 0.6
                
                if(system.integrity == system.maxIntegrity):
                    cooldownReduction -= 0
                elif(system.integrity == 0):
                    energyTicks -= 1
                    break
                elif(system.integrity < system.maxIntegrity * 0.3):
                    cooldownReduction -= 0.9
                elif(system.integrity > system.maxIntegrity * 0.7):
                    cooldownReduction -= 0.3
                else:
                    cooldownReduction -= 0.6
                if(cooldownReduction > 0):
                    system.cooldown -= cooldownReduction
                energyTicks -= 1
                if(system.cooldown < 0):
                    system.cooldown = 0
                    break
                system.trigger(var,ship,ships,shipLookup,uiMetrics)

def updateHeat(ships):
    for ship in ships:
        for system in ship.systemSlots:
            system.coolUnits += system.cooling
            system.coolTicks = math.floor(system.coolUnits/100)
            if(system.coolTicks):
                system.coolUnits -= system.coolTicks * 100
                while(system.heat > 0 and system.coolTicks):
                    system.coolTicks -= 1
                    if(system.heat < 70):
                        system.heat -= 0.5
                    if(system.heat < 30):
                        system.heat -= 0
                    elif(system.heat > 200):
                        system.heat -= 2
                    else:
                        system.heat -= 1
            system.heat = round(system.heat*100)/100
            if(system.heat < 0):
                system.heat = 0

def dealHeatDamage(ships):
    for ship in ships:
        for system in ship.systemSlots:
            if(system.heat < 70):
                heatDamage = 0.2
            if(system.heat < 30):
                heatDamage = 0
            elif(system.heat > 200):
                heatDamage = 5
            else:
                heatDamage = 1
            system.heatUnits += heatDamage
            system.heatDamageTicks = math.floor(system.heatUnits/100)
            if(system.heatDamageTicks):
                system.heatUnits -= system.heatDamageTicks*100
                while(system.integrity > 0 and system.heatDamageTicks):
                    system.integrity -= 1
                    system.heatDamageTicks -= 1

def update(var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements):
    #for ship in var.ships:
    #    print(str(ship.name) + " " + str(ship.killed))
    if(not naglowek.loadingCombat):
        if(var.drag=='' and not var.paused):
            canvas.delete('all')
            if(var.frameTime % 10 == 0):
                updateLabels(uiElements,shipLookup,var,root)
            hidePausedText(var,uiElements)
            updateScales(uiElements,var,shipLookup)
            updateEnergy(var,uiElements,shipLookup)
            var.gameSpeed = float((uiElements.gameSpeedScale).get())
            if(not var.turnInProgress):
                manageSystemActivations(var.ships,var,gameRules,uiMetrics,shipLookup)
                for ship in var.ships:
                    getOrders(ship,var,gameRules,uiMetrics)
            ticksToEndFrame = 0
            root.title(uiElements.rootTitle)
            if(var.turnInProgress):
                root.title("TURN IN PROGRESS")
                var.systemTime = time.time()
                while(ticksToEndFrame < var.gameSpeed):
                    detectionCheck(var,uiMetrics)
                    updateShipsLocation(var,uiMetrics,gameRules,shipLookup,events,uiElements,root,canvas)
                    updateShipsStatus(var,uiMetrics,gameRules,shipLookup,events,uiElements,root,canvas)
                    manageLandmarks(var.landmarks,var.ships,uiMetrics)
                    manageSystemTriggers(var.ships,var,shipLookup,uiMetrics)
                    manageRockets(var.currentMissles,shipLookup,var,events,uiElements,uiMetrics,root,canvas) 
                    updateShields(var.ships,var)
                    updateCooldowns(var.ships,var,shipLookup,uiMetrics)
                    updateHeat(var.ships)
                    dealHeatDamage(var.ships)
                    checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas)
                    updateSignatures(var.ships)
                    for laser in var.lasers:
                        if var.turnInProgress:
                            laser.ttl -= 1
                    ticksToEndFrame += 1
                    uiElements.timeElapsedProgressBar['value'] += 1
                    if(uiElements.timeElapsedProgressBar['value'] > var.turnLength):
                        root.title("AI IS THINKING")
                        endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root)
                        break
            var.input = (var.mouseWheelUp or var.mouseWheelDown or (var.mouseButton3 and var.zoom != 1 and mouseOnCanvas(var,uiMetrics)) or var.mouseButton1 )
            endConditions.killedShips(var,events)
            endConditions.disabledShips(var,events)
            endConditions.foundLandmarks(var,events)
            endConditions.dominatedLandmarks(var,events)
            endConditions.showWin(var,events,config,root,menuUiElements)
            endConditions.showLoose(var,events,config,root,menuUiElements,uiElements)
            newWindow(uiMetrics,var,canvas,root)
            canvasCalls.drawGhostPoints(canvas,var)
            canvasCalls.drawSignatures(canvas,var)
            canvasCalls.drawLandmarks(var,canvas,uiIcons,uiMetrics)
            canvasCalls.drawLasers(var,canvas,uiMetrics)
            canvasCalls.drawRockets(var,ammunitionType,canvas)
            var.mouseOnUI = False
            var.mouseWheelUp = False
            var.mouseWheelDown = False
            var.mouseButton1 = False
            var.mouseButton2 = False
            var.zoomChange = False
            canvasCalls.drawShips(canvas,var,uiMetrics)
            trackMouse(var)
            var.frameTime+=1
            if(var.finished):
                return
            if(var.updateTimer>0):
                var.updateTimer -= 1
            if(var.turnInProgress or var.mouseButton3):
                root.after(10, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements))
            else:
                root.after(100, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements))
        else:
            showPausedText(var,uiElements,uiMetrics)
