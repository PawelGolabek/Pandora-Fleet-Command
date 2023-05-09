import math
from tkinter import *

import src.naglowek as naglowek
from src.ammunitionType import *
from src.colorCommands import rgbtohex

    
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

def finishSetTrue(var):
    var.finished = True

def detectionCheck(globalVar,uiMetrics):
    for ship in globalVar.ships:
        ship.visible = False
        for ship2 in globalVar.ships:
            if(not ship2.owner == ship.owner):
                list = []
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos
                ghostShip.y = ship2.yPos
                list.append(ghostShip)
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos + uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos
                list.append(ghostShip)
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos - uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos
                list.append(ghostShip)
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos
                ghostShip.y = ship2.yPos + uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos
                ghostShip.y = ship2.yPos - uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos - uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos - uiMetrics.canvasHeight 
                list.append(ghostShip)
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos + uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos - uiMetrics.canvasHeight
                list.append(ghostShip)
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos - uiMetrics.canvasWidth 
                ghostShip.y = ship2.yPos + uiMetrics.canvasHeight 
                list.append(ghostShip)
                ghostShip = naglowek.dynamic_object()
                ghostShip.x = ship2.xPos + uiMetrics.canvasWidth
                ghostShip.y = ship2.yPos + uiMetrics.canvasHeight
                list.append(ghostShip)
                for element in list:
                    distance = abs((ship.xPos-element.x)*(ship.xPos-element.x) +
                                    (ship.yPos-element.y)*(ship.yPos-element.y))
                    if(distance < ship2.detectionRange * ship2.detectionRange):
                   #     print(str(element.x) + " " + str(element.y) + " " + str(ship.id) + " " + str(ship2.id) + " " + str(distance))
                        ship.visible = True
                        break
       
def createGhostPoint(ship, xPos, yPos,number = 0):
    ghost = naglowek.ghost_point()
    ship.ghostPoints.append(ghost)
    setattr(ship.ghostPoints[-1],'xPos',xPos)
    setattr(ship.ghostPoints[-1],'yPos',yPos)
    setattr(ship.ghostPoints[-1],'number',number)

def createSignature(ship, xPos, yPos,ttl = 1200,number = 0):
    signature = naglowek.ghost_point()
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
    if(ship.owner == 'player1'):
        ship.ghostPoints = []
        currentTracer = naglowek.tracer()
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
                movementPenality = 0.000001  # change

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
    # move direction into normalised vector
    if(scale != 0):
        object.xDir = object.xDir / scale
        object.yDir = object.yDir / scale
      
def dealDamage(ship, damage,var):
    if(ship.shields > 0):
        tmp = 0
        while tmp < len(ship.shieldsState):
            if(ship.shieldsState[tmp] == var.shieldMaxState):
                ship.shieldsState[tmp] = 0
                break
            tmp += 1
        ship.shields -= 1
    else:
        while(damage > 0):
            if(ship.ap > 0):  # armor
                ship.ap -= 1
            else:
                ship.hp -= damage
                damage -= damage
            damage-=1


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
    

def createRocket(var, ship, target,_type,offsetX=0,offsetY=0):
    var.misslesShot += 1
    missleClass = _type
    # copy standard for ammunition. To be transformed into constructor like in c++ if needed
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
    setattr(var.currentMissles[-1], 'speed',missleClass.speed)
    setattr(var.currentMissles[-1], 'turnRate',
            missleClass.turnRate)
    setattr(var.currentMissles[-1], 'target', target.id)


def drawRockets(globalVar,ammunitionType,canvas):
    for missle in globalVar.currentMissles:
        color = "white"
        drawX = (missle.xPos - globalVar.left) * \
            globalVar.zoom
        drawY = (missle.yPos - globalVar.top) * \
            globalVar.zoom

        dirLineX = missle.xDir
        dirLineY = missle.yDir
        
        scale = math.sqrt((dirLineX)*(dirLineX) +
                            (dirLineY)*(dirLineY))
        dirLineX /= scale
        dirLineY /= scale

        if(not missle.sort == "kinetic"):
            if(missle.owner == "ai1"):
                _fill = "red"
            elif(missle.owner == "player1"):
                _fill = "green"
            line = canvas.create_line(drawX,drawY,drawX+dirLineX*20,drawY+dirLineY*20,fill = _fill)
            canvas.elements.append(line)
        
        if(missle.typeName == ammunitionType.type1adefault):
            line = canvas.create_line(drawX-2, drawY-2,
                            drawX+2, drawY+2, fill = color)
            canvas.elements.append(line)
        elif(missle.typeName == ammunitionType.type2adefault):
            line = canvas.create_line(drawX-5, drawY-5,
                            drawX+5, drawY+5, fill = color)
            canvas.elements.append(line)
        elif(missle.typeName == ammunitionType.kinetic1):
            line = canvas.create_line(drawX-1, drawY-1,
                            drawX+1, drawY+1, fill = color)
            canvas.elements.append(line)

        else:
            line = canvas.create_line(drawX-5, drawY-5,
                            drawX-7, drawY-5, fill = color)
            canvas.elements.append(line)
            line = canvas.create_line(drawX-5, drawY-5,
                            drawX-7, drawY-5, fill = color)
            canvas.elements.append(line)

            line = canvas.create_line(drawX+5, drawY+5,
                            drawX+7, drawY+5)
            canvas.elements.append(line)
            line = canvas.create_line(drawX+5, drawY+5,
                            drawX+5, drawY+7, fill = color)
            canvas.elements.append(line)

            line = canvas.create_line(drawX+5, drawY-5,
                            drawX+7, drawY-5, fill = color)
            canvas.elements.append(line)
            line = canvas.create_line(drawX+5, drawY-5,
                            drawX+5, drawY-7, fill = color)
            canvas.elements.append(line)

            line = canvas.create_line(drawX-5, drawY+5,
                            drawX-7, drawY+5, fill = color)
            canvas.elements.append(line)
            line = canvas.create_line(drawX-5, drawY+5,
                            drawX-5, drawY+7, fill = color)
            canvas.elements.append(line)

            line = canvas.create_line(drawX+1, drawY,
                            drawX-1, drawY, fill = color)
            canvas.elements.append(line)
            line = canvas.create_line(drawX, drawY+1,
                            drawX, drawY-1, fill = color)
            canvas.elements.append(line)

