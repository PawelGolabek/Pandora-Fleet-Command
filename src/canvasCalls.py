from math import floor
from tkinter import W
from array import *




def drawGhostPoints(canvas,var):
    for ship in var.ships:
        for ghost in ship.ghostPoints:
            drawX = int((ghost.xPos - var.left) * var.zoom)
            drawY = int((ghost.yPos - var.top) * var.zoom )
            line = canvas.create_line(int(drawX-1*var.zoom), drawY, drawX, drawY, width=int(var.zoom),  fill='orange')    # draw name
            canvas.elements.append(line)

def drawSignatures(canvas,var):
    for ship in var.ships:
        for signature in ship.signatures:
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
