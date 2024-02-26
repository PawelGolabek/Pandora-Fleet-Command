from functools import partial
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from turtle import isdown

import src.settings as settings
from src.multiplayer.netCommands import disconnect


def on_closing():
   quit()


def hideMultiplayerLabel(multiplayerOptions,uiElements):
    if(multiplayerOptions.multiplayerGame):
        multiplayerOptions.statusLabel.place_forget()
        disconnect(multiplayerOptions)

def hideMultiplayerMenuUi(uiElements):
    for uiElement in uiElements:
      uiElement.place_forget()

def hideMenuUi(uiElements):
    for uiElement in uiElements:
      uiElement.place_forget(),

def hideBattleUi(uiElementsList,uiElements):
    for uiElement in uiElementsList:
        uiElement.place_forget()
    (uiElements.systemsLF).place_forget()

def hideSystemTargets(uiElementsList):
    for uiElement in uiElementsList:
        uiElement.place_forget()

def updateCheckbox(var,shipLookup,uiElements):    
    shipChosen = shipLookup[var.shipChoice]
    var.uiTargetOnlyCB = ttk.Checkbutton(uiElements.systemsLF,variable = shipChosen.CBVar, style = 'Red.TCheckbutton', text = "Target Only", onvalue = 1, offvalue = 0,command=shipChosen.setTargetOnly)

    shipChosen = shipLookup[var.shipChoice]
    if(shipChosen.targetOnly):
        shipChosen.CBVar.set(1)
    else:
        shipChosen.CBVar.set(0)
    var.uiTargetOnlyCB.place(x = 500, y = 3)
    var.uiTargetOnlyCB.invoke()
    var.uiTargetOnlyCB.invoke()

def showPausedText(var,uiElements,uiMetrics):
    if(var.pausedLVisible == False):
        uiElements.pausedL.place(x = uiMetrics.canvasWidth/2-uiMetrics.pausedLWidth/2 - 2, y = uiMetrics.canvasHeight/2-uiMetrics.pausedLHeight/2 - 2)
        var.pausedLVisible = True

def hidePausedText(var,uiElements):
    if(var.pausedLVisible == True):
        uiElements.pausedL.place_forget()
        var.pausedLVisible = False

def clearUtilityChoice(uiElements,var):
    for widget in (uiElements.systemsLF).winfo_children():
        widget.destroy()
    (uiElements.systemsLF).destroy()
    uiElements.uiSystems = []
    uiElements.uiSystemsProgressbars = []

       
def updateBattleUi(shipLookup,uiMetrics,var,root,uiElements,canvas,uiElementsList,multiplayerOptions):
    clearUtilityChoice(uiElements,var)
    shipChosen = shipLookup[var.shipChoice]
    uiElements.systemsLF = ttk.Labelframe(root,style = 'Green.TLabelframe', width=uiMetrics.canvasWidth, \
                                                    height = uiMetrics.systemScalesLFHeight, text= shipChosen.name + " systems", \
                                                    borderwidth=2, relief="groove")
    var.uiEnergyLabel = ttk.Label(uiElements.systemsLF,style = 'Grey.TLabel', width=20, text = "Energy remaining: " + str(shipChosen.energy), font = "16")
    var.paused = True
  #  uiElementsList.append(uiElements.systemsLF)
    showPausedText(var,uiElements,uiMetrics)
    hideBattleUi(uiElements.staticUi,uiElements)
    placeBattleUi(uiElements,uiMetrics,canvas,var,shipLookup,root,uiElements,uiElementsList,multiplayerOptions)
    hidePausedText(var,uiElements)
    var.paused = False
    return


def viewButtonCommand(var, Tbutton):
    var.extendedView = not var.extendedView
    if(var.extendedView):
        Tbutton.configure(text = "Extended View")
    else:
        Tbutton.configure(text = "Simplified View")

