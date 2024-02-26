import math
import time
from functools import partial
from tkinter import NORMAL,DISABLED
import PIL.Image
from PIL import ImageTk

import src.canvasCalls as canvasCalls
import src.settings as settings
import src.endConditions as endConditions
from src.shipCombat import checkForKilledShips,dealDamage,putTracer,updateBattleUi,detectionCheck,updateLabels,putLaser, \
    updateShipsLocation,rotateVector,updateShipsStatus,updateSignatures,getOrders,updateShields,newWindow
from src.aiControllers import aiController
from src.inputs import mouseOnCanvas,trackMouse
from src.rootCommands import hidePausedText,showPausedText
from src.turnManagers import startTurn,endTurn

            #### pause and stop drag calls need multiplayer options !!!!
def pauseGame(e,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions):
    if(var.paused):
        var.paused = False
        root.after(1, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions))
    else:
        var.paused = True
def stop_drag(var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions):
    var.drag = ''
    root.after(1, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions))


def dragging(event,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements,multiplayerOptions):
    if event.widget is root:
        if not var.drag == '':
            root.after_cancel(var.drag)
        var.drag = root.after(100, partial(stop_drag,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements,multiplayerOptions))



def radioBox(shipLookup,uiElements,var,uiMetrics,root,canvas,uiElementsList,multiplayerOptions):
    var.selection = int((var.radio).get())
    if(var.selection == 0):
        var.shipChoice = shipLookup[0].id
    if(var.selection == 1):
        var.shipChoice = shipLookup[1].id
    if(var.selection == 2):
        var.shipChoice = shipLookup[2].id
    updateBattleUi(shipLookup,uiMetrics,var,root,uiElements,canvas,uiElementsList,multiplayerOptions)
    updateLabels(uiElements,shipLookup,var,root)




def updateScales(uiElements,var,shipLookup):
    var.tmpCounter += 1
    shipChosen = shipLookup[var.shipChoice]
    uiElements.timeElapsedProgressBar.config(maximum=var.turnLength)
    i = 0
    sys1 = 0
    for system in uiElements.uiSystemsProgressbars:
        if(i>=len(shipChosen.systemSlots)):
            break
        system1 = shipChosen.systemSlots[i]
        if(system1.integrity < 1):
            uiElements.uiSystems[i].config(state=DISABLED, background="#D0D0D0")
            if(shipChosen.systemSlots[i].category == "weapon" and var.extendedView):
                shipChosen.optionMenus[sys1].configure(state=DISABLED, background="#D0D0D0")
                sys1 += 1
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
        system1.energyLevelLabel.config(text = "Energy: " + str(system1.energy) + '/' + str(system1.maxEnergy))

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
    

def manageSystemActivations(ships,var,gameRules,uiMetrics,shipLookup,uiElements):
    for ship in ships:
        for system in ship.systemSlots:
            system.activate(ship,var,gameRules,uiMetrics,uiElements)

def manageSystemTriggers(ships,var,shipLookup,uiMetrics,uiElements):
    for ship1 in ships:
        if(ship1.desynchronisedFired):
            ship1.desynchronisedFired -= 1
        if(ship1.hp > 0):
            for system in ship1.systemSlots:
                system.trigger(var,ship1,ships,shipLookup,uiMetrics,uiElements)
                    # trigger is activated during round and activation is between
    for ship1 in ships:
        for system in ship1.systemSlots:
            if(system.category == 'weapon'):
                system.shotThisTurn = False
 
