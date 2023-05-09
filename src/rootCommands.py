from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
import sys,os

import src.naglowek as naglowek

def on_closing():
   quit()

   
def hideMenuUi(uiElements):
    for uiElement in uiElements:
      uiElement.place_forget()

def hideBattleUi(uiElementsList,uiElements):
    for uiElement in uiElementsList:
        uiElement.place_forget()
    (uiElements.systemsLF).place_forget()

def placeBattleUi(staticUi,uiMetrics,canvas,globalVar,shipLookup):
    
    staticUi.playerShipsLF.place(x=uiMetrics.canvasX + 480, y=uiMetrics.canvasY - 95)
    staticUi.enemyShipsLF.place(x=uiMetrics.canvasX + 800, y=uiMetrics.canvasY - 95)

    staticUi.shipChoiceRadioButton0.place(x=uiMetrics.canvasX + 540, y=uiMetrics.canvasY - 30)
    staticUi.shipChoiceRadioButton1.place(x=uiMetrics.canvasX + 700, y=uiMetrics.canvasY - 30)
    staticUi.shipChoiceRadioButton2.place(x=uiMetrics.canvasX + 860, y=uiMetrics.canvasY - 30)

    staticUi.shipButton0.place(x=10,y=10)
    staticUi.shipButton1.place(x=90,y=10)
    staticUi.shipButton2.place(x=170,y=10)
    staticUi.shipButton3.place(x=10,y=10)
    staticUi.shipButton4.place(x=90,y=10)
    staticUi.shipButton5.place(x=170,y=10)

    (staticUi.gameSpeedScale).place(x=uiMetrics.canvasX, y=uiMetrics.canvasY - 80)
    canvas.place(x=uiMetrics.canvasX, y=uiMetrics.canvasY)
    staticUi.timeElapsedProgressBar.place(
        x=uiMetrics.canvasX+120, y=uiMetrics.canvasY - 60)
    staticUi.timeElapsedLabel.place(x=uiMetrics.canvasX+140, y=uiMetrics.canvasY - 80)
    (staticUi.gameSpeedScale).place(x=uiMetrics.canvasX, y=uiMetrics.canvasY - 80)
    (staticUi.exitToMenuButton).place(x = uiMetrics.canvasX + uiMetrics.canvasWidth + 120, y = uiMetrics.canvasY - 120)

    # ship shields                                                                              1
    (staticUi.playerSPLF).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.playerSPLF2).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.playerSPLF3).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 2*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.enemySPLF).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 3*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.enemySPLF2).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 4*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.enemySPLF3).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 5*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    # place shields
    for tmpShip,shieldArray in zip(globalVar.ships,staticUi.tmpShieldsLabel):
        tmp = 0
        for progressBar in shieldArray:
            progressBar.place(x=tmp + 5, y=5)
            tmp += ((uiMetrics.shipDataWidth-10) /
                    (tmpShip.maxShields*4+(tmpShip.maxShields-1)))*5
    # ship armor   player
    staticUi.playerAPLF.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.playerAPProgressBar.place(x=2, y=5)
    staticUi.playerAPLF2.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.playerAPProgressBar2.place(x=2, y=5)
    staticUi.playerAPLF3.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 2*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.playerAPProgressBar3.place(x=2, y=5)

    staticUi.enemyAPLF.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 3*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.enemyAPProgressBar.place(x=2, y=5)
    staticUi.enemyAPLF2.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 4*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.enemyAPProgressBar2.place(x=2, y=5)
    staticUi.enemyAPLF3.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 5*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.enemyAPProgressBar3.place(x=2, y=5)

    # ship hp      player                                                                        1
    staticUi.playerHPLF.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.playerHPProgressBar.place(x=2, y=5)
    staticUi.playerHPLF2.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.playerHPProgressBar2.place(x=2, y=5)
    staticUi.playerHPLF3.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 2*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.playerHPProgressBar3.place(x=2, y=5)
    staticUi.enemyHPLF.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 3*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.enemyHPProgressBar.place(x=2, y=5)
    staticUi.enemyHPLF2.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX+4*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.enemyHPProgressBar2.place(x=2, y=5)
    staticUi.enemyHPLF3.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX+5*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.enemyHPProgressBar3.place(x=2, y=5)


    ######################### right section ###################################
    (staticUi.startTurnButton).place(x=(uiMetrics.canvasX+uiMetrics.canvasWidth + 200),y=uiMetrics.canvasY+uiMetrics.canvasHeight)
    ########################## SYSTEMS WIP #######################
    
    globalVar.uiEnergyLabel.place(x = 10, y = 20)

    shipChosen = shipLookup[globalVar.shipChoice]
    i=0
    for system in shipChosen.systemSlots:
        if(i>=len(shipChosen.systemSlots)):
            break
        scale = tk.Scale(staticUi.systemsLF, orient=HORIZONTAL, length=uiMetrics.systemScalesWidth, \
                            label=system.name, from_ = system.minEnergy, to=system.maxEnergy, relief=RIDGE,fg="white", bg="#4582ec",highlightcolor = "white")
        scale.set(system.energy)
        if(globalVar.turnInProgress):
            scale.config(state = 'disabled', background="#D0D0D0")
        (staticUi.uiSystems).append(scale)
        progressBar = ttk.Progressbar(staticUi.systemsLF, bootstyle = 'primary', maximum=system.maxCooldown, length=(uiMetrics.systemScalesWidth),variable=(system.maxCooldown-system.cooldown))

        (staticUi.uiSystemsProgressbars).append(progressBar)
        scale.place(x=10,y=uiMetrics.systemScalesMarginTop+i*uiMetrics.systemScalesHeightOffset)
        progressBar.place(x=10,y=uiMetrics.systemScalesMarginTop+i*(uiMetrics.systemScalesHeightOffset)+uiMetrics.systemProgressbarsHeightOffset)
        i+=1
    (staticUi.systemsLF).place(x = uiMetrics.canvasX, y = uiMetrics.canvasY + uiMetrics.canvasHeight + 10)

    staticUi.enemyLF.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY)
    staticUi.enemyLF2.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY + 200)
    staticUi.enemyLF3.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY + 400)
    staticUi.playerLF.place(x=20, y = uiMetrics.canvasY)
    staticUi.playerLF2.place(x=20, y = uiMetrics.canvasY + 200)
    staticUi.playerLF3.place(x=20, y = uiMetrics.canvasY + 400)

    i = j = 0
    for element in staticUi.enemyLabels:
        element.place(x=10 + i*100,y=10+j*20)
        i+=1
        if(i%4==0):
            j+=1
            i=0
    i = j = 0
    for element in staticUi.enemyLabels2:
        element.place(x=10 + i*100,y=10+j*20)
        i+=1
        if(i%4==0):
            j+=1
            i=0
    i = j = 0
    for element in staticUi.enemyLabels3:
        element.place(x=10 + i*100,y=10+j*20)
        i+=1
        if(i%4==0):
            j+=1
            i=0
    i = j = 0
    for element in staticUi.playerLabels:
        element.place(x=10 + i*100,y=10+j*20)
        i+=1
        if(i%4==0):
            j+=1
            i=0
    i = j = 0
    for element in staticUi.playerLabels2:
        element.place(x=10 + i*100,y=10+j*20)
        i+=1
        if(i%4==0):
            j+=1
            i=0
    i = j = 0
    for element in staticUi.playerLabels3:
        element.place(x=10 + i*100,y=10+j*20)
        i+=1
        if(i%4==0):
            j+=1
            i=0


