from tkinter import *
import tkinter.ttk as ttk
import src.loadGame as loadGame

def killedShips(var,events):
    noEnemies = True
    noPlayers = True
    gameEnded = ((events.showedLoose) or events.showedWin)
    for ship in var.ships:
        if(not ship.owner == "player1" and not ship.killed):
            noEnemies = False
        elif(ship.owner == "player1" and not ship.killed):
            noPlayers = False
    if(var.winByEliminatingEnemy):
        if (noEnemies and not gameEnded):
            var.wonByEliminatingEnemy = True

    if(var.winByEliminatingPlayer):
        if (noPlayers and not gameEnded):
            var.wonByEliminatingPlayer = True
        
    if(var.looseByEliminatingPlayer):
        if (noPlayers and not gameEnded):
            var.lostByEliminatingPlayer = True

    if(var.looseByEliminatingEnemy):
        if (noEnemies and not gameEnded):
            var.lostByEliminatingEnemy = True


def disabledShips(var,events):
 #   if(events.disabledWin or events.disabledLoose or var.looseByDisablingPlayer or var.winByDisablingPlayer or var.winByDisablingEnemy or var.looseByDisablingEnemy):
 #       return
    ships = var.ships
    gameEnded = ((events.showedLoose) or events.showedWin)
    disabledEnemy = True
    disabledPlayer = True
    setattr(var, f"wonByDisabling0", True)
    setattr(var, f"wonByDisabling1", True)
    setattr(var, f"wonByDisabling2", True)
    setattr(var, f"wonByDisabling3", True)
    setattr(var, f"wonByDisabling4", True)
    setattr(var, f"wonByDisabling5", True)

    setattr(var, f"lostByDisabling0", False)
    setattr(var, f"lostByDisabling1", False)
    setattr(var, f"lostByDisabling2", False)
    setattr(var, f"lostByDisabling3", False)
    setattr(var, f"lostByDisabling4", False)
    setattr(var, f"lostByDisabling5", False)

    for ship in ships:
        ship.disabled = True
        for system in ship.systemSlots:
            if(system.integrity > 0):
                setattr(var, f"wonByDisabling{ship.id}", False)
                setattr(var, f"lostByDisabling{ship.id}", False)
                ship.disabled = False
                break
    for ship in ships:
        if(ship.owner == 'player1' and not ship.disabled):
            disabledPlayer = False
            break
    for ship in ships:
  #      print(ship.name + str(ship.disabled))
        if(ship.owner == 'ai1' and not ship.disabled):
            disabledEnemy = False
            break

    if(var.winByDisablingPlayer):
        if (disabledPlayer and not gameEnded):
            var.wonByDisablingPlayer = True

    if(var.winByDisablingEnemy):
        if (disabledEnemy and not gameEnded):
            var.wonByDisablingEnemy = True

    if(var.looseByDisablingPlayer):
        if (disabledPlayer and not gameEnded):
            var.lostByDisablingPlayer = True

    if(var.looseByDisablingEnemy):
        if (disabledEnemy and not gameEnded):
            var.lostByDisablingEnemy = True
    

def foundLandmarks(var,events):
    gameEnded = ((events.showedLoose) or events.showedWin)
    if(var.winBySeeingLandmarks):
        noInvisibleLandmarks = True
        for landmark in var.landmarks:
            if(not landmark.visible):
                noInvisibleLandmarks = False
                break
        if (noInvisibleLandmarks and not gameEnded):
            var.wonBySeeingLandmarks = True 


def showWin(var,events):
    gameEnded = ((events.showedLoose) or events.showedWin)

    arr = [var.winByEliminatingPlayer, var.winByEliminatingEnemy \
    ,var.winByEliminating0
    ,var.winByEliminating1
    ,var.winByEliminating2
    ,var.winByEliminating3
    ,var.winByEliminating4
    ,var.winByEliminating5]

    arr2 = [var.wonByEliminatingPlayer, var.wonByEliminatingEnemy \
    ,var.wonByEliminating0
    ,var.wonByEliminating1
    ,var.wonByEliminating2
    ,var.wonByEliminating3
    ,var.wonByEliminating4
    ,var.wonByEliminating5]

    elimWin = True
    for arg,arg2 in zip(arr,arr2):
        if((not arg) or arg2):
            continue
        else:
            elimWin = False
            break

    arr = [var.winByDisablingPlayer, var.winByDisablingEnemy \
            ,var.winByDisabling0
            ,var.winByDisabling1
            ,var.winByDisabling2
            ,var.winByDisabling3
            ,var.winByDisabling4
            ,var.winByDisabling5]
    
    arr2 = [var.wonByDisablingPlayer, var.wonByDisablingEnemy\
            ,var.wonByDisabling0
            ,var.wonByDisabling1
            ,var.wonByDisabling2
            ,var.wonByDisabling3
            ,var.wonByDisabling4
            ,var.wonByDisabling5]

    disWin = True
    for arg,arg2 in zip(arr,arr2):
        if(not arg or arg2):
            continue
        else:
            disWin = False
            break

    landmarkWin = var.wonBySeeingLandmarks or not var.winBySeeingLandmarks
    if((disWin and elimWin and landmarkWin) and not gameEnded):
        window = Toplevel()
        window.config(bg="#202020", width = 600, height = 600)
        label = ttk.Label(window, style = "Grey.TLabel", text='You Won\n\n'+ var.winMessage+'\n\nPress "Exit to Menu" to continue')
        label.config(justify='center')
        label.pack()
        events.showedWin = True


def showLoose(var,events):
    gameEnded = ((events.showedLoose) or events.showedWin)


    arr = [var.looseByEliminatingPlayer, var.looseByEliminatingEnemy \
    ,var.looseByEliminating0
    ,var.looseByEliminating1
    ,var.looseByEliminating2
    ,var.looseByEliminating3
    ,var.looseByEliminating4
    ,var.looseByEliminating5]

    arr2 = [var.lostByEliminatingPlayer, var.lostByEliminatingEnemy \
    ,var.lostByEliminating0
    ,var.lostByEliminating1
    ,var.lostByEliminating2
    ,var.lostByEliminating3
    ,var.lostByEliminating4
    ,var.lostByEliminating5]

    elimLoose = False
    for arg,arg2 in zip(arr,arr2):
        if(arg and arg2):
            elimLoose = True
            break

    arr = [var.looseByDisablingPlayer, var.looseByDisablingEnemy \
            ,var.looseByDisabling0
            ,var.looseByDisabling1
            ,var.looseByDisabling2
            ,var.looseByDisabling3
            ,var.looseByDisabling4
            ,var.looseByDisabling5]
    
    arr2 = [var.lostByDisablingPlayer, var.lostByDisablingEnemy\
            ,var.lostByDisabling0
            ,var.lostByDisabling1
            ,var.lostByDisabling2
            ,var.lostByDisabling3
            ,var.lostByDisabling4
            ,var.lostByDisabling5]

    disLoose = False
    for arg,arg2 in zip(arr,arr2):
        if(arg and arg2):
            disLoose = True
            break

    if((disLoose or elimLoose) and not gameEnded):
        window = Toplevel()
        window.config(bg="#202020", width = 600, height = 600)
        label = ttk.Label(window, style = "Grey.TLabel", text='You Lost\n\n'+ var.looseMessage+'\n\nPress "Exit to Menu" to continue')
        label.config(justify='center')
        label.pack()
        button = ttk.Button(window, style = "Grey.TButton", text='Replay',command = loadGame.run())
        events.showedLoose = True

