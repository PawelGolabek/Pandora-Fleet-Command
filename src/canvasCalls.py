from math import floor
from tkinter import W
from array import *
import math

import src.naglowek as naglowek


def drawShips(canvas,var,uiMetrics):  # draw ship on the map with all of its accesories
    for ship in var.ships:
        if(ship.killed == False):
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
                    line = canvas.create_line(drawOrderX+uiMetrics.orderLength, drawOrderY+uiMetrics.orderLength, drawOrderX,
                                    drawOrderY,   fill=fillColor)
                    canvas.elements.append(line)
                    line = canvas.create_line(drawOrderX-uiMetrics.orderLength, drawOrderY-uiMetrics.orderLength, drawOrderX,
                                    drawOrderY,   fill=fillColor)
                    canvas.elements.append(line)
                    line = canvas.create_line(drawOrderX+uiMetrics.orderLength, drawOrderY-uiMetrics.orderLength, drawOrderX,
                                    drawOrderY,   fill=fillColor)
                    canvas.elements.append(line)
                    line = canvas.create_line(drawOrderX-uiMetrics.orderLength, drawOrderY+uiMetrics.orderLength, drawOrderX,
                                    drawOrderY,   fill=fillColor)
                    canvas.elements.append(line)
                else:
                    fillColor = ship.color
                    
                line = canvas.create_line(int(drawX-5*var.zoom),
                                    int(drawY-5*var.zoom),
                                    int(drawX +5*var.zoom),
                                    int(drawY+5*var.zoom),
                                    width=int(1+2*var.zoom),
                                    fill=fillColor)
                canvas.elements.append(line)
                                    
                if(ship.owner == "player1" or ship.visible or not var.fogOfWar):
                    line = canvas.create_line(drawX, drawY,   drawX+(ship.xDir*20*var.zoom),
                                    drawY+(ship.yDir*20*var.zoom), fill="green")
                    canvas.elements.append(line)
                if(ship.owner == "player1"):
                    _fill = 'white'
                    if(ship.stealth):
                        _fill = 'deepSkyBlue2'
                    if(drawX < uiMetrics.canvasWidth - 50 * var.zoom):
                        line = canvas.create_text(drawX + 12 * var.zoom, drawY + 10, anchor=W,
                                    font=("Purisa", 8 + floor(var.zoom)), text=ship.name, fill = _fill)
                        canvas.elements.append(line)
                    else:
                        line = canvas.create_text(drawX - (20 + 12 * var.zoom), drawY + 10, anchor=W,
                                    font=("Purisa", 8 + floor(var.zoom)), text=ship.name, fill = _fill)
                        canvas.elements.append(line)

                else:
                    _fill = 'white'
                    if(ship.stealth):
                        _fill = 'deepSkyBlue4'
                    if(drawX < uiMetrics.canvasWidth - 50 * var.zoom):
                        line = canvas.create_text(drawX + 12 * var.zoom, drawY + 10, anchor=W,
                                    font=("Purisa", 8 + floor(var.zoom)), text=ship.name, fill = _fill)
                        canvas.elements.append(line)
                    else:
                        line = canvas.create_text(drawX - (20 + 12 * var.zoom), drawY + 10, anchor=W,
                                    font=("Purisa", 8 + floor(var.zoom)), text=ship.name, fill = _fill)
                        canvas.elements.append(line)
                
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

 
def drawGhostPoints(canvas,var):
    for ship in var.ships:
        for ghost in ship.ghostPoints:
            drawX = int((ghost.xPos - var.left) * var.zoom)
            drawY = int((ghost.yPos - var.top) * var.zoom )
            line = canvas.create_line(int(drawX-1*var.zoom), drawY, drawX, drawY, width=int(var.zoom),  fill='orange')    # draw name
            canvas.elements.append(line)

