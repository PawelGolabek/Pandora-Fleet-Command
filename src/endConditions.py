
from tkinter import *
import tkinter.ttk as ttk

def killedShips(var,events):
    noEnemies = True
    noPlayers = True
    for ship in var.ships:
   #     print("id" + str(ship.id))
        if(not ship.owner == "player1" and not ship.killed):
            noEnemies = False
        elif(ship.owner == "player1" and not ship.killed):
            noPlayers = False
    if (noEnemies and not events.showedWin):
        window = Toplevel()
        window.config(bg="#202020", width = 600, height = 600)
        label = ttk.Label(window, style = "Grey.TLabel", text='You Won\n\n'+ var.winMessage+'\n\nPress "Exit to Menu" to continue')
        label.config(justify='center')
        label.pack()
        events.showedWin = True
    if (noPlayers and not events.showedLoose):
        window = Toplevel()
        window.config(bg="#202020", width = 600, height = 600)
        label = ttk.Label(window, style = "Grey.TLabel", text='You Lost\n\n'+ var.looseMessage+'\n\nPress "Exit to Menu" to continue')
        label.config(justify='center')
        label.pack()
        events.showedLoose = True


def disabledShips(var,events):
    if(events.disabledWin or events.disabledLoose):
        return
    ships = var.ships
    events.disabledWin = True
    events.disabledLoose = True
    for ship in ships:
        ship.disabled = True
        for system in ship.systemSlots:
            if(system.integrity):
                ship.disabled = False
    for ship in ships:
        if(ship.owner == 'player1' and not ship.disabled):
            events.disabledLoose = False
            break
    for ship in ships:
        if(ship.owner == 'ai1' and not ship.disabled):
            events.disabledWin = False
            break
    if (events.disabledWin and not events.showedWin):
        window = Toplevel()
        window.config(bg="#202020", width = 600, height = 600)
        label = ttk.Label(window, style = "Grey.TLabel", text='You Won\n\n'+ var.winMessage+'\n\nPress "Exit to Menu" to continue')
        label.config(justify='center')
        label.pack()
        events.showedWin = True
    if (events.disabledLoose and not events.showedLoose):
        window = Toplevel()
        window.config(bg="#202020", width = 600, height = 600)
        label = ttk.Label(window, style = "Grey.TLabel", text='You Lost\n\n'+ var.looseMessage+'\n\nPress "Exit to Menu" to continue')
        label.config(justify='center')
        label.pack()
        events.showedLoose = True