def showClientOptions(uiElements):
    uiElements.hostBFrame.place(x=100,y=400)
    uiElements.IPEntry.place(x=100,y=100)
    uiElements.clientBFrame.place(x=100,y=190)
    uiElements.clientGameButton.pack()

def placeMultiplayerMenuUi(uiElements):
  # multiplayerMenuUiList.append(multiplayerMenuUi.hostBFrame)
  # multiplayerMenuUiList.append(multiplayerMenuUi.clientBFrame)
  # multiplayerMenuUiList.append(multiplayerMenuUi.customGameButtonUser)
  # multiplayerMenuUiList.append(multiplayerMenuUi.statusLabel)
    uiElements.hostBFrame.place(x=100,y=400)
    uiElements.clientBFrame.place(x=100,y=190)
    uiElements.statusLabel.place(x=100,y=300)

    uiElements.IPEntry.place(x=100,y=100)
    uiElements.copyIPBFrame.place(x=400,y=300)

    uiElements.copyIPB.pack()
    uiElements.hostGameButton.pack()
    uiElements.clientGameButton.pack()



def placeBattleUi(staticUi,uiMetrics,canvas,var,shipLookup,root,uiElements,uiElementsList,multiplayerOptions):
    
    if(not shipLookup[0].name.startswith(">Not Available<") or not shipLookup[0].killed):
        disable = var.radio0Hidden
        if(disable):
            uiElements.RadioElementsList[2].config(state = DISABLED)
        uiElements.RadioElementsList[0].place(x=uiMetrics.canvasX - 120, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 160)
        
    if(not shipLookup[1].name.startswith(">Not Available<") or not shipLookup[1].killed):
        disable = var.radio1Hidden
        if(disable):
            uiElements.RadioElementsList[2].config(state = DISABLED)
        uiElements.RadioElementsList[1].place(x=uiMetrics.canvasX - 120, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 200)
    
    if(not shipLookup[2].name.startswith(">Not Available<") or not shipLookup[2].killed):
        disable = var.radio2Hidden
        if(disable):
            uiElements.RadioElementsList[2].config(state = DISABLED)
        uiElements.RadioElementsList[2].place(x=uiMetrics.canvasX - 120, y=uiMetrics.canvasY + uiMetrics.canvasHeight + 240)

    canvas.place(x=uiMetrics.canvasX, y=uiMetrics.canvasY)
    staticUi.gameSpeedL.place(x = uiMetrics.gameSpeedLX, y = uiMetrics.gameSpeedLY)
    staticUi.gameSpeedScale.place(x = uiMetrics.gameSpeedSCX, y= uiMetrics.gameSpeedSCY)
    staticUi.timeElapsedLabel.place(x = uiMetrics.timeElapsedLX, y = uiMetrics.timeElapsedLY)
    staticUi.timeElapsedProgressBar.place(x=uiMetrics.timeElapsedPBX, y=uiMetrics.timeElapsedPBY)


    staticUi.exitToMenuBFrame.place(x = uiMetrics.exitBX , y = uiMetrics.exitBY)
    staticUi.startTurnBFrame.place(x = uiMetrics.startTurnBX, y = uiMetrics.startTurnBY)
    staticUi.exitToMenuButton.pack()
    staticUi.startTurnButton.pack()

    staticUi.objectivesLF.place(x=uiMetrics.objectivesLFX, y = uiMetrics.objectivesLFY)
    staticUi.objectivesL.place(x=10, y = 10)

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
        if(len(shieldArray) and tmpShip.maxShields):
            for progressBar in shieldArray:
                progressBar.place(x=tmp + 5, y=5)
                tmp += (((lenGap+lenPro)/lenTotal)/tmpShip.maxShields)*(uiMetrics.systemsLFWidth)
                i+=1

    ######################### ENERGY #################################

    var.uiEnergyLabel.place(x = 10, y = 3) 


    ######################## TARGET CHECKBOX #########################
    updateCheckbox(var,shipLookup,uiElements)
    ########################## SYSTEMS  #######################

    options = var.enemies
    systemOptions = ({"no target" : -1})
    systemOptionsReversed = {}
    targetID = 3
    for enemy in var.enemies.keys():
        if(enemy == shipLookup[var.shipChoice].target):
            break
        targetID+=1
    systemSlots = shipLookup[targetID].systemSlots
    idSystem = 0
    for system in systemSlots:
        systemOptions.update({system.name : idSystem})
        systemOptionsReversed.update({idSystem : system.name})
        idSystem += 1

    ship = shipLookup[var.shipChoice]

    delete = [option for option in options if '>Not Available<' in option]
    for element in delete:
        del options[element]

    ship.shipTarget = StringVar()
    ship.shipTarget.set(ship.target)
    shipTargetSystem = StringVar()

  #  if(len(systemOptions.keys()) == 0):
  #      systemOptions.update({"no target" : -1})
    if(not ship.targetSystem == "no target" and ship.targetSystem >= 0):
        if(ship.targetSystem >= len(systemOptionsReversed)):
            ship.targetSystem = len(systemOptionsReversed) -1
        shipTargetSystem.set(systemOptionsReversed[ship.targetSystem])
    else:
        shipTargetSystem.set("Target system")

    uiElements.optionMenu = tk.OptionMenu(staticUi.systemsLF, ship.shipTarget, *options.keys(),
                              command=lambda _: [shipLookup[var.shipChoice].setTarget(ship.shipTarget),updateBattleUi(shipLookup,uiMetrics,var,root,uiElements,canvas,uiElementsList,multiplayerOptions)])
    
    
    uiElements.systemOptionMenu = tk.OptionMenu(staticUi.systemsLF, 
                                                shipTargetSystem, 
                                                *systemOptions.keys(),
command=lambda _: [shipLookup[var.shipChoice].setTargetSystem(systemOptions[shipTargetSystem.get()]),updateBattleUi(shipLookup,uiMetrics,var,root,uiElements,canvas,uiElementsList,multiplayerOptions)])

    uiElements.optionMenu.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
    uiElements.systemOptionMenu.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
    
    uiElements.viewBFrame = tk.Frame(staticUi.systemsLF)
    uiElements.viewBFrame.config(bg="#4582ec", width=10, height=10,padx=1)
    uiElements.viewButton = tk.Button(uiElements.viewBFrame,text = "Simplified View",
                           state = NORMAL, command = lambda:[viewButtonCommand(var,uiElements.viewButton),updateBattleUi(shipLookup,uiMetrics,var,root,uiElements,canvas,uiElementsList,multiplayerOptions)])
    uiElements.viewButton.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'))
    viewButtonCommand(var, uiElements.viewButton)
    viewButtonCommand(var, uiElements.viewButton)
 
 #   optionMenu.config(bg='#3562a6')
    systemTargetLabel = ttk.Label(staticUi.systemsLF, style = 'SmallGrey.TLabel', text = "Focus\ntarget")
    shipTargetLabel = ttk.Label(staticUi.systemsLF, style = 'SmallGrey.TLabel', text = "Focus\nship")
    
    shipTargetLabel.place(x = 250, y = 0)
    systemTargetLabel.place(x = 620, y = 0)
    uiElements.optionMenu.place(x = 290, y = 0)
    uiElements.systemOptionMenu.place(x = 660, y = 0)
    uiElements.viewBFrame.place(x = 820, y = 0)
    uiElements.viewButton.pack()
    declareSystemsTargets(var,root,shipLookup,staticUi,uiMetrics,ship.shipTarget,uiElements)
    