def drawLandmarks(var,canvas,uiIcons):
    for landmark in var.landmarks:
        drawX = (landmark.xPos - var.left) * \
            var.zoom   # change ###
        drawY = (landmark.yPos - var.top) * \
            var.zoom    # change ###

        radius = landmark.radius * var.zoom
        text = canvas.create_text(drawX, drawY+20,
                           text=math.ceil(landmark.cooldown/100), fill = "white")              
        canvas.elements.append(text)
        canvas.create_oval(drawX-radius, drawY-radius, drawX+radius, drawY+radius, outline = "yellow", dash=(2,3))       
        iconX = drawX
        iconY = drawY
        if(landmark.boost == 'armor'):
            image = canvas.create_image(iconX, iconY, image=uiIcons.armorIcon)
            canvas.elements.append(image)


def drawShips(canvas,var,uiMetrics):  # draw ship on the map with all of its accesories
    for ship in var.ships:
        if(ship.visible or not var.fogOfWar or ship.owner == "player1"):
            drawX = (ship.xPos - var.left) * var.zoom   # get coords relative to window
            drawY = (ship.yPos - var.top) * var.zoom

            fillColor = "red"
            if(ship.owner == "player1"):
                if(var.shipChoice == ship.id):
                    fillColor = "spring green"
                else:
                    fillColor = "white"
                drawOrderX = (ship.moveOrderX - var.left) * \
                    var.zoom    # get order relative to window
                drawOrderY = (ship.moveOrderY - var.top) * var.zoom
                line = canvas.create_line(drawOrderX+2, drawOrderY+2, drawOrderX,
                                   drawOrderY,   fill=fillColor)
                canvas.elements.append(line)
                line = canvas.create_line(drawOrderX-2, drawOrderY-2, drawOrderX,
                                   drawOrderY,   fill=fillColor)
                canvas.elements.append(line)
                line = canvas.create_line(drawOrderX+2, drawOrderY-2, drawOrderX,
                                   drawOrderY,   fill=fillColor)
                canvas.elements.append(line)
                line = canvas.create_line(drawOrderX-2, drawOrderY+2, drawOrderX,
                                   drawOrderY,   fill=fillColor)
                canvas.elements.append(line)

            line = canvas.create_line(int(drawX-5*var.zoom), 
                                int(drawY-5*var.zoom), 
                                int(drawX +5*var.zoom), 
                                int(drawY+5*var.zoom),
                                width=int(1+2*var.zoom), 
                                fill=fillColor)
            canvas.elements.append(line)
                                   
            if(ship.owner == "player1" or (not var.fogOfWar)):
                line = canvas.create_line(drawX, drawY,   drawX+(ship.xDir*20*var.zoom),
                                   drawY+(ship.yDir*20*var.zoom), fill="green")
                canvas.elements.append(line)
            if(ship.owner == "player1"):
                if(drawX < uiMetrics.canvasWidth - 50 * var.zoom):
                    line = canvas.create_text(drawX + 12 * var.zoom, drawY + 10, anchor=W,
                                font=("Purisa", 8 + math.floor(var.zoom)), text=ship.name, fill = fillColor)
                    canvas.elements.append(line)
                else:
                    line = canvas.create_text(drawX - (20 + 12 * var.zoom), drawY + 10, anchor=W,
                                font=("Purisa", 8 + math.floor(var.zoom)), text=ship.name, fill = fillColor)
                    canvas.elements.append(line)

            else:
                if(drawX < uiMetrics.canvasWidth - 50 * var.zoom):
                    line = canvas.create_text(drawX + 12 * var.zoom, drawY + 10, anchor=W,
                                font=("Purisa", 8 + math.floor(var.zoom)), text=ship.name, fill = "white")
                    canvas.elements.append(line)
                else:
                    line = canvas.create_text(drawX - (20 + 12 * var.zoom), drawY + 10, anchor=W,
                                font=("Purisa", 8 + math.floor(var.zoom)), text=ship.name, fill = "white")
                    canvas.elements.append(line)
            
            if(ship.owner == "player1"):
                fillColor = "white"
            
            if(ship.owner == "ai1"):
                fillColor = "red"
            
            list = []
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos - var.left) * var.zoom
            ghostShip.y = (ship.yPos - var.top) * var.zoom
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos + uiMetrics.canvasWidth - var.left) * var.zoom
            ghostShip.y = (ship.yPos - var.top) * var.zoom
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos - uiMetrics.canvasWidth - var.left) * var.zoom
            ghostShip.y = (ship.yPos + var.top) * var.zoom
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos - var.left) * var.zoom  
            ghostShip.y = (ship.yPos + uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos - var.left) * var.zoom 
            ghostShip.y = (ship.yPos - uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos - uiMetrics.canvasWidth  - var.left) * var.zoom 
            ghostShip.y = (ship.yPos - uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos + uiMetrics.canvasWidth  - var.left) * var.zoom 
            ghostShip.y = (ship.yPos - uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos - uiMetrics.canvasWidth  - var.left) * var.zoom 
            ghostShip.y = (ship.yPos + uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostShip)
            ghostShip = naglowek.dynamic_object()
            ghostShip.x = (ship.xPos + uiMetrics.canvasWidth  - var.left) * var.zoom 
            ghostShip.y = (ship.yPos + uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostShip)
            
            for element in list:
                x1 = element.x-ship.detectionRange*var.zoom
                x2 = element.x + ship.detectionRange*var.zoom
                y1 = element.y - ship.detectionRange*var.zoom
                y2 = element.y+ship.detectionRange*var.zoom
                canvas.create_oval(x1, y1, x2, y2, outline=ship.outlineColor, dash = (1,3))

 

       
