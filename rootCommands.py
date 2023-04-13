from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk

def on_closing():
   quit()

   
def hideMenuUi(uiElements):
    for uiElement in uiElements:
      uiElement.place_forget()

def hideBattleUi(uiElementsList,uiElements):
    for uiElement in uiElementsList:
        uiElement.place_forget()
    (uiElements.systemsLabelFrame).place_forget()

def placeBattleUi(staticUi,uiMetrics,canvas,globalVar,shipLookup):
    staticUi.shipChoiceRadioButton1.place(
        x=uiMetrics.canvasX + 540, y=uiMetrics.canvasY - 60)
    staticUi.shipChoiceRadioButton2.place(
        x=uiMetrics.canvasX + 700, y=uiMetrics.canvasY - 60)
    staticUi.shipChoiceRadioButton3.place(
        x=uiMetrics.canvasX + 860, y=uiMetrics.canvasY - 60)

    (staticUi.gameSpeedScale).place(x=uiMetrics.canvasX, y=uiMetrics.canvasY - 80)
    canvas.place(x=uiMetrics.canvasX, y=uiMetrics.canvasY)
    staticUi.timeElapsedProgressBar.place(
        x=uiMetrics.canvasX+120, y=uiMetrics.canvasY - 60)
    staticUi.timeElapsedLabel.place(x=uiMetrics.canvasX+140, y=uiMetrics.canvasY - 80)
    (staticUi.gameSpeedScale).place(x=uiMetrics.canvasX, y=uiMetrics.canvasY - 80)
    (staticUi.exitToMenuButton).place(x = uiMetrics.canvasX + uiMetrics.canvasWidth + 60, y = uiMetrics.canvasY - 40)

    # ship displays
    # playerDisplay.place(x=uiMetrics.canvasX,
    #                   y=uiMetrics.canvasY + uiMetrics.canvasHeight)
    # enemyDisplay.place(x=uiMetrics.canvasX+400,
    #                   y=uiMetrics.canvasY + uiMetrics.canvasHeight)

    # ship shields                                                                              1
    (staticUi.playerSPLabelFrame).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.playerSPLabelFrame2).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.playerSPLabelFrame3).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 2*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.enemySPLabelFrame).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 3*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.enemySPLabelFrame2).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 4*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    (staticUi.enemySPLabelFrame3).place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 5*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY, anchor="nw")
    # place shields
    for tmpShip,shieldArray in zip(globalVar.ships,staticUi.tmpShieldsLabel):
        tmp = 0
        for progressBar in shieldArray:
            progressBar.place(x=tmp + 5, y=5)
            tmp += ((uiMetrics.shipDataWidth-10) /
                    (tmpShip.maxShields*4+(tmpShip.maxShields-1)))*5
    # ship armor   player
    staticUi.playerAPLabelFrame.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.playerAPProgressBar.place(x=2, y=5)
    staticUi.playerAPLabelFrame2.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.playerAPProgressBar2.place(x=2, y=5)
    staticUi.playerAPLabelFrame3.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 2*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.playerAPProgressBar3.place(x=2, y=5)

    staticUi.enemyAPLabelFrame.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 3*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.enemyAPProgressBar.place(x=2, y=5)
    staticUi.enemyAPLabelFrame2.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 4*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.enemyAPProgressBar2.place(x=2, y=5)
    staticUi.enemyAPLabelFrame3.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 5*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween, anchor="nw")
    staticUi.enemyAPProgressBar3.place(x=2, y=5)

    # ship hp      player                                                                        1
    staticUi.playerHPLabelFrame.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.playerHPProgressBar.place(x=2, y=5)
    staticUi.playerHPLabelFrame2.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.playerHPProgressBar2.place(x=2, y=5)
    staticUi.playerHPLabelFrame3.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 2*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.playerHPProgressBar3.place(x=2, y=5)
    staticUi.enemyHPLabelFrame.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX + 3*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.enemyHPProgressBar.place(x=2, y=5)
    staticUi.enemyHPLabelFrame2.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX+4*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.enemyHPProgressBar2.place(x=2, y=5)
    staticUi.enemyHPLabelFrame3.place(width=uiMetrics.shipDataWidth, height=54, x=uiMetrics.canvasX+5*uiMetrics.shipDataWidth,
                            y=uiMetrics.canvasY + uiMetrics.canvasHeight + uiMetrics.shipDataOffsetY + uiMetrics.shipDataOffsetBetween * 2, anchor="nw")
    staticUi.enemyHPProgressBar3.place(x=2, y=5)


    ######################### right section ###################################
    (staticUi.startTurnButton).place(x=(uiMetrics.canvasX+uiMetrics.canvasWidth + 20),
                        y=uiMetrics.canvasY+uiMetrics.canvasHeight-20)
    ########################## SYSTEMS WIP #######################
    
    globalVar.uiEnergyLabel.place(x = 10, y = 20)

    shipChosen = shipLookup[globalVar.shipChoice]
    i=0
    for system in shipChosen.systemSlots:
        if(i>=len(shipChosen.systemSlots)):
            break
        scale = tk.Scale(staticUi.systemsLabelFrame, orient=HORIZONTAL, length=uiMetrics.systemScalesWidth, \
                            label=system.name, from_ = system.minEnergy, to=system.maxEnergy, relief=RIDGE)
        scale.set(system.energy)
        if(globalVar.turnInProgress):
            scale.config(state = 'disabled', background="#D0D0D0")
        (staticUi.uiSystems).append(scale)
        progressBar = ttk.Progressbar(staticUi.systemsLabelFrame, maximum=system.maxCooldown, length=(uiMetrics.systemScalesWidth), variable=(system.maxCooldown-system.cooldown))
        (staticUi.uiSystemsProgressbars).append(progressBar)
        scale.place(x=10,y=uiMetrics.systemScalesMarginTop+i*uiMetrics.systemScalesHeightOffset)
        progressBar.place(x=10,y=uiMetrics.systemScalesMarginTop+i*(uiMetrics.systemScalesHeightOffset)+uiMetrics.systemProgressbarsHeightOffset)
        i+=1
    (staticUi.systemsLabelFrame).place(x = uiMetrics.leftMargin, y = uiMetrics.canvasY)




    