def handleUpClick(system, scale):
    if system.energy + 1 <= system.maxEnergy:
        scale.set(scale.get() + 1)

def handleDownClick(system, scale):
    if system.energy - 1 >= system.minEnergy:
        scale.set(scale.get() - 1)

def declareSystemsTargets(var,root,shipLookup,staticUi,uiMetrics,shipTarget,uiElements):
    shipChosen = shipLookup[var.shipChoice]
    i=0
    sys1 = 0
    for ship in var.ships:
        ship.optionMenus = []
    uiElements.systemTargetsList = []
    var.uiSystemsAS = []

    for system in shipChosen.systemSlots:
        if (i < 3):
            isDown = 0
        else:
            isDown = 1
        if(i>=len(shipChosen.systemSlots)):
            break
        lf = ttk.LabelFrame(staticUi.systemsLF, style = 'Grey.TLabelframe', text=system.name, height = uiMetrics.systemScalesOffsetY-5, width = uiMetrics.systemScalesWidthOffset)
        lf.place(x = 10 + (i - isDown*3) * (uiMetrics.systemScalesWidthOffset+10), y = uiMetrics.systemScalesMarginTop + uiMetrics.systemScalesOffsetY * isDown )
        frame = tk.Frame(lf, bg = '#4582ec', width = uiMetrics.systemScaleWidth, height = 10, borderwidth=1, highlightbackground="#4582ec")
        scale = tk.Scale(frame, orient=HORIZONTAL, length=uiMetrics.systemScaleWidth, from_ = system.minEnergy, to=system.maxEnergy, relief=FLAT,
                       border = 1,  fg="#4582ec", bg="#4582ec",highlightcolor = "#4582ec",showvalue=1)

        energyLabel = ttk.Label(lf, style = "SmallGrey.TLabel" , text = "Energy")
        energyLabel.place(x = 10, y = 0)

        readinessLabel = ttk.Label(lf, style = "SmallGrey.TLabel" , text = "Readiness")
        readinessLabel.place(x = 10, y = 39)

        system.energyLevelLabel = ttk.Label(lf, style = "Grey.TLabel" , text = "Energy: " + str(system.energy) + '/' + str(system.maxEnergy))
        system.energyLevelLabel.place(x = 180, y = 90)
        
        scale.set(system.energy)
        shipChosen.systemUp = []
        shipChosen.systemDown = []
        if(not system.category == 'module'):
            shipChosen.systemAS = []
            shipChosen.systemDesynchronise = []
            shipChosen.systemHold = []
            shipChosen.systemDelay = []
            if(system.category == 'weapon'):
                system.options = shipLookup[var.enemies[shipTarget.get()]].systemSlots[:]
                noTargetSystem = settings.dynamic_object()
                noTargetSystem.name = 'no target'
                system.options.insert(0, noTargetSystem)
                system.targetDict = {"no target" : -1}
                system.elementID = 1
                system.systemTargets = []
                targetLabel = ttk.Label(lf, style = "SmallGrey.TLabel" , text = "Target")
                for element in system.options:
                    system.systemTargets.append(system.elementID)
                    system.targetDict.update({element.name : system.elementID})
                    system.elementID += 1
                system.variable = StringVar(root)
                if(system.target >= len((list(system.targetDict.keys()))) or system.target < 0):
                    system.target = -1
                    system.variable.set((list(system.targetDict.keys())[0]))
                else:
                    system.variable.set((list(system.targetDict.keys())[system.target + 1]))
                anotherCommand = partial((system.setTarget),(system.targetDict[system.variable.get()]))
                optionMenu = tk.OptionMenu(lf, system.variable, *system.targetDict.keys() , command = anotherCommand)
                optionMenu.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
                shipChosen.optionMenus.append(optionMenu)
                uiElements.systemTargetsList.append(optionMenu)
                system.alphaStrikeVar = IntVar()
                system.alphaStrikeVar.set(system.alphaStrike)
                system.holdVar = IntVar()
                system.holdVar.set(system.hold)
                system.delayVar = IntVar()
                system.delayVar.set(system.delay)
                system.desynchroniseVar = IntVar()
                system.desynchroniseVar.set(system.desynchroniseVar)
                anotherCommand2 = partial(system.setAS)
                anotherCommand3 = partial(system.setHold)
                anotherCommand4 = partial(system.setDelay)
                anotherCommand5 = partial(system.setDesynchronise)     
                shipChosen.systemAS.append(ttk.Checkbutton(lf, text='Synchronise',style = 'Red.TCheckbutton', variable=system.alphaStrikeVar, onvalue=1, offvalue=0, command=anotherCommand2))
                shipChosen.systemDesynchronise.append(ttk.Checkbutton(lf, text='Desynchronise',style = 'Red.TCheckbutton', variable=system.desynchroniseVar, onvalue=1, offvalue=0, command=anotherCommand5))
                shipChosen.systemHold.append(ttk.Checkbutton(lf, text='Hold',style = 'Red.TCheckbutton', variable=system.holdVar, onvalue=1, offvalue=0, command=anotherCommand3))
                shipChosen.systemDelay.append(ttk.Checkbutton(lf, text='Delay',style = 'Red.TCheckbutton', variable=system.delayVar, onvalue=1, offvalue=0, command=anotherCommand4))
                if(var.extendedView):
                    shipChosen.optionMenus[sys1].place(x = 10, y = 82)
                    shipChosen.systemAS[-1].place(x = 180, y = 50)
                    shipChosen.systemDesynchronise[-1].place(x = 180, y = 70)
                    shipChosen.systemHold[-1].place(x = 180, y = 10)
                    shipChosen.systemDelay[-1].place(x = 180, y = 30)
                    targetLabel.place(x = 10, y = 64)
                sys1 += 1
                var.uiSystemsAS.append(shipChosen.systemAS[-1])
                var.uiSystemsAS.append(shipChosen.systemDesynchronise[-1])
                var.uiSystemsAS.append(shipChosen.systemHold[-1])
                var.uiSystemsAS.append(shipChosen.systemDelay[-1])
        if(var.turnInProgress):
            scale.config(state = 'disabled', background="#D0D0D0")
        staticUi.uiSystems.append(scale)
        progressBar = ttk.Progressbar(lf, bootstyle = 'primary', maximum=system.maxCooldown, length=(uiMetrics.systemScaleWidth + 40),variable=(system.maxCooldown-system.cooldown))
        command1 = partial(system.showInfo,'whatever')
        infoBF = tk.Frame(lf)
        infoBF.config(bg="#4582ec", width=2, height=2,padx=1)
        infoButton = tk.Button(infoBF, text = "?", width = 4, height = 1, fg="white", state = NORMAL, command = command1)
        infoButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 11 normal'), highlightbackground="#4582ec")
        staticUi.uiSystemsProgressbars.append(progressBar)

        upF = tk.Frame(lf)
        upF.config(bg="#4582ec", width=2, height=2,padx=1)
        up = tk.Button(upF, text='►', width=2, height=1,command=lambda s=system, sc=scale: handleUpClick(s, sc))
        up.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 8 normal'), highlightbackground="#4582ec")
        shipChosen.systemUp.append(up)

        downF = tk.Frame(lf)
        downF.config(bg="#4582ec", width=2, height=2,padx=1)
        down = tk.Button(downF, text='◄', width=2, height=1,command=lambda s=system, sc=scale: handleDownClick(s, sc))
        down.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 8 normal'), highlightbackground="#4582ec")
        shipChosen.systemDown.append(down)

        frame.place(x = 28, y = 19)
        scale.pack()
        upF.place(x = uiMetrics.systemScaleWidth + 32, y = 19)
        downF.place(x = 10, y = 19)

        shipChosen.systemUp[-1].pack()
        shipChosen.systemDown[-1].pack()

        progressBar.place(x = 10 , y = 55)

        infoBF.place(x=250,y=5)
        infoButton.pack()
        i += 1
    staticUi.systemsLF.place(x = uiMetrics.canvasX, y = uiMetrics.systemsLFY)

    if(not shipLookup[0].name.startswith(">Not Available<")):
        staticUi.playerLF.place(x=20, y = uiMetrics.canvasY)
    if(not shipLookup[1].name.startswith(">Not Available<")):
        staticUi.playerLF2.place(x=20, y = uiMetrics.canvasY + 1 * uiMetrics.canvasHeight/5*2)
    if(not shipLookup[2].name.startswith(">Not Available<")):
        staticUi.playerLF3.place(x=20, y = uiMetrics.canvasY + 2 * uiMetrics.canvasHeight/5*2)
    if(not shipLookup[3].name.startswith(">Not Available<")):
        staticUi.enemyLF.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY)
    if(not shipLookup[4].name.startswith(">Not Available<")):
        staticUi.enemyLF2.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY + 1 * uiMetrics.canvasHeight/5*2)
    if(not shipLookup[5].name.startswith(">Not Available<")):
        staticUi.enemyLF3.place(x=uiMetrics.canvasX + uiMetrics.canvasWidth + 10, y = uiMetrics.canvasY + 2 * uiMetrics.canvasHeight/5*2)


    labelsList = [staticUi.enemyLabels, staticUi.enemyLabels2, staticUi.enemyLabels3, staticUi.playerLabels, staticUi.playerLabels2, staticUi.playerLabels3]
    for target in labelsList:
        i = j = 0
        for element in target:
            if(i<=4 and j == 0):
                element.place(x=10 + i*60,y=30)             # armor and hull
                i+=1
                if(i%5==0):
                    j+=1
                    i=0
            else:
                if(i > 0 and j > 1):
                    element.place(x=75 + i*56,y=50+j*23)        # numbers
                else:
                    if(j == 1 and not i == 0):                  # labels
                        if(i < 3):
                            element.place(x=60 + i*55,y=50+j*23)
                        else:
                            element.place(x=85 + i*50,y=50+j*23)
                    else:
                        element.place(x=3 + i*80,y=50+j*23)
                i+=1
                if(i%6==0):
                    j+=1
                    i=0


