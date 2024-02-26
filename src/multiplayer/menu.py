import configparser
import sys,os
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from pathlib import Path
import socket

from src.rootCommands import hideMultiplayerMenuUi,placeMultiplayerMenuUi, showClientOptions
from src.customGameMenu import customGame
from src.settings import dynamic_object
from src.multiplayer.netCommands import get_local_ip

def listenForClient(root,statusLabel,config,uiMenuElements,uiMetrics,multiplayerOptions):
    statusLabel.config(text = "Awaiting the client to join ... \n Your local IP adress: " + get_local_ip())
    root.update()
    # Create a socket object
    multiplayerOptions.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the host and port
    host = '0.0.0.0'
    port = 12345
    # Bind the socket to a specific address and port
    multiplayerOptions.serverSocket.bind((host, port))
    # Listen for incoming connections
    multiplayerOptions.serverSocket.listen(1)
    print('Server listening on {}:{}'.format(host, port))
    # Accept a client connection
    multiplayerOptions.clientSocket, addr = multiplayerOptions.serverSocket.accept()
    print('Connected to client:', addr)
    # Receive data from the client
    data = multiplayerOptions.clientSocket.recv(1024).decode()
    print('Received data:', data)
    # Process the received data (you can add your own logic here)
    # In this example, we'll convert the data to uppercase
    response = "Welcome, client"
    # Send a response back to the client
    multiplayerOptions.clientSocket.send(response.encode())

    multiplayerOptions.multiplayerGame = True
    multiplayerOptions.side = "server"
    multiplayerOptions.statusLabel = statusLabel

    customGame(root,config,uiMenuElements,uiMetrics,multiplayerOptions)

    # Close the socket (dont, do it after game ends)
    multiplayerOptions.clientSocket.close()
    multiplayerOptions.serverSocket.close()
    
    # find someone, stop searching
    # send him your set and he sends you his
    # server decides who is blue who is red?
    # create a game with player2 ships as enemy. Supress ai commands with wait for player2
    # when server gets orders and ready start simulating on server and on client.
    # after simulation ends on server send it to player2. Overwrite whatever happened on player2 with server results. (Optional: If drastically different write synchronisation or sth)
    # play until win
    # disconnect and closeimport socket



def joinHost(hostIP,root, statusLabel,config,uiMenuElements,uiMetrics,uiElements,multiplayerOptions):
    # Create a socket object
    multiplayerOptions.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the host and port to connect to
    host = hostIP
    port = 12345
    # Connect to the server
    try:
        multiplayerOptions.clientSocket.connect((host, port))
        # Send data to the server
        data = 'Client joined!'
        multiplayerOptions.clientSocket.send(data.encode())
        # Receive the response from the server
        response = multiplayerOptions.clientSocket.recv(1024).decode()
        print('Response from server:', response)

        multiplayerOptions.multiplayerGame = True
        multiplayerOptions.side = "client"
        multiplayerOptions.statusLabel = statusLabel

        statusLabel.place_forget()
       # uiElements.IPlabel.place_forget()
        customGame(root,config,uiMenuElements,uiMetrics,multiplayerOptions)

    except:
        statusLabel.config(text = "Couldn't find a server")
        showClientOptions(uiElements)
        return
    

    # custom game with multiplayer client side

    # Close the socket (dont, do it after game ends)
    multiplayerOptions.clientSocket.close()


def copy_text(root, label):
    text = label.cget("text")    
    text = text[:0] + text[43:]
    print(text)
    root.clipboard_clear()  # Clear the clipboard contents
    root.clipboard_append(text)  # Append the specified text to the clipboard
    root.update()  # Update the clipboard
    return 


def on_entry_click(entry):
    if entry.get() == "Insert Host IP Address":
        entry.delete(0, tk.END)

def on_entry_leave(entry):
    if entry.get() == '':
        entry.insert(0, "Insert Host IP Address") 
        
def hideClientOptions(clientElements):
    for element in clientElements:
        element.place_forget()

def hideHostOptions(hostElements):
    for element in hostElements:
        element.place_forget()


