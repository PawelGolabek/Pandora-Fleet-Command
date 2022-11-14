import math
from tkinter import *
from naglowek import *
from ammunitionType import *

class laser():
    def __init__(self, xPos=300, yPos=300, targetXPos=300, targetYPos=300, color = rgbtohex(22,22,22), ttl = 10): 
        self.xPos = xPos
        self.yPos = yPos
        self.targetXPos = targetXPos
        self.targetYPos = targetYPos
        self.color = color
        self.ttl = ttl

def detectionCheck(ships):
    for ship in ships:
        ship.visible = False
        if(ship.owner == 'ai1'):
            for ship2 in ships:
                if(ship2.owner == 'player1'):
                    distance = abs((ship.xPos-ship2.xPos)*(ship.xPos-ship2.xPos) +
                                   (ship.yPos-ship2.yPos)*(ship.yPos-ship2.yPos))
                    if(distance < ship2.detectionRange*ship2.detectionRange):
                        ship.visible = True
                        break
        else:
            for ship2 in ships:
                if(ship2.owner == 'ai1'):
                    distance = abs((ship.xPos-ship2.xPos)*(ship.xPos-ship2.xPos) +
                                   (ship.yPos-ship2.yPos)*(ship.yPos-ship2.yPos))
                    if(distance < ship2.detectionRange*ship2.detectionRange):
                        ship.visible = True
                        break
       
def createGhostPoint(ship, xPos, yPos,number = 0):
    ghost = ghostPoint()
    ship.ghostPoints.append(ghost)
    setattr(ship.ghostPoints[-1],'xPos',xPos)
    setattr(ship.ghostPoints[-1],'yPos',yPos)
    setattr(ship.ghostPoints[-1],'number',number)

def putTracer(ship,var,gameRules,uiMetrics): # rotate and move the chosen ship
    if(ship.owner == 'player1'):
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
        currentTracer.ttl = var.turnLength
        while(currentTracer.ttl>0):
            # check for terrain
            if(not 0 < currentTracer.xPos < uiMetrics.canvasWidth-5):
                currentTracer.ttl = 0
            if(not 0 < currentTracer.yPos < uiMetrics.canvasHeight-5):
                currentTracer.ttl = 0                        
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
    # move direviton into normalised vector
    if(scale != 0):
        object.xDir = object.xDir / scale
        object.yDir = object.yDir / scale
      
def dealDamage(ship, damage,globalVar):
    if(ship.shields > 0):
        tmp = 0
        while tmp < len(ship.shieldsState):
            if(ship.shieldsState[tmp] == globalVar.shieldMaxState):
                ship.shieldsState[tmp] = 0
                break
            tmp += 1
        ship.shields -= 1
    else:
        while(damage > 0):
            if(ship.ap > 0):  # armor
                ship.ap -= 1
            else:
                ship.hp -= 1
            damage -= 1


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
    setattr(var.currentMissles[-1], 'target', target.name)


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
            canvas.create_line(drawX,drawY,drawX+dirLineX*20,drawY+dirLineY*20,fill = _fill)
        
        if(missle.typeName == ammunitionType.type1adefault):
            canvas.create_line(drawX-2, drawY-2,
                            drawX+2, drawY+2, fill = color)
        elif(missle.typeName == ammunitionType.type2adefault):
            canvas.create_line(drawX-5, drawY-5,
                            drawX+5, drawY+5, fill = color)
        elif(missle.typeName == ammunitionType.kinetic1):
            canvas.create_line(drawX-1, drawY-1,
                            drawX+1, drawY+1, fill = color)

        else:
            canvas.create_line(drawX-5, drawY-5,
                            drawX-7, drawY-5, fill = color)
            canvas.create_line(drawX-5, drawY-5,
                            drawX-7, drawY-5, fill = color)

            canvas.create_line(drawX+5, drawY+5,
                            drawX+7, drawY+5)
            canvas.create_line(drawX+5, drawY+5,
                            drawX+5, drawY+7, fill = color)

            canvas.create_line(drawX+5, drawY-5,
                            drawX+7, drawY-5, fill = color)
            canvas.create_line(drawX+5, drawY-5,
                            drawX+5, drawY-7, fill = color)

            canvas.create_line(drawX-5, drawY+5,
                            drawX-7, drawY+5, fill = color)
            canvas.create_line(drawX-5, drawY+5,
                            drawX-5, drawY+7, fill = color)

            canvas.create_line(drawX+1, drawY,
                            drawX-1, drawY, fill = color)
            canvas.create_line(drawX, drawY+1,
                            drawX, drawY-1, fill = color)

