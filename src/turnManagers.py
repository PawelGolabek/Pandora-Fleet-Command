import tkinter as tk
import tkinter.ttk as ttk
from tkinter import DISABLED, NORMAL
from ctypes import pointer
from dis import dis
from ensurepip import bootstrap
from faulthandler import disable
from tkinter.filedialog import askopenfilename
#from src.update import update
import configparser
import copy
import json
import pickle

import src.canvasCalls as canvasCalls
import src.settings as settings
import src.endConditions as endConditions
from src.shipCombat import detectionCheck,updateLabels,getOrders,newWindow,updateShields
from src.aiControllers import aiController
from src.multiplayer.otherCommands import encodeChoices, decodeChoices


def sendDataInChunks(client_socket, data):
    configDict = {section: dict(data[section]) for section in data.sections()}
    #Convert the Python dictionary into JSON format using json module
    configJson = json.dumps(configDict, indent=4)
    data = configJson.encode()
    bytes_sent = 0
    chunk_size = 4096
    chunksToSend = 8
    while chunksToSend > 0:
        chunk = data[bytes_sent:bytes_sent + chunk_size]
        client_socket.send(chunk)
        bytes_sent += len(chunk)
        chunksToSend -= 1


def receiveDataInChunks(server_socket):
    chunkSize = 4096  # You should use the same chunk size as on the server side
    chunks = 8
    received_data = b""
    while chunks > 0:
        chunk = server_socket.recv(chunkSize)
        received_data += chunk
        chunks -= 1
        print(chunk)
    return received_data

def startTurn(uiElements,var,ships,gameRules,uiMetrics,multiplayerOptions,root):
    if(not var.turnInProgress):
        if(var.debugging):
            print("New Round")
        uiElements.startTurnButton.config(state = DISABLED)
        uiElements.exitToMenuButton.config(state = DISABLED)
        uiElements.viewButton.config(state = DISABLED)
        uiElements.timeElapsedProgressBar['value'] = 0
        for object in uiElements.UIElementsList:
            object.config(state=tk.DISABLED, background="#D0D0D0")
        for object in uiElements.RadioElementsList:
            object.config(state=tk.DISABLED)
        for object in uiElements.uiSystems:
            object.config(state = tk.DISABLED, background="#D0D0D0")
        for object in var.uiSystemsAS:
            object.config(state = tk.DISABLED, style = 'Disabled.TCheckbutton')
        for ship in var.ships:
            for element in ship.optionMenus:
                element.config(fg="#4F4F4F", state = DISABLED)
        uiElements.optionMenu.config(fg="#4F4F4F", state = DISABLED)
        uiElements.systemOptionMenu.config(fg="#4F4F4F", state = DISABLED)
        if(not multiplayerOptions.multiplayerGame):
            var.turnInProgress = True
        else:
            root.title("Waiting for another player")
            multiplayerOptions.waitingForOtherPlayer = True
            if(multiplayerOptions.side == 'client'):
                configOut = encodeChoices(var,multiplayerOptions)
                multiplayerOptions.clientSocket.send(pickle.dumps(configOut))
                config = configparser.ConfigParser()
                config = multiplayerOptions.clientSocket.recv(65536)
                multiplayerOptions.clientSocket.recv(0)
                print(config)
                config = pickle.loads(config)
            #    config.load(config_data
            else:
                config = configparser.ConfigParser()
                config = multiplayerOptions.clientSocket.recv(65536)
                multiplayerOptions.serverSocket.recv(0)
                configOut = encodeChoices(var,multiplayerOptions)
                multiplayerOptions.clientSocket.send(pickle.dumps(configOut))
                print(config)
                config = pickle.loads(config)
            


            decodeChoices(var, config)
    #        FlushListen(multiplayerOptions.clientSocket)
            var.turnInProgress = True
            # wait and get everything from server or client. On receiving start turn

def endTurn(uiElements,var,gameRules,uiMetrics,canvas,ammunitionType,uiIcons,shipLookup,root,multiplayerOptions): 
    var.turnInProgress = False
    uiElements.startTurnButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 10 normal'), highlightbackground="#4582ec", state = NORMAL)
    uiElements.exitToMenuButton.config(background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 10 normal'), highlightbackground="#4582ec", state = NORMAL)
    uiElements.viewButton.config(fg = "white",state = NORMAL)
    for object in uiElements.UIElementsList:
        object.config(state = NORMAL, bg="#4582ec",highlightcolor = "white",fg = "white",highlightbackground = "#bfbfbf")
    if(not var.radio0Hidden):
        uiElements.RadioElementsList[0].config(state = NORMAL)
    if(not var.radio1Hidden):
        uiElements.RadioElementsList[1].config(state = NORMAL)
    if(not var.radio2Hidden):
        uiElements.RadioElementsList[2].config(state = NORMAL)
    for object in uiElements.uiSystems:
        object.config(state = NORMAL, bg="#4582ec",highlightcolor = "white")
    for object in var.uiSystemsAS:
        object.config(state = NORMAL, style = 'Red.TCheckbutton')
    uiElements.gameSpeedScale.config(bg="#4582ec",highlightcolor = "white",fg = "white")
    for ship in var.ships:
        ship.ghostPoints = []
    uiElements.optionMenu.config(fg="#bfbfbf", state = NORMAL)
    uiElements.systemOptionMenu.config(fg="#bfbfbf", state = NORMAL)
    if(not multiplayerOptions.multiplayerGame):
        for ship in var.ships:
            for element in ship.optionMenus:
                element.config(fg="#bfbfbf", state = NORMAL)
            if(ship.owner == "ai1"):
                aiController.moveOrderChoice(ship,var.ships,var,gameRules,uiMetrics)
                aiController.systemChoice(ship,var.ships,shipLookup)
    for ship in var.ships:
        getOrders(ship,var,gameRules,uiMetrics,True)
    var.updateTimer = 3
    newWindow(uiMetrics,var,canvas,root)
    detectionCheck(var,uiMetrics)
    canvasCalls.drawShips(canvas,var,uiMetrics)
    canvasCalls.drawGhostPoints(canvas,var)
    canvasCalls.drawSignatures(canvas,var)
    canvasCalls.drawLandmarks(var,canvas,uiIcons,uiMetrics)
    canvasCalls.drawLasers(var,canvas,uiMetrics)
    canvasCalls.drawRockets(var,ammunitionType,canvas)
    updateShields(var.ships,var)
    updateLabels(uiElements,shipLookup,var,root)
    if(multiplayerOptions.multiplayerGame):
        multiplayerOptions.waitingForOtherPlayer = False
        if(multiplayerOptions.side == 'server'):
          #  sendEverythingToClient ...
          x=120
        else:
            # get everything from server ...
            x=10