def drawSignatures(canvas,var):
    if(var.fogOfWar):
        for ship in var.ships:
            for signature in ship.signatures:
                if(not ship.owner == "player1"):
                    drawX = int((signature.xPos - var.left) * var.zoom)
                    drawY = int((signature.yPos - var.top) * var.zoom )
                    line = canvas.create_line(int(drawX-4*var.zoom), int(drawY-10*var.zoom), int(drawX-8*var.zoom), int(drawY-8*var.zoom), width=int(var.zoom),  fill='white') 
                    canvas.elements.append(line) 
                    line = canvas.create_line(int(drawX-8*var.zoom), int(drawY-8*var.zoom), int(drawX-8*var.zoom), int(drawY+8*var.zoom), width=int(var.zoom),  fill='white')  
                    canvas.elements.append(line)
                    line = canvas.create_line(int(drawX-8*var.zoom), int(drawY+8*var.zoom), int(drawX-4*var.zoom), int(drawY+10*var.zoom), width=int(var.zoom),  fill='white') 
                    canvas.elements.append(line)
                    line = canvas.create_line(int(drawX+4*var.zoom), int(drawY-10*var.zoom), int(drawX+8*var.zoom), int(drawY-8*var.zoom), width=int(var.zoom),  fill='white')  
                    canvas.elements.append(line)
                    line = canvas.create_line(int(drawX+8*var.zoom), int(drawY-8*var.zoom), int(drawX+8*var.zoom), int(drawY+8*var.zoom), width=int(var.zoom),  fill='white')  
                    canvas.elements.append(line)
                    line = canvas.create_line(int(drawX+8*var.zoom), int(drawY+8*var.zoom), int(drawX+4*var.zoom), int(drawY+10*var.zoom), width=int(var.zoom),  fill='white')  
                    canvas.elements.append(line)


def createMask(var,uiMetrics):
    i = j = 0
    mapMask = [[[0,0,0] for x in range(uiMetrics.canvasHeight)] for y in range(uiMetrics.canvasWidth)]
    while(i<uiMetrics.canvasHeight):
        while(j<uiMetrics.canvasWidth):
            colors = var.imageMask.getpixel((j,i))
            mapMask[j][i] = (colors[0] + colors[1] + colors[2])
            j+=1
        j=0
        i+=1
    return mapMask

def createPFMask(var,uiMetrics):
    prec = var.PFprecision
    prec2 = prec * prec
    i = j = 0
    mapMask = [[[0,0,0] for x in range(math.ceil(uiMetrics.canvasHeight/prec))] for y in range(math.ceil(uiMetrics.canvasWidth/prec))]
    mapWidthUnits = uiMetrics.canvasWidth/prec
    mapHeightUnits = uiMetrics.canvasHeight/prec
    while(i<mapHeightUnits):
        while(j<mapWidthUnits):
            x1 = 0
            y1 = 0
            sum1 = 0
            while(y1<prec):
                while(x1<prec):
                    if((i * prec + x1) < uiMetrics.canvasHeight and (j * prec + y1) < uiMetrics.canvasWidth):
                        colors = var.imageMask.getpixel((j * prec + y1,i * prec + x1))
                        sum1 += (colors[0] + colors[1] + colors[2])
                    x1 += 1
                x1 = 0
                y1 += 1
            mapMask[j][i] = (sum1/prec2)
            j+=1
        j=0
        i+=1
    return mapMask

