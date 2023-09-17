from functools import partial
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
import sys,os
from turtle import isdown

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

def hideSystemTargets(uiElementsList):
    for uiElement in uiElementsList:
        uiElement.place_forget()


def placeBattleUi(staticUi,uiMetrics,canvas,var,shipLookup,root,uiElements):
    
    staticUi.shipChoiceRadioButton0.place(x=uiMetrics.canvasX - 120, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 160)
    staticUi.shipChoiceRadioButton1.place(x=uiMetrics.canvasX - 120, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 200)
    staticUi.shipChoiceRadioButton2.place(x=uiMetrics.canvasX - 120, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 240)

    staticUi.gameSpeedScale.place(x=uiMetrics.canvasX, y=uiMetrics.canvasY - 160)
    canvas.place(x=uiMetrics.canvasX, y=uiMetrics.canvasY)
    staticUi.timeElapsedProgressBar.place(x=uiMetrics.canvasX+uiMetrics.canvasWidth-160, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 70)
    staticUi.timeElapsedLabel.place(x=uiMetrics.canvasX+uiMetrics.canvasWidth-160, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 50)
    staticUi.gameSpeedScale.place(x=uiMetrics.canvasX+uiMetrics.canvasWidth-160, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 30)
    staticUi.gameSpeedL.place(x=uiMetrics.canvasX+uiMetrics.canvasWidth-160, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 10)
    staticUi.exitToMenuButton.place(x = uiMetrics.canvasX + uiMetrics.canvasWidth -160, y = uiMetrics.canvasY + uiMetrics.canvasHeight + 220)
    staticUi.startTurnButton.place(x = uiMetrics.canvasX + uiMetrics.canvasWidth -160, y = uiMetrics.canvasY + uiMetrics.canvasHeight + 100)

    # place shields
    for tmpShip,shieldArray in zip(var.ships,staticUi.tmpShieldsLabel):
        tmp = 0
        i = 0
        if(tmpShip.maxShields == 1):
            lenGap = 0
            lenPro = 5
        else:
            lenGap = (tmpShip.maxShields-1)
            lenPro = (tmpShip.maxShields)*4
        lenTotal = lenGap + lenPro
        for progressBar in shieldArray:
            progressBar.place(x=tmp + 5, y=5)
            tmp += (((lenGap+lenPro)/lenTotal)/tmpShip.maxShields)*(uiMetrics.systemsLFWidth)
            i+=1

    ########################## SYSTEMS  #######################
    var.uiEnergyLabel.place(x = 10, y = 20) 

    options = var.enemies
    shipTarget = StringVar()
    shipTarget.set(shipLookup[var.shipChoice].target)
    optionMenu = tk.OptionMenu(staticUi.systemsLF, shipTarget, *options.keys(), command=lambda _: [shipLookup[var.shipChoice].setTarget(shipTarget),
                                                                                                hideSystemTargets(uiElements.systemTargetsList),
                                                                                                declareSystemsTargets(var,root,shipLookup,staticUi,uiMetrics,shipTarget,uiElements)])
    optionMenu.place(x = 160, y = 20)
    declareSystemsTargets(var,root,shipLookup,staticUi,uiMetrics,shipTarget,uiElements)

