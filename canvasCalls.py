from math import floor
from tkinter import W
from array import *


def drawGhostPoints(canvas,globalVar):
    for ship in globalVar.ships:
        for ghost in ship.ghostPoints:
            drawX = (ghost.xPos - globalVar.left) * \
                globalVar.zoom
            drawY = (ghost.yPos - globalVar.top) * globalVar.zoom 
            canvas.create_line(drawX-1*globalVar.zoom, drawY, drawX, drawY, width=globalVar.zoom,  fill='orange')  
            number1 = floor(ghost.number)
            if(not number1 == 0):
                canvas.create_text(drawX-1*globalVar.zoom, drawY,  anchor=W,font=("Purisa", 8+globalVar.zoom), text=number1, fill="white")  # draw name

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