def manageLandmarks(landmarks, ships,uiMetrics,events):
    gameEnded = ((events.showedLoose) or events.showedWin)
    for landmark in landmarks:
        landmark.wasContested = False
    for landmark in landmarks:
        if(landmark.cooldown > 0):
            landmark.cooldown -= 1
        for ship in ships:
            list = []
            ghostlandmark = settings.dynamic_object()
            ghostlandmark.x = landmark.xPos
            ghostlandmark.y = landmark.yPos
            list.append(ghostlandmark)
            ghostlandmark = settings.dynamic_object()
            ghostlandmark.x = landmark.xPos + uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos
            list.append(ghostlandmark)
            ghostlandmark = settings.dynamic_object()
            ghostlandmark.x = landmark.xPos - uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos
            list.append(ghostlandmark)
            ghostlandmark = settings.dynamic_object()
            ghostlandmark.x = landmark.xPos
            ghostlandmark.y = landmark.yPos + uiMetrics.canvasHeight
            list.append(ghostlandmark)
            ghostlandmark = settings.dynamic_object()
            ghostlandmark.x = landmark.xPos
            ghostlandmark.y = landmark.yPos - uiMetrics.canvasHeight
            list.append(ghostlandmark)
            ghostlandmark = settings.dynamic_object()
            ghostlandmark.x = landmark.xPos - uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos - uiMetrics.canvasHeight 
            list.append(ghostlandmark)
            ghostlandmark = settings.dynamic_object()
            ghostlandmark.x = landmark.xPos + uiMetrics.canvasWidth
            ghostlandmark.y = landmark.yPos - uiMetrics.canvasHeight
            list.append(ghostlandmark)
            ghostlandmark = settings.dynamic_object()
            ghostlandmark.x = landmark.xPos - uiMetrics.canvasWidth 
            ghostlandmark.y = landmark.yPos + uiMetrics.canvasHeight 
            list.append(ghostlandmark)
            ghostlandmark = settings.dynamic_object()
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
                    if(not landmark.owner == ship.owner and landmark.boost == 'control' and not gameEnded):
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

def manageRockets(missles,shipLookup,var,events,uiElements,uiMetrics,root,canvas,multiplayerOptions):    # manage mid-air munitions
    for missle in missles:
        if(missle.ttl <= 0):
            missles.remove(missle)
            continue
        if(missle.sort == 'laser'):
            if(not missle.owner == 'none'):
                putLaser(missle,var,shipLookup)
                dealDamage(shipLookup[missle.target], missle.damage,var,missle.targetSystem, missle.heat,uiElements,shipLookup,root,events)
                checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas,multiplayerOptions)
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



def updateCooldowns(ships,var,shipLookup,uiMetrics,uiElements):
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
                system.trigger(var,ship,ships,shipLookup,uiMetrics,uiElements)

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

def update(var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions):
    if(not settings.loadingCombat):
        if(var.drag=='' and not var.paused):
            canvas.delete('all')
            if(var.frameTime % 10 == 0):
                updateLabels(uiElements,shipLookup,var,root)
            hidePausedText(var,uiElements)
            updateScales(uiElements,var,shipLookup)
            updateEnergy(var,uiElements,shipLookup)
            var.gameSpeed = float((uiElements.gameSpeedScale).get())
            if(not var.turnInProgress):
                manageSystemActivations(var.ships,var,gameRules,uiMetrics,shipLookup,uiElements)
                for ship in var.ships:
                    getOrders(ship,var,gameRules,uiMetrics)
            ticksToEndFrame = 0
            root.title(uiElements.rootTitle)
            if(var.turnInProgress):
                root.title("TURN IN PROGRESS")
                var.systemTime = time.time()
                while(ticksToEndFrame < var.gameSpeed):
                    detectionCheck(var,uiMetrics)
                    updateShipsLocation(var,uiMetrics,gameRules,shipLookup,events,uiElements,root,canvas,multiplayerOptions)
                    updateShipsStatus(var,uiMetrics,gameRules,shipLookup,events,uiElements,root,canvas)
                    manageLandmarks(var.landmarks,var.ships,uiMetrics,events)
                    manageSystemTriggers(var.ships,var,shipLookup,uiMetrics,uiElements)
                    manageRockets(var.currentMissles,shipLookup,var,events,uiElements,uiMetrics,root,canvas,multiplayerOptions) 
                    updateShields(var.ships,var)
                    updateCooldowns(var.ships,var,shipLookup,uiMetrics,uiElements)
                    updateHeat(var.ships)
                    dealHeatDamage(var.ships)
                    checkForKilledShips(events,shipLookup,var,uiElements,uiMetrics,root,canvas,multiplayerOptions)
                    updateSignatures(var.ships)
                    for laser in var.lasers:
                        if var.turnInProgress:
                            laser.ttl -= 1
                    ticksToEndFrame += 1
                    uiElements.timeElapsedProgressBar['value'] += 1
                    if(uiElements.timeElapsedProgressBar['value'] > var.turnLength):
                        if(multiplayerOptions.multiplayerGame):
                            root.title("Waiting for another player")
                        else:
                            root.title("AI IS THINKING")
                        endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root,multiplayerOptions)
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
                root.after(10, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions))
            else:
                root.after(100, partial(update,var,uiElements,uiMetrics,uiIcons,canvas,events,shipLookup,gameRules,ammunitionType,root,config,menuUiElements, multiplayerOptions))
        else:
            showPausedText(var,uiElements,uiMetrics)
