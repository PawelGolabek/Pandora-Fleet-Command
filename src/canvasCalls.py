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
                    if(drawX < uiMetrics.canvasWidth - 50 * var.zoom):
                        line = canvas.create_text(drawX + 12 * var.zoom, drawY + 10, anchor=W,
                                    font=("Purisa", 8 + floor(var.zoom)), text=ship.name, fill = fillColor)
                        canvas.elements.append(line)
                    else:
                        line = canvas.create_text(drawX - (20 + 12 * var.zoom), drawY + 10, anchor=W,
                                    font=("Purisa", 8 + floor(var.zoom)), text=ship.name, fill = fillColor)
                        canvas.elements.append(line)

                else:
                    if(drawX < uiMetrics.canvasWidth - 50 * var.zoom):
                        line = canvas.create_text(drawX + 12 * var.zoom, drawY + 10, anchor=W,
                                    font=("Purisa", 8 + floor(var.zoom)), text=ship.name, fill = "white")
                        canvas.elements.append(line)
                    else:
                        line = canvas.create_text(drawX - (20 + 12 * var.zoom), drawY + 10, anchor=W,
                                    font=("Purisa", 8 + floor(var.zoom)), text=ship.name, fill = "white")
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
        
        if(missle.typeName == ammunitionType.bolter):
            line = canvas.create_line(drawX-2, drawY-2,
                            drawX+2, drawY+2, fill = color)
            canvas.elements.append(line)
        elif(missle.typeName == ammunitionType.missle):
            line = canvas.create_line(drawX-5, drawY-5,
                            drawX+5, drawY+5, fill = color)
            canvas.elements.append(line)
        elif(missle.typeName == ammunitionType.kinetic1):
            line = canvas.create_line(drawX-1, drawY-1,
                            drawX+1, drawY+1, fill = color)
            canvas.elements.append(line)
        elif(missle.typeName == ammunitionType.incirination1adefault):
            line = canvas.create_line(drawX-2, drawY-2,
                            drawX-7, drawY+2, fill = color)
            canvas.elements.append(line)
            line = canvas.create_line(drawX-7, drawY+2,
                            drawX, drawY+2, fill = color)
            canvas.elements.append(line)
            line = canvas.create_line(drawX, drawY+2,
                            drawX+2, drawY-2, fill = color)
            canvas.elements.append(line)
            line = canvas.create_line(drawX+2, drawY-2,
                            drawX-2, drawY-2, fill = color)
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

def drawLandmarks(var,canvas,uiIcons,uiMetrics):
    for landmark in var.landmarks:
        if(landmark.visible):
            drawX = (landmark.xPos - var.left) * \
                var.zoom   # change ###
            drawY = (landmark.yPos - var.top) * \
                var.zoom    # change ###
            radius = landmark.radius * var.zoom
            if(not landmark.boost == 'spotter'):
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
            
            for element in list:
                x1 = element.x-landmark.radius*var.zoom
                x2 = element.x + landmark.radius*var.zoom
                y1 = element.y - landmark.radius*var.zoom
                y2 = element.y+landmark.radius*var.zoom
                canvas.create_oval(x1, y1, x2, y2, outline = "yellow", dash=(2,3))   
    
            iconX = drawX
            iconY = drawY
            if(landmark.boost == 'armor'):
                image = canvas.create_image(iconX, iconY, image=uiIcons.armorIcon)
                canvas.elements.append(image)
            elif(landmark.boost == 'spotter'):
                image = canvas.create_image(iconX, iconY, image=uiIcons.spotterIcon)
                canvas.elements.append(image)
