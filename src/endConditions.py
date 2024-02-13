
from tkinter import *
import tkinter.ttk as ttk

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
            window = Toplevel()
            window.config(bg="#202020", width = 600, height = 600)
            label = ttk.Label(window, style = "Grey.TLabel", text='You Won\n\n'+ var.winMessage+'\n\nPress "Exit to Menu" to continue')
            label.config(justify='center')
            label.pack()
            events.showedWin = True

    if(var.winByEliminatingPlayer):
        if (noPlayers and not gameEnded):
            window = Toplevel()
            window.config(bg="#202020", width = 600, height = 600)
            label = ttk.Label(window, style = "Grey.TLabel", text='You Lost\n\n'+ var.winMessage+'\n\nPress "Exit to Menu" to continue')
            label.config(justify='center')
            label.pack()
            events.showedWin = True
        
    if(var.looseByEliminatingPlayer):
        if (noPlayers and not gameEnded):
            window = Toplevel()
            window.config(bg="#202020", width = 600, height = 600)
            label = ttk.Label(window, style = "Grey.TLabel", text='You Lost\n\n'+ var.looseMessage+'\n\nPress "Exit to Menu" to continue')
            label.config(justify='center')
            label.pack()
            events.showedLoose = True

    print("loose by eli" + str(var.looseByEliminatingEnemy)  ) 
    if(var.looseByEliminatingEnemy):
        if (noEnemies and not gameEnded):
            print("test " + str(var.looseByEliminatingPlayer))
            window = Toplevel()
            window.config(bg="#202020", width = 600, height = 600)
            label = ttk.Label(window, style = "Grey.TLabel", text='You Lost\n\n'+ var.looseMessage+'\n\nPress "Exit to Menu" to continue')
            label.config(justify='center')
            label.pack()
            events.showedLoose = True


def disabledShips(var,events):
 #   if(events.disabledWin or events.disabledLoose or var.looseByDisablingPlayer or var.winByDisablingPlayer or var.winByDisablingEnemy or var.looseByDisablingEnemy):
 #       return
    ships = var.ships
    gameEnded = ((events.showedLoose) or events.showedWin)
    disabledEnemy = True
    disabledPlayer = True
    for ship in ships:
        ship.disabled = True
        for system in ship.systemSlots:
            if(system.integrity > 0):
                ship.disabled = False
                break
    for ship in ships:
        if(ship.owner == 'player1' and not ship.disabled):
            events.disabledPlayer = False
            break
    for ship in ships:
  #      print(ship.name + str(ship.disabled))
        if(ship.owner == 'ai1' and not ship.disabled):
            events.disabledEnemy = False
            break
    if(var.looseByDisablingPlayer):
        print("var.looseByDisablingPlayer")
        if (disabledPlayer and not gameEnded):
            window = Toplevel()
            window.config(bg="#202020", width = 600, height = 600)
            label = ttk.Label(window, style = "Grey.TLabel", text='You Lost\n\n'+ var.looseMessage+'\n\nPress "Exit to Menu" to continue')
            label.config(justify='center')
            label.pack()
            events.showedLoose = True

    if(var.winByDisablingPlayer):
        print("var.winByDisablingPlayer")
        if (disabledPlayer and not gameEnded):
            window = Toplevel()
            window.config(bg="#202020", width = 600, height = 600)
            label = ttk.Label(window, style = "Grey.TLabel", text='You Won\n\n'+ var.winMessage+'\n\nPress "Exit to Menu" to continue')
            label.config(justify='center')
            label.pack()
            events.showedWin = True

    if(var.looseByDisablingEnemy):
        print("loose enemyt")
        if (disabledEnemy and not gameEnded):
            window = Toplevel()
            window.config(bg="#202020", width = 600, height = 600)
            label = ttk.Label(window, style = "Grey.TLabel", text='You Lost\n\n'+ var.looseMessage+'\n\nPress "Exit to Menu" to continue')
            label.config(justify='center')
            label.pack()
            events.showedLoose = True

    if(var.winByDisablingEnemy):
        print("win enemyt")
        if (disabledEnemy and not gameEnded):
            window = Toplevel()
            window.config(bg="#202020", width = 600, height = 600)
            label = ttk.Label(window, style = "Grey.TLabel", text='You Won\n\n'+ var.winMessage+'\n\nPress "Exit to Menu" to continue')
            label.config(justify='center')
            label.pack()
            events.showedWin = True