def checkForKilledShips(events,shipLookup,var,uiElements):
    for ship1 in var.ships:
        if(ship1.hp < 1): 
            killShip(ship1.id,var,events,shipLookup,uiElements)
            
def killShip(shipId,var,events,shipLookup,uiElements):
    ship = shipLookup[shipId]
    for missle in var.currentMissles:
        if shipLookup[missle.target] == ship:
            (var.currentMissles).remove(missle)
    noEnemies = TRUE
    for progressBar in ship.shieldsLabel:
        progressBar['value'] = 0
    for ship in var.ships:
        if(not ship.owner == "player1"):
            noEnemies = FALSE
            break
    if(ship.id == 0):
        (var.shipChoiceRadioButtons).remove(uiElements.shipChoiceRadioButton0)
        (uiElements.shipChoiceRadioButton0).config(state = DISABLED)
        (uiElements.shipChoiceRadioButton0).config(state = "Destroyed")
        var.radio0Hidden = True
    elif(ship.id == 1):
        (var.shipChoiceRadioButtons).remove(uiElements.shipChoiceRadioButton1)
        (uiElements.shipChoiceRadioButton1).config(state = DISABLED)
        (uiElements.shipChoiceRadioButton1).config(state = "Destroyed")
        var.radio1Hidden = True
    elif(ship.id == 2):
        (var.shipChoiceRadioButtons).remove(uiElements.shipChoiceRadioButton2)
        (uiElements.shipChoiceRadioButton2).config(state = DISABLED)
        (uiElements.shipChoiceRadioButton2).config(state = "Destroyed")
        var.radio2Hidden = True

    if noEnemies and not events.showedWin:
        window = Toplevel()
        label = Label(window, text='yes, you win')
        label.place(x=0, y=0)
        events.showedWin = True
    elif(ship.owner == 'player1' and events.playerDestroyed == False):
        events.playerDestroyed = True
        window = Toplevel()
        label = Label(window, text='yes, you looose')
        label.place(x=0, y=0)
    for element in var.ships:
        if element.id == shipId:
            (var.ships).remove(element)
            break

def updateShips(var,uiMetrics,gameRules,shipLookup,events,uiElements):  # rotate and move the chosen ship
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
        #canvas.create_text(ship.xPos, ship.yPos + 10, anchor=W,font=("Purisa", 8+globalVar.zoom), text=colorWeight, fill="white")  # draw name
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
        elif(colorWeight < 200):
            movementPenality = gameRules.movementPenalityHard
            dealDamage(shipLookup[ship.id], 1,var)
            checkForKilledShips(events,shipLookup,var,uiElements)
        else:
            movementPenality = 0.000001  # change

        xVector = ship.xDir*ship.speed/360
        yVector = ship.yDir*ship.speed/360

        ship.xPos += xVector - xVector * movementPenality
        ship.yPos += yVector - yVector * movementPenality
        if(ship.signatureCounter >= 1200 and not ship.visible and not ship.owner == "player1"):
            createSignature(ship, ship.xPos, ship.yPos)
            ship.signatureCounter = 0
        else:
            ship.signatureCounter += 1