def placeMenuUi(root,staticUi,uiMetrics):
    root.title("Main Menu")
    if(settings.combatUiReady):
        staticUi.resumeButton.config(state = NORMAL)
    staticUi.menuCanvas.place(x=0,y=0)
    staticUi.resumeButtonFrame.place(x = uiMetrics.rootX/2, y=550 + 0 * 70, anchor=tk.CENTER)
    staticUi.missionSelectButtonFrame.place(x = uiMetrics.rootX/2, y=550 + 1 * 70, anchor=tk.CENTER)
    staticUi.customGameButtonFrame.place(x = uiMetrics.rootX/2, y=550 + 2 * 70, anchor=tk.CENTER)
    staticUi.multiplayerButtonFrame.place(x = uiMetrics.rootX/2, y=550 + 3 * 70, anchor=tk.CENTER)
    staticUi.shipEditorButtonFrame.place(x = uiMetrics.rootX/2, y=550 + 4 * 70, anchor=tk.CENTER)
    staticUi.exitButtonFrame.place(x = uiMetrics.rootX/2, y=550 + 5 * 70, anchor=tk.CENTER)

    staticUi.resumeButton.pack()
    staticUi.missionSelectButton.pack()
    staticUi.shipEditorButton.pack()
    staticUi.customGameButton.pack()
    staticUi.multiplayerButton.pack()
    staticUi.exitButton.pack()


