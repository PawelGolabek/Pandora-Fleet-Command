import random
import time
import math
from threading import Thread

from src.shipCombat import tracer, rotateVector


def checkForCollision(currentTracer,gameRules,var,uiMetrics,colorWeight,currentOrderValue):
    if(colorWeight < 600 and colorWeight > 400):
        movementPenality = gameRules.movementPenalityMedium
        currentOrderValue -= 800
    elif(colorWeight < 400 and colorWeight > 200):
        movementPenality = gameRules.movementPenalityMedium
        currentOrderValue -= 4000
    elif(colorWeight <= 200):
        movementPenality = gameRules.movementPenalityHard
        currentOrderValue = float('inf')
    else:
        movementPenality = 0.000001  # change
    # vector normalisation
    scale = math.sqrt((currentTracer.moveOrderX-currentTracer.xPos)*(currentTracer.moveOrderX-currentTracer.xPos) +
                        (currentTracer.moveOrderY-currentTracer.yPos)*(currentTracer.moveOrderY-currentTracer.yPos))
    if(scale == 0):
        scale = 0.01
    # move order into normalised vector
    moveDirX = -(currentTracer.xPos-currentTracer.moveOrderX) / scale
    moveDirY = -(currentTracer.yPos-currentTracer.moveOrderY) / scale

    degree = currentTracer.turnRate
    rotateVector(degree, currentTracer, moveDirX, moveDirY)
    
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


def fillTracer(currentTracer,ship,currentOrderX,currentOrderY,var):
    currentTracer.xPos = ship.xPos
    currentTracer.yPos = ship.yPos
    currentTracer.xDir = ship.xDir
    currentTracer.yDir = ship.yDir
    currentTracer.turnRate = ship.turnRate
    currentTracer.speed = ship.speed
    currentTracer.moveOrderX = currentOrderX
    currentTracer.moveOrderY = currentOrderY
    currentTracer.ttl = var.turnLength + 40 # +800 to avoid unavoidable collisions next turn)
    return currentTracer

def distToClosestEnemy(ships,aiShip):
    minDist = float('inf')
    for ship in ships:
        if(ship.owner != 'ai1'):
            dist2 = (ship.xPos - aiShip.xPos)*(ship.xPos - aiShip.xPos) + (ship.yPos - aiShip.yPos)*(ship.yPos - aiShip.yPos)
            if(dist2 < minDist):
                minDist = dist2
    return minDist