def multiplayerMenu(root,config,uiMenuElements,uiMetrics,multiplayerOptions):
    multiplayerMenuUi = dynamic_object()
    multiplayerMenuUi.hostBFrame = tk.Frame(root)
    multiplayerMenuUi.hostBFrame.config(bg="#4582ec", width=2, height=2,padx=1)

    multiplayerMenuUi.hostGameButton = tk.Button(multiplayerMenuUi.hostBFrame, text = "Host a new game",
        command = lambda:[hideMultiplayerMenuUi(multiplayerMenuUi),customGame(root,config,uiMenuElements,uiMetrics,True,True)])
    multiplayerMenuUi.hostGameButton.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 14 normal'), highlightbackground="#4582ec", width = 14, height = 2)

    multiplayerMenuUi.clientBFrame = tk.Frame(root)
    multiplayerMenuUi.clientBFrame.config(bg="#4582ec", width=2, height=2,padx=1)

    multiplayerMenuUi.clientGameButton = tk.Button(multiplayerMenuUi.clientBFrame, text = "Join a game",
        command = lambda:[hideMultiplayerMenuUi(multiplayerMenuUi),customGame(root,config,uiMenuElements,uiMetrics,True,False)])   
    multiplayerMenuUi.clientGameButton.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 14 normal'), highlightbackground="#4582ec", width = 14, height = 2)

    

    multiplayerMenuUi.IPEntry = ttk.Entry(root, style = 'GreyBig.TEntry', text = "Insert IP adress of a host")
    multiplayerMenuUi.IPEntry.configure(background='#1e1e1e',foreground = "#000000",justify='center',font= ('Calibri', 20))

    multiplayerMenuUi.statusLabel = ttk.Label(root, style = 'GreyBig.TLabel', text = ("Or host a new game:\nYour local IP Address: "+ get_local_ip()))

    multiplayerMenuUi.copyIPBFrame = tk.Frame(root)
    multiplayerMenuUi.copyIPBFrame.config(bg="#4582ec", width=2, height=2,padx=1)

    multiplayerMenuUi.copyIPB = tk.Button(multiplayerMenuUi.copyIPBFrame, text = "Copy", command = lambda:[copy_text(root, multiplayerMenuUi.statusLabel)])
    multiplayerMenuUi.copyIPB.config(background='#1a1a1a',fg="white",relief="ridge", font=('Calibri 14 normal'), highlightbackground="#4582ec", width = 14, height = 2)

    multiplayerMenuUi.IPEntry.insert(0, "Insert Host IP Address")
    multiplayerMenuUi.IPEntry.bind("<Button-1>",  lambda event: on_entry_click(multiplayerMenuUi.IPEntry))
    multiplayerMenuUi.IPEntry.bind("<FocusOut>",  lambda event: on_entry_leave(multiplayerMenuUi.IPEntry))

    hostOptions = []
    hostOptions.append(multiplayerMenuUi.IPEntry)
    hostOptions.append(multiplayerMenuUi.hostBFrame)
    hostOptions.append(multiplayerMenuUi.clientBFrame)
    hostOptions.append(multiplayerMenuUi.copyIPBFrame)
    

    clientOptions = []
    clientOptions.append(multiplayerMenuUi.IPEntry)
    clientOptions.append(multiplayerMenuUi.hostBFrame)
    clientOptions.append(multiplayerMenuUi.clientBFrame)
    clientOptions.append(multiplayerMenuUi.copyIPBFrame)

    multiplayerMenuUi.hostGameButton.config(command = lambda:[hideHostOptions(hostOptions),listenForClient(root, multiplayerMenuUi.statusLabel,config,uiMenuElements,uiMetrics,multiplayerOptions)])
    multiplayerMenuUi.clientGameButton.config(command = lambda:[hideClientOptions(clientOptions),joinHost(multiplayerMenuUi.IPEntry.get(),root, multiplayerMenuUi.statusLabel,config,uiMenuElements,uiMetrics,multiplayerMenuUi,multiplayerOptions)])

    multiplayerMenuUiList = []
    multiplayerMenuUiList.append(multiplayerMenuUi.hostBFrame)
    multiplayerMenuUiList.append(multiplayerMenuUi.clientBFrame)
    multiplayerMenuUiList.append(multiplayerMenuUi.hostGameButton)
    multiplayerMenuUiList.append(multiplayerMenuUi.clientGameButton)
    multiplayerMenuUiList.append(multiplayerMenuUi.IPEntry)
    multiplayerMenuUiList.append(multiplayerMenuUi.statusLabel)
    multiplayerMenuUiList.append(multiplayerMenuUi.copyIPBFrame)
    multiplayerMenuUiList.append(multiplayerMenuUi.copyIPB)

    placeMultiplayerMenuUi(multiplayerMenuUi)