def placeMenuUi(staticUi,uiMetrics):
    (staticUi.resumeButton).place(x=uiMetrics.rootX/2-30,y = 200)
    (staticUi.quickBattleButton).place(x=uiMetrics.rootX/2-30,y = 300)
    (staticUi.missionSelectButton).place(x=uiMetrics.rootX/2-30,y = 400)
    (staticUi.shipEditorButton).place(x=uiMetrics.rootX/2-30,y = 500)
    (staticUi.exitButton).place(x=uiMetrics.rootX/2-30,y = 600)

    

def placeShipEditorUi(staticUi,uiMetrics):

    (staticUi.shipNameInput).place(x=100,y=100)
    (staticUi.shipStatsLabelFrame).place(x=400,y=150)
    (staticUi.systemStatsLabelFrame).place(x=700,y=150)

    (staticUi.engineChoiceMenu).place(x=100,y=200)
    (staticUi.thrustersChoiceMenu).place(x=100,y=250)
    (staticUi.radarChoiceMenu).place(x=100,y=300)
    (staticUi.generatorChoiceMenu).place(x=100,y=350)

    (staticUi.systemChoiceLabelFrame).place(x = uiMetrics.editorSystemsFrameX, y = uiMetrics.editorSystemsFrameY)
    (staticUi.subsystemChoiceLabelFrame).place(x = uiMetrics.editorSystemsFrameX + 400, y = uiMetrics.editorSystemsFrameY)
    
    (staticUi.systemChoiceMenu0).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY)
    (staticUi.systemChoiceMenu1).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu2).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu3).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu4).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu5).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu6).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 6 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceMenu7).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 7 * uiMetrics.editorSystemsYOffset)
    
    (staticUi.subsystemChoiceMenu0).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY)
    (staticUi.subsystemChoiceMenu1).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu2).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu3).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu4).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu5).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu6).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 6 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu7).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 7 * uiMetrics.editorSystemsYOffset)
    

    (staticUi.saveShipButton).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY)
    (staticUi.completeButton).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY + 60)
    (staticUi.clearButton).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY + 120)
    (staticUi.exitToMenuButton).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY - 160)

def hideEditorUi(uiElementsList):
    for element in uiElementsList:
        element.place_forget()
