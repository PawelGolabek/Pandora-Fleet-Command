def drawGhostPoints(canvas,globalVar):
    for ship in globalVar.ships:
        for ghost in ship.ghostPoints:
            drawX = (ghost.xPos - globalVar.left) * \
                globalVar.zoom
            drawY = (ghost.yPos - globalVar.top) * globalVar.zoom 
            canvas.create_line(drawX-1*globalVar.zoom, drawY, drawX, drawY, width=globalVar.zoom,  fill='orange')