def drawLandmarks(var,canvas,uiIcons):
    for landmark in var.landmarks:
        drawX = (landmark.xPos - var.left) * \
            var.zoom   # change ###
        drawY = (landmark.yPos - var.top) * \
            var.zoom    # change ###

        radius = landmark.radius * var.zoom
        canvas.create_text(drawX, drawY+20,
                           text=math.ceil(landmark.cooldown/100), fill = "white")
        canvas.create_oval(drawX-radius, drawY-radius,
                           drawX+radius, drawY+radius, outline = "yellow", dash=(2,3))
        iconX = drawX
        iconY = drawY
        if(landmark.boost == 'armor'):
            canvas.create_image(iconX, iconY, image=uiIcons.armorIcon)


def drawShips(canvas,globalVar):  # draw ship on the map with all of its accesories
    for ship in globalVar.ships:
        if(ship.visible or not globalVar.fogOfWar or ship.owner == "player1"):
            drawX = (ship.xPos - globalVar.left) * \
                globalVar.zoom   # get coords relative to window
            drawY = (ship.yPos - globalVar.top) * globalVar.zoom

            if(ship.owner == "player1" and ship.moveOrderX):
                drawOrderX = (ship.moveOrderX - globalVar.left) * \
                    globalVar.zoom    # get order relative to window
                drawOrderY = (ship.moveOrderY - globalVar.top) * globalVar.zoom
                canvas.create_line(drawOrderX+1, drawOrderY+1, drawOrderX,
                                   drawOrderY,   fill='white')
                canvas.create_line(drawOrderX-1, drawOrderY-1, drawOrderX,
                                   drawOrderY,   fill='white')
                canvas.create_line(drawOrderX+1, drawOrderY-1, drawOrderX,
                                   drawOrderY,   fill='white')
                canvas.create_line(drawOrderX-1, drawOrderY+1, drawOrderX,
                                   drawOrderY,   fill='white')

            if(ship.owner == "ai1"):
                canvas.create_oval(drawX-ship.detectionRange*globalVar.zoom, drawY - ship.detectionRange*globalVar.zoom,
                                   drawX + ship.detectionRange*globalVar.zoom, drawY+ship.detectionRange*globalVar.zoom, outline=ship.outlineColor, dash = (1,3))
                canvas.create_line(drawX-5*globalVar.zoom, drawY-5*globalVar.zoom, drawX +
                                   5*globalVar.zoom, drawY+5*globalVar.zoom, width=1+2*globalVar.zoom,  fill='red')
            else:
                canvas.create_oval(drawX-ship.detectionRange*globalVar.zoom,
                                   drawY - ship.detectionRange*globalVar.zoom, drawX +
                                   ship.detectionRange*globalVar.zoom,
                                   drawY+ship.detectionRange*globalVar.zoom, outline=ship.outlineColor, dash = (1,3))
                canvas.create_line(drawX-5*globalVar.zoom, drawY-5*globalVar.zoom,
                                   drawX + 5*globalVar.zoom, drawY+5*globalVar.zoom, width=1+2*globalVar.zoom,  fill='white') 

            if(ship.owner == "player1" or (not globalVar.fogOfWar)):
                canvas.create_line(drawX, drawY,   drawX+(ship.xDir*20*globalVar.zoom),
                                   drawY+(ship.yDir*20*globalVar.zoom), fill="green")
            canvas.create_text(drawX + 20, drawY + 10, anchor=W,
                               font=("Purisa", 8+math.floor(globalVar.zoom)), text=ship.name, fill = "white")  # draw name
       
def updateShips(var,uiMetrics,gameRules,shipLookup,canvas):  # rotate and move the chosen ship
    for ship in var.ships:
        if(ship.moveOrderX):
            # check for terrain
            if(not 0 < ship.xPos < uiMetrics.canvasWidth-5):
                var.ships.remove(ship)
            if(not 0 < ship.yPos < uiMetrics.canvasHeight-5):
                var.ships.remove(ship)                            
            colorWeight = var.mask[int(ship.xPos)][int(ship.yPos)]

       #     canvas.create_text(ship.xPos, ship.yPos + 10, anchor=W,font=("Purisa", 8+globalVar.zoom), text=colorWeight, fill="white")  # draw name

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
                dealDamage(shipLookup[ship.name], 1,var)
            else:
                movementPenality = 0.000001  # change

            xVector = ship.xDir*ship.speed/360
            yVector = ship.yDir*ship.speed/360

            ship.xPos += xVector - xVector * movementPenality
            ship.yPos += yVector - yVector * movementPenality