def drawRockets(var,ammunitionType,canvas):
    for missle in var.currentMissles:
        color = "white"
        drawX = (missle.xPos - var.left) * \
            var.zoom
        drawY = (missle.yPos - var.top) * \
            var.zoom

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
            else:
                _fill = "yellow"

            line = canvas.create_line(drawX,drawY,drawX+dirLineX*20,drawY+dirLineY*20,fill = _fill)
            canvas.elements.append(line)
        
        if(missle.typeName == ammunitionType.bolter):
            line = canvas.create_line(drawX-2*var.zoom, drawY-2*var.zoom,
                            drawX+2*var.zoom, drawY+2*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
        elif(missle.typeName == ammunitionType.missle):
            line = canvas.create_line(drawX-5*var.zoom, drawY-5*var.zoom,
                            drawX+5*var.zoom, drawY+5*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
        elif(missle.typeName == ammunitionType.kinetic1):
            line = canvas.create_line(drawX-1*var.zoom, drawY-1*var.zoom,
                            drawX+1*var.zoom, drawY+1*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
        elif(missle.typeName == ammunitionType.incirination1adefault):
            line = canvas.create_line(drawX-2*var.zoom, drawY-2*var.zoom,
                            drawX-7*var.zoom, drawY+2*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
            line = canvas.create_line(drawX-7*var.zoom, drawY+2*var.zoom,
                            drawX, drawY+2*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
            line = canvas.create_line(drawX, drawY+2*var.zoom,
                            drawX+2*var.zoom, drawY-2*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
            line = canvas.create_line(drawX+2*var.zoom, drawY-2*var.zoom,
                            drawX-2*var.zoom, drawY-2*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)

        else:
            line = canvas.create_line(drawX-5*var.zoom, drawY-5*var.zoom,
                            drawX-7*var.zoom, drawY-5*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
            line = canvas.create_line(drawX-5*var.zoom, drawY-5*var.zoom,
                            drawX-7*var.zoom, drawY-5*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)

            line = canvas.create_line(drawX+5*var.zoom, drawY+5*var.zoom,
                            drawX+7*var.zoom, drawY+5*var.zoom)
            canvas.elements.append(line)
            line = canvas.create_line(drawX+5*var.zoom, drawY+5*var.zoom,
                            drawX+5*var.zoom, drawY+7*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)

            line = canvas.create_line(drawX+5*var.zoom, drawY-5*var.zoom,
                            drawX+7*var.zoom, drawY-5*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
            line = canvas.create_line(drawX+5*var.zoom, drawY-5*var.zoom,
                            drawX+5*var.zoom, drawY-7*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)

            line = canvas.create_line(drawX-5*var.zoom, drawY+5*var.zoom,
                            drawX-7*var.zoom, drawY+5*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
            line = canvas.create_line(drawX-5*var.zoom, drawY+5*var.zoom,
                            drawX-5*var.zoom, drawY+7*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)

            line = canvas.create_line(drawX+1*var.zoom, drawY,
                            drawX-1*var.zoom, drawY, fill = color, width=int(var.zoom))
            canvas.elements.append(line)
            line = canvas.create_line(drawX, drawY+1*var.zoom,
                            drawX, drawY-1*var.zoom, fill = color, width=int(var.zoom))
            canvas.elements.append(line)

def drawLandmarks(var,canvas,uiIcons,uiMetrics):
    for landmark in var.landmarks:
        if(landmark.visible):
            drawX = (landmark.xPos - var.left) * \
                var.zoom   # change ###
            drawY = (landmark.yPos - var.top) * \
                var.zoom    # change ###
            radius = landmark.radius * var.zoom
            if(not landmark.boost == 'spotter' and not landmark.boost == 'control'):
                text = canvas.create_text(drawX, drawY+20,
                                text=math.ceil(landmark.cooldown/100), fill = "white")               
                canvas.elements.append(text)

            list = []
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos - var.left) * var.zoom
            ghostlandmark.y = (landmark.yPos - var.top) * var.zoom
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos + uiMetrics.canvasWidth - var.left) * var.zoom
            ghostlandmark.y = (landmark.yPos - var.top) * var.zoom
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos - uiMetrics.canvasWidth - var.left) * var.zoom
            ghostlandmark.y = (landmark.yPos + var.top) * var.zoom
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos - var.left) * var.zoom  
            ghostlandmark.y = (landmark.yPos + uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos - var.left) * var.zoom 
            ghostlandmark.y = (landmark.yPos - uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos - uiMetrics.canvasWidth  - var.left) * var.zoom 
            ghostlandmark.y = (landmark.yPos - uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos + uiMetrics.canvasWidth  - var.left) * var.zoom 
            ghostlandmark.y = (landmark.yPos - uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos - uiMetrics.canvasWidth  - var.left) * var.zoom 
            ghostlandmark.y = (landmark.yPos + uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostlandmark)
            ghostlandmark = naglowek.dynamic_object()
            ghostlandmark.x = (landmark.xPos + uiMetrics.canvasWidth  - var.left) * var.zoom 
            ghostlandmark.y = (landmark.yPos + uiMetrics.canvasHeight - var.top) * var.zoom
            list.append(ghostlandmark)
            
            if(landmark.owner == 'player1'):
                outln = '#02640a'
            elif(landmark.owner == 'ai1'):
                outln = '#802200'
            else:
                outln = '#646402'
            
            for element in list:
                x1 = element.x-landmark.radius*var.zoom
                x2 = element.x + landmark.radius*var.zoom
                y1 = element.y - landmark.radius*var.zoom
                y2 = element.y+landmark.radius*var.zoom
                canvas.create_oval(x1, y1, x2, y2, outline = outln, dash=(7,2))   
    
            iconX = drawX
            iconY = drawY
            if(landmark.boost == 'armor'):
                image = canvas.create_image(iconX, iconY, image=uiIcons.armorIcon)
                canvas.elements.append(image)
            elif(landmark.boost == 'spotter'):
                image = canvas.create_image(iconX, iconY, image=uiIcons.spotterIcon)
                canvas.elements.append(image)
            elif(landmark.boost == 'control'):
                if(landmark.owner == 'player1'):
                    image = canvas.create_image(iconX, iconY, image=uiIcons.controlIconP)
                elif(landmark.owner == 'ai1'):
                    image = canvas.create_image(iconX, iconY, image=uiIcons.controlIconE)
                elif(landmark.owner == 'none'):
                    image = canvas.create_image(iconX, iconY, image=uiIcons.controlIconN)
                canvas.elements.append(image)

def drawLasers(var,canvas,uiMetrics):
    for laser in var.lasers:
        if laser.ttl>0:
            drawX = (laser.xPos - var.left) * var.zoom
            drawY = (laser.yPos - var.top) * var.zoom
            aroundFlagX = False
            aroundFlagY = False
            if(laser.xPos == max(laser.xPos,laser.targetXPos)):
                aroundDistance = uiMetrics.canvasWidth - laser.xPos + laser.targetXPos
                laserCloserToRight = True
                straightDistance = laser.xPos - laser.targetXPos
            else:
                aroundDistance = uiMetrics.canvasWidth + laser.xPos - laser.targetXPos
                laserCloserToRight = False
                straightDistance = laser.targetXPos - laser.xPos

            if (straightDistance < aroundDistance):
                x2 = laser.targetXPos
                x3 = laser.xPos
                x4 = laser.targetXPos
            else:
                aroundFlagX = True
                if(laserCloserToRight):
                    x2 = laser.targetXPos + uiMetrics.canvasWidth
                    x3 = laser.xPos - uiMetrics.canvasWidth
                    x4 = laser.targetXPos
                else: 
                    x2 = laser.targetXPos - uiMetrics.canvasWidth
                    x3 = laser.xPos + uiMetrics.canvasWidth
                    x4 = laser.targetXPos
            ##
            if(laser.yPos == max(laser.yPos,laser.targetYPos)):
                aroundDistance = uiMetrics.canvasHeight - laser.yPos + laser.targetYPos
                laserCloserToDown = True
                straightDistance = laser.yPos - laser.targetYPos
            else:
                aroundDistance = uiMetrics.canvasHeight + laser.yPos - laser.targetYPos
                laserCloserToDown = False
                straightDistance = laser.targetYPos - laser.yPos

            if (straightDistance < aroundDistance):
                y2 = laser.targetYPos 
                y3 = laser.yPos
                y4 = laser.targetYPos
            else:
                aroundFlagY = True
                if(laserCloserToDown):
                    y2 = laser.targetYPos + uiMetrics.canvasHeight
                    y3 = laser.yPos - uiMetrics.canvasHeight
                    y4 = laser.targetYPos
                else: 
                    y2 = laser.targetYPos - uiMetrics.canvasHeight
                    y3 = laser.yPos + uiMetrics.canvasHeight
                    y4 = laser.targetYPos

            drawX2 = (x2- var.left) * var.zoom
            drawX3 = (x3- var.left) * var.zoom
            drawX4 = (x4- var.left) * var.zoom

            drawY2 = (y2- var.top) * var.zoom
            drawY3 = (y3- var.top) * var.zoom
            drawY4 = (y4- var.top) * var.zoom

            line = canvas.create_line(drawX,drawY,drawX2,drawY2, fill = laser.color, #stipple="gray75"
                                      )
            canvas.elements.append(line)
            

            if(aroundFlagX or aroundFlagY):
                line = canvas.create_line(drawX3,drawY3,drawX4,drawY4, fill = laser.color, #stipple="gray75"
                                          )
                canvas.elements.append(line)
        else:
            (var.lasers).remove(laser)
            del laser