def declareSystemsTargets(var,root,shipLookup,staticUi,uiMetrics,shipTarget,uiElements):
    shipChosen = shipLookup[var.shipChoice]
    i=0
    sys1 = 0
    shipChosen.optionMenus = []
    uiElements.systemTargetsList = []

    for system in shipChosen.systemSlots:
        if (i < 4):
            isDown = 0
        else:
            isDown = 1
        if(i>=len(shipChosen.systemSlots)):
            break
        scale = tk.Scale(staticUi.systemsLF, orient=HORIZONTAL, length=uiMetrics.systemScaleWidth, \
                            label=system.name, from_ = system.minEnergy, to=system.maxEnergy, relief=RIDGE,fg="white", bg="#4582ec",highlightcolor = "white")
        scale.set(system.energy)
        if(system.category == 'weapon'):
            system.options = shipLookup[var.enemies[shipTarget.get()]].systemSlots
            system.targetDict = {}
            system.elementID = 0
            system.systemTargets = []
            shipChosen.systemAS = []
            for element in system.options:
                system.systemTargets.append(system.elementID)
                system.targetDict.update({element.name : system.elementID})
                system.elementID += 1
            system.variable = StringVar(root)
            system.variable.set((list(system.targetDict.keys())[system.target]))
            anotherCommand = partial((system.setTarget),(system.targetDict[system.variable.get()]))
            a = tk.OptionMenu(staticUi.systemsLF, system.variable, *system.targetDict.keys() , command = anotherCommand)
            shipChosen.optionMenus.append(a)
            uiElements.systemTargetsList.append(a)
            system.alphaStrikeVar = IntVar()
            system.alphaStrikeVar.set(system.alphaStrike)
            anotherCommand2 = partial(system.setAS)
            shipChosen.systemAS.append(ttk.Checkbutton(staticUi.systemsLF,style = 'Red.TCheckbutton', text='AS', variable=system.alphaStrikeVar, onvalue=1, offvalue=0, command=anotherCommand2))
            shipChosen.systemAS[-1].place(x = 135 + (i - isDown*4) * uiMetrics.systemScalesWidthOffset, y = uiMetrics.systemScalesMarginTop + 60 + uiMetrics.systemScalesOffset * isDown)
            shipChosen.optionMenus[sys1].place(x = 10 + (i - isDown*4) * uiMetrics.systemScalesWidthOffset, y = uiMetrics.systemScalesMarginTop + 60 + uiMetrics.systemScalesOffset * isDown)
            sys1 += 1
        if(var.turnInProgress):
            scale.config(state = 'disabled', background="#D0D0D0")
        (staticUi.uiSystems).append(scale)
        progressBar = ttk.Progressbar(staticUi.systemsLF, bootstyle = 'primary', maximum=system.maxCooldown, length=(uiMetrics.systemScaleWidth),variable=(system.maxCooldown-system.cooldown))

        (staticUi.uiSystemsProgressbars).append(progressBar)
        scale.place(x = 10 + (i - isDown*4) * uiMetrics.systemScalesWidthOffset, y = uiMetrics.systemScalesMarginTop + uiMetrics.systemScalesOffset * isDown)
        progressBar.place(x = 10 + (i - isDown*4) * uiMetrics.systemScalesWidthOffset, y = uiMetrics.systemScalesMarginTop + 42 + uiMetrics.systemScalesOffset * isDown)
        i += 1
    (staticUi.systemsLF).place(x = uiMetrics.canvasX, y = uiMetrics.canvasY + uiMetrics.canvasHeight + 10)

    if(not shipLookup[3].name.startswith(">Not Available<")):
        staticUi.enemyLF.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY)
    if(not shipLookup[4].name.startswith(">Not Available<")):
        staticUi.enemyLF2.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY + 1 * uiMetrics.canvasHeight/5*2)
    if(not shipLookup[5].name.startswith(">Not Available<")):
        staticUi.enemyLF3.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY + 2 * uiMetrics.canvasHeight/5*2)
    if(not shipLookup[0].name.startswith(">Not Available<")):
        staticUi.playerLF.place(x=20, y = uiMetrics.canvasY)
    if(not shipLookup[1].name.startswith(">Not Available<")):
        staticUi.playerLF2.place(x=20, y = uiMetrics.canvasY + 1 * uiMetrics.canvasHeight/5*2)
    if(not shipLookup[2].name.startswith(">Not Available<")):
        staticUi.playerLF3.place(x=20, y = uiMetrics.canvasY + 2 * uiMetrics.canvasHeight/5*2)
    labelsList = [staticUi.enemyLabels, staticUi.enemyLabels2, staticUi.enemyLabels3, staticUi.playerLabels, staticUi.playerLabels2, staticUi.playerLabels3]
    for target in labelsList:
        i = j = 0
        for element in target:
            if(i<=5 and j == 0):
                element.place(x=10 + i*80,y=30)
                i+=1
                if(i%5==0):
                    j+=1
                    i=0
            else:
                if(i > 0 and j > 1):
                    element.place(x=45 + i*80,y=50+j*17)
                else:
                    if(j == 1 and not i == 0):
                        element.place(x=20 + i*80,y=50+j*17)
                    else:
                        element.place(x=10 + i*80,y=50+j*17)
                i+=1
                if(i%5==0):
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
    (staticUi.exitToMenuButton).place(x=1200, y = uiMetrics.cgStartButton - 300)
    (staticUi.mapLF).place(x=600,y=uiMetrics.cgMapChoiceY)
    (staticUi.mapOM).place(x=10,y=10)

    (staticUi.missionCanvas).place(x=uiMetrics.customBlueShipX + 150,y=10)
    
def placeSelectMenuUI(staticUi,uiMetrics):
    staticUi.levelOptionMenu.place(x=40,y=100)
    staticUi.button.place(x=40,y=150)
    staticUi.desLabelFrame.place(x=440,y=650)
    staticUi.objLabelFrame.place(x=40,y=600)

    i = 0
    staticUi.cryptonymLF.place(x=40,y=250)
    i+=1
    staticUi.dateLF.place(x=40,y=250 + i * 70)
    i+=1
    staticUi.unitLF.place(x=40,y=250 + i * 70)
    i+=1
    staticUi.reconLF.place(x=40,y=250 + i * 70)
    i+=1
    staticUi.codeLF.place(x=40,y=250 + i * 70)
    i+=1
    staticUi.threatLF.place(x=40,y=250 + i * 70)

    (staticUi.missionCanvas).place(x=uiMetrics.msCanvasX, y=uiMetrics.msCanvasY)
    (staticUi.exitToMenuButton).place(x=uiMetrics.msCanvasX + uiMetrics.msCanvasWidth + 40, y=uiMetrics.msCanvasY)