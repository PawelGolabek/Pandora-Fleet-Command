def on_closing():
   quit()

   
def hideMenuUi(uiElements):
    for uiElement in uiElements:
      uiElement.place_forget()

def showMenuUi(uiElements):
    for uiElement in uiElements:
      uiElement.grid()

def hideBattleUi(uiElements,root):
    for uiElement in uiElements:
        uiElement.place_forget()

def placeBattleUi(staticUi,uiMetrics,canvas,globalVar):
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
    tmp = 0
    for tmpShip,shieldArray in zip(globalVar.ships,staticUi.tmpShieldsLabel):
        tmp = 0
        for progressBar in shieldArray:
            progressBar.place(x=tmp + 5, y=5)
            tmp += ((uiMetrics.shipDataWidth-10) /
                    (tmpShip.shields*4+(tmpShip.shields-1)))*5
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