class aiController():
    def systemChoice(ship,ships):
        basicEnergy = 0
        for system in ship.systemSlots:
            system.energy = system.minEnergy
            basicEnergy += system.minEnergy
        systemPool = []
        energy = ship.energyLimit - basicEnergy
        systemChecked = 0
        for system in ship.systemSlots:         # create system pool
            systemMaxPoints = system.maxEnergy
            while(systemMaxPoints > 0):
                systemPool.append(systemChecked)
                systemMaxPoints -= 1
            systemChecked += 1
                                                # add modifiers to pool if neeeded
        while(energy > 0 and len(systemPool)):
            choiceRand = random.randrange(0,len(systemPool))
            choiceNumber = systemPool.pop(choiceRand)
            (ship.systemSlots[choiceNumber]).energy += 1
            energy-=1
       
    def dijstraFill(maskMap,uiMetrics,var):
        prec = var.PFprecision
        newMaskMap = [[0 for x in range(math.ceil(uiMetrics.canvasHeight/prec))] for y in range(math.ceil(uiMetrics.canvasWidth/prec))]
        for ship in var.ships:          #place player markers
            if(ship.owner == "player1"):
                newMaskMap[round(ship.yPos / prec)][round(ship.xPos / prec)] = prec/2
        x = 0
        y = 0
        i = prec/2
        while(i):           #spread player markers
            for element in maskMap:
                adj1 = adj2 = adj3 = adj4 = -1
                if(i - prec):
                    adj1 = (i - prec)
                else:
                    adj1 = (i + prec * prec)
                if(not (i%prec == prec - 1)):
                    adj2 = i+1
                else:
                    adj2 = i-prec
                if(i+prec < prec*prec):
                    adj3 = i+prec
                else:
                    adj3 = i - prec * prec + prec
                if(not (i%prec == 0)):
                    adj4 = i-1
                else:
                    adj4 = i + prec - 1
                element1 = element[0] + element[1] + element[2]
                if(newMaskMap[int(math.floor(adj1/prec))][int(adj1%prec)] < element1 - 1):
                    newMaskMap[int(math.floor(adj1/prec))][int(adj1%prec)] = element1 - 1
            i -= 1
    #   if(colorWeight < 600 and colorWeight > 400):
    #       movementPenality = gameRules.movementPenalityMedium
    #   elif(colorWeight < 400 and colorWeight > 200):
    #       movementPenality = gameRules.movementPenalityMedium
    #       currentOrderValue -= 400
    #   elif(colorWeight <= 200):
    #       movementPenality = gameRules.movementPenalityHard
    #       currentOrderValue -= 4000
    #   maskMap

        # make it for players ( prec - )
        # make it for obstacles 9-8 (2 fase)
        return newMaskMap

    def moveOrderChoice(ship,ships,var,gameRules,uiMetrics):
        checksLeft = 40
        bestOrderX = 100    #default if everything else fails
        bestOrderY = 100    #default if everything else fails
        bestOrderValue = float('-inf')
        while(checksLeft):
            currentOrderValue = random.randint(19000, 21000)
            currentOrderX = ship.xPos + random.randint(-200, 200)
            currentOrderY = ship.yPos + random.randint(-200, 200)
            ship.ghostPoints = []
            currentTracer = tracer()
            currentTracer.xPos = ship.xPos
            currentTracer.yPos = ship.yPos
            currentTracer.xDir = ship.xDir
            currentTracer.yDir = ship.yDir
            currentTracer.turnRate = ship.turnRate
            currentTracer.speed = ship.speed
            currentTracer.moveOrderX = currentOrderX
            currentTracer.moveOrderY = currentOrderY
            currentTracer.ttl = var.turnLength + 800 # +200 to avoid unavoidable collisions next turn
            
            maskMap = aiController.dijstraFill(var.mask,uiMetrics,var) # change for dijkstra filled map
            while(True):
                # check for terrain
                if(currentTracer.ttl % 5 == 0):
                    colorWeight = maskMap[int(currentTracer.xPos/var.PFprecision)][int(currentTracer.yPos/var.PFprecision)]
                # vector normalisation
                scale = math.sqrt((currentTracer.moveOrderX-currentTracer.xPos)*(currentTracer.moveOrderX-currentTracer.xPos) +
                                    (currentTracer.moveOrderY-currentTracer.yPos)*(currentTracer.moveOrderY-currentTracer.yPos))
                if(scale == 0):
                    scale = 0.01
                # move order into normalised vector
                moveDirX = -(currentTracer.xPos-currentTracer.moveOrderX) / scale
                moveDirY = -(currentTracer.yPos-currentTracer.moveOrderY) / scale

                degree = currentTracer.turnRate
                rotateVector(degree, currentTracer, moveDirX, moveDirY)

                if(colorWeight < 600 and colorWeight > 400):
                    movementPenality = gameRules.movementPenalityMedium
                elif(colorWeight < 400 and colorWeight > 200):
                    movementPenality = gameRules.movementPenalityMedium
                    currentOrderValue -= 400
                elif(colorWeight <= 200):
                    movementPenality = gameRules.movementPenalityHard
                    currentOrderValue -= 4000
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
                currentTracer.ttl -= 1
                if(not currentTracer.ttl):
                    break
            if(currentOrderValue > bestOrderValue):
                bestOrderX = currentOrderX
                bestOrderY = currentOrderY
                bestOrderValue = currentOrderValue
            del currentTracer
            checksLeft -= 1
            if(checksLeft < 360 and bestOrderValue > 0 or not checksLeft):
                break
        ship.moveOrderX = bestOrderX
        ship.moveOrderY = bestOrderY

class aiRush(aiController):
    x = 29
