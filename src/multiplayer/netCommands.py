from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from functools import partial
from pathlib import Path
import socket

from src.settings import dynamic_object


def fill_data_to_size(data, target_size):
    """
    Fills the data with null bytes to reach the target size.
    """
    return data.ljust(target_size, ' ')

def get_local_ip():
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except Exception as e:
        print("Error while trying to read ip address")


def receiveFixedMessage(socket):
    # Receive the header (4 bytes for message length)
    header = socket.recv(4)
    messageLength = int.from_bytes(header, byteorder='big')

    # Receive the message
    message = socket.recv(messageLength).decode("utf-8")
    return message

    
def sendFixedMessage(sock, message):
    message_length = len(message)
    message_header = message_length.to_bytes(4, byteorder='big')  # Using 4 bytes for the header
    sock.sendall(message_header + message.encode("utf-8"))

def disconnect(multiplayerOptions):
    multiplayerOptions.socket.close()
    if(multiplayerOptions.side == 'server'):
        multiplayerOptions.serverSocket.close()