def placeMenuUi(root,staticUi,uiMetrics):
    root.title("Main Menu")
    if(naglowek.combatUiReady):
        staticUi.resumeButton.config(state = NORMAL)
    (staticUi.resumeButton).place(x=uiMetrics.rootX/2-30,y = 200)
    (staticUi.quickBattleButton).place(x=uiMetrics.rootX/2-30,y = 300)
    (staticUi.missionSelectButton).place(x=uiMetrics.rootX/2-30,y = 400)
    (staticUi.shipEditorButton).place(x=uiMetrics.rootX/2-30,y = 500)
    (staticUi.customGameButton).place(x=uiMetrics.rootX/2-30,y = 600)
    (staticUi.exitButton).place(x=uiMetrics.rootX/2-30,y = 700)

    

def placeShipEditorUi(staticUi,uiMetrics):

    staticUi.systemStatsLF.place(x=500,y=40)
    staticUi.systemStatsL.place(x=10,y=10)
    (staticUi.shipNameInput).place(x=100,y=100)
    (staticUi.shipStatsLF).place(x=1000,y=40)
    (staticUi.shipStatsL).place(relx = 0.1, rely = 0.0)

    (staticUi.engineChoiceMenuLF).place(x=100,y=uiMetrics.editorChoiceMenuY)
    (staticUi.thrustersChoiceMenuLF).place(x=100,y=uiMetrics.editorChoiceMenuY + uiMetrics.editorChoiceMenuOffset)
    (staticUi.radarChoiceMenuLF).place(x=100,y=uiMetrics.editorChoiceMenuY + 2 * uiMetrics.editorChoiceMenuOffset)
    (staticUi.generatorChoiceMenuLF).place(x=100,y=uiMetrics.editorChoiceMenuY + 3 * uiMetrics.editorChoiceMenuOffset)

    (staticUi.engineChoiceMenuL).place(x = uiMetrics.editorSystemsLOffsetX, y = 0)
    (staticUi.thrustersChoiceMenuL).place(x = uiMetrics.editorSystemsLOffsetX, y = 0)
    (staticUi.radarChoiceMenuL).place(x = uiMetrics.editorSystemsLOffsetX, y = 0)
    (staticUi.generatorChoiceMenuL).place(x = uiMetrics.editorSystemsLOffsetX, y = 0)

    (staticUi.engineChoiceMenu).place(x=10,y=10)
    (staticUi.thrustersChoiceMenu).place(x=10,y=10)
    (staticUi.radarChoiceMenu).place(x=10,y=10)
    (staticUi.generatorChoiceMenu).place(x=10,y=10)

    (staticUi.systemChoiceLF).place(x = uiMetrics.editorSystemsFrameX, y = uiMetrics.editorSystemsFrameY)
    (staticUi.subsystemChoiceLF).place(x = uiMetrics.editorSystemsFrameX + 400, y = uiMetrics.editorSystemsFrameY)
    
    (staticUi.systemChoiceMenu0).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY)
    (staticUi.systemChoiceMenu1).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu2).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu3).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu4).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu5).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu6).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 6 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu7).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 7 * uiMetrics.editorSystemsYOffset)
    
    (staticUi.systemChoiceL0).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY)
    (staticUi.systemChoiceL1).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL2).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL3).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL4).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL5).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL6).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 6 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL7).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 7 * uiMetrics.editorSystemsYOffset)
    
    (staticUi.subsystemChoiceMenu0).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY)
    (staticUi.subsystemChoiceMenu1).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu2).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu3).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu4).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu5).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu6).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 6 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu7).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 7 * uiMetrics.editorSystemsYOffset)
    
    (staticUi.subsystemChoiceL0).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY)
    (staticUi.subsystemChoiceL1).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL2).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL3).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL4).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL5).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL6).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 6 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL7).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 7 * uiMetrics.editorSystemsYOffset)
    
    (staticUi.saveShipButton).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY)
    (staticUi.completeButton).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY + 60)
    (staticUi.clearButton).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY + 120)
    (staticUi.exitToMenuButton).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY - 160)