def placeShipEditorUi(staticUi,uiMetrics):
    staticUi.systemStatsLF.place(x=500,y=40)
    staticUi.systemStatsL.place(x=10,y=10)
    staticUi.shipChoice.place(x=100,y=50)
    staticUi.shipNameInput.place(x=100,y=100)
    staticUi.shipStatsLF.place(x=1000,y=40)
    staticUi.shipStatsL.place(relx = 0.1, rely = 0.0)

    staticUi.engineChoiceMenuLF.place(x=100,y=uiMetrics.editorChoiceMenuY)
    staticUi.thrustersChoiceMenuLF.place(x=100,y=uiMetrics.editorChoiceMenuY + uiMetrics.editorChoiceMenuOffset)
    staticUi.radarChoiceMenuLF.place(x=100,y=uiMetrics.editorChoiceMenuY + 2 * uiMetrics.editorChoiceMenuOffset)
    staticUi.generatorChoiceMenuLF.place(x=100,y=uiMetrics.editorChoiceMenuY + 3 * uiMetrics.editorChoiceMenuOffset)

    staticUi.engineChoiceMenuL.place(x = uiMetrics.editorSystemsLOffsetX, y = 0)
    staticUi.thrustersChoiceMenuL.place(x = uiMetrics.editorSystemsLOffsetX, y = 0)
    staticUi.radarChoiceMenuL.place(x = uiMetrics.editorSystemsLOffsetX, y = 0)
    staticUi.generatorChoiceMenuL.place(x = uiMetrics.editorSystemsLOffsetX, y = 0)

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
    
    (staticUi.systemChoiceL0).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY)
    (staticUi.systemChoiceL1).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL2).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL3).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL4).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.systemChoiceL5).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    
    (staticUi.subsystemChoiceMenu1).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY)
    (staticUi.subsystemChoiceMenu2).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu3).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu4).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu5).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu6).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu7).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 6 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceMenu8).place(x=uiMetrics.editorSystemsX, y = uiMetrics.editorSystemsY + 7 * uiMetrics.editorSystemsYOffset)
    
    (staticUi.subsystemChoiceL1).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY)
    (staticUi.subsystemChoiceL2).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL3).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 2 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL4).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 3 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL5).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 4 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL6).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 5 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL7).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 6 * uiMetrics.editorSystemsYOffset)
    (staticUi.subsystemChoiceL8).place(x=uiMetrics.editorSystemsX + uiMetrics.editorSystemsLOffsetX, y = uiMetrics.editorSystemsY + 7 * uiMetrics.editorSystemsYOffset)
    
    (staticUi.saveShipButtonF).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY)
    (staticUi.completeButtonF).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY + 60)
    (staticUi.clearButtonF).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY + 120)
    (staticUi.exitToMenuButtonF).place(x=uiMetrics.editorSaveButtonX, y = uiMetrics.editorSaveButtonY - 160)
    
    staticUi.saveShipButton.pack()
    staticUi.completeButton.pack()
    staticUi.clearButton.pack()
    staticUi.exitToMenuButton.pack()


def placeCustomGameUi(staticUi,uiMetrics,multiplayer): 
    staticUi.blueShipLF0.place(x=uiMetrics.cgBlueShipX,y=uiMetrics.cgBlueShipY)
    staticUi.blueShipLF1.place(x=uiMetrics.cgBlueShipX,y=uiMetrics.cgBlueShipY + uiMetrics.cgShipYoffset)
    staticUi.blueShipLF2.place(x=uiMetrics.cgBlueShipX,y=uiMetrics.cgBlueShipY + uiMetrics.cgShipYoffset * 2)
    if(not multiplayer.multiplayerGame):
        staticUi.redShipLF0.place(x=uiMetrics.cgRedShipX,y=uiMetrics.cgBlueShipY)
        staticUi.redShipLF1.place(x=uiMetrics.cgRedShipX,y=uiMetrics.cgBlueShipY + uiMetrics.cgShipYoffset)
        staticUi.redShipLF2.place(x=uiMetrics.cgRedShipX,y=uiMetrics.cgBlueShipY + uiMetrics.cgShipYoffset * 2)

    staticUi.blueShipOM0F.place(x=10,y=10)
    staticUi.blueShipOM1F.place(x=10,y=10)
    staticUi.blueShipOM2F.place(x=10,y=10)
    staticUi.blueShipOM0.pack()
    staticUi.blueShipOM1.pack()
    staticUi.blueShipOM2.pack()
    
    staticUi.costLBlue.place(x = uiMetrics.cgBlueShipX, y = uiMetrics.cgBlueShipY - 60)
    staticUi.massLBlue.place(x = uiMetrics.cgBlueShipX, y = uiMetrics.cgBlueShipY - 40)
    if(not multiplayer.multiplayerGame):
        staticUi.costLRed.place(x = uiMetrics.cgRedShipX, y = uiMetrics.cgBlueShipY - 60)
        staticUi.massLRed.place(x = uiMetrics.cgRedShipX, y = uiMetrics.cgBlueShipY - 40)
        staticUi.redShipOM0F.place(x=10,y=10)
        staticUi.redShipOM1F.place(x=10,y=10)
        staticUi.redShipOM2F.place(x=10,y=10)
        staticUi.redShipOM0.pack()
        staticUi.redShipOM1.pack()
        staticUi.redShipOM2.pack()
        staticUi.startGameBF.place(x=775,y=uiMetrics.cgStartButton)
        staticUi.startGameButton.pack()
        staticUi.mapLF.place(x=uiMetrics.cgMapChoiceX,y=uiMetrics.cgMapChoiceY)
        staticUi.mapOMF.place(x=10,y=10)
        staticUi.mapOM.pack()
        staticUi.foWLF.place(x=uiMetrics.cgMapChoiceX,y=uiMetrics.cgMapChoiceY+100)
        staticUi.foWCB.place(x=10,y=10)
        staticUi.swapCB.place(x=10,y=40)
        staticUi.missionCanvas.place(x=uiMetrics.cgCanvasX,y=10)
    else:
        if(multiplayer.side == 'server'):
            staticUi.startGameBF.place(x=775,y=uiMetrics.cgStartButton)
            staticUi.startGameButton.pack()
            staticUi.mapLF.place(x=uiMetrics.cgMapChoiceX,y=uiMetrics.cgMapChoiceY)
            staticUi.mapOMF.place(x=10,y=10)
            staticUi.mapOM.pack()
            staticUi.foWLF.place(x=uiMetrics.cgMapChoiceX,y=uiMetrics.cgMapChoiceY+100)
            staticUi.foWCB.place(x=10,y=10)
            staticUi.swapCB.place(x=10,y=40)
            staticUi.missionCanvas.place(x=uiMetrics.cgCanvasX,y=10)
        else:
            staticUi.startGameBF.place(x=775,y=uiMetrics.cgStartButton)
            staticUi.startGameButton.pack()

    staticUi.exitToMenuBF.place(x=975, y = uiMetrics.cgStartButton)
    staticUi.exitToMenuButton.pack()
    
def placeSelectMenuUI(staticUi,uiMetrics):

    staticUi.levelOptionMenu.place(x=40,y=100)


    staticUi.startBFrame.place(x=40,y=150)
    staticUi.exitToMenuBFrame.place(x=uiMetrics.msCanvasX + uiMetrics.msCanvasWidth + 40, y=uiMetrics.msCanvasY)


    staticUi.startB.pack()
    staticUi.exitToMenuButton.pack()

    staticUi.desLabelFrame.place(x=440,y=600)

    i = 0
    staticUi.cryptonymLF.place(x=40,y=250)
    i+=1
    staticUi.dateLF.place(x=40,y=250 + i * 70)
    i+=1
    staticUi.unitLF.place(x=40,y=250 + i * 70)
    i+=2
    staticUi.reconLF.place(x=40,y=250 + i * 70)
    i+=1
    staticUi.codeLF.place(x=40,y=250 + i * 70)
    i+=1
    staticUi.threatLF.place(x=40,y=250 + i * 70)
    i+=1
    staticUi.objLabelFrame.place(x=40,y=250 + i * 70)

    (staticUi.missionCanvas).place(x=uiMetrics.msCanvasX, y=uiMetrics.msCanvasY)