def placeCustomGameUi(staticUi,uiMetrics):   
    (staticUi.blueShipLF0).place(x=uiMetrics.customBlueShipX,y=uiMetrics.customBlueShipY)
    (staticUi.blueShipLF1).place(x=uiMetrics.customBlueShipX,y=uiMetrics.customBlueShipY + uiMetrics.cgShipYoffset)
    (staticUi.blueShipLF2).place(x=uiMetrics.customBlueShipX,y=uiMetrics.customBlueShipY + uiMetrics.cgShipYoffset * 2)
    (staticUi.redShipLF0).place(x=uiMetrics.customRedShipX,y=uiMetrics.customBlueShipY)
    (staticUi.redShipLF1).place(x=uiMetrics.customRedShipX,y=uiMetrics.customBlueShipY + uiMetrics.cgShipYoffset)
    (staticUi.redShipLF2).place(x=uiMetrics.customRedShipX,y=uiMetrics.customBlueShipY + uiMetrics.cgShipYoffset * 2)

    (staticUi.blueShipOM0).place(x=10,y=10)
    (staticUi.blueShipOM1).place(x=10,y=10)
    (staticUi.blueShipOM2).place(x=10,y=10)
    (staticUi.redShipOM0).place(x=10,y=10)
    (staticUi.redShipOM1).place(x=10,y=10)
    (staticUi.redShipOM2).place(x=10,y=10)

    (staticUi.startGameButton).place(x=700,y=uiMetrics.cgStartButton)
    (staticUi.mapLF).place(x=600,y=uiMetrics.cgMapChoiceY)
    (staticUi.mapOM).place(x=10,y=10)

    (staticUi.missionCanvas).place(x=uiMetrics.customBlueShipX + 150,y=10)