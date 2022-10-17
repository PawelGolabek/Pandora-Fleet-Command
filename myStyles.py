from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk

def loadStyles(root,style):
    
    style.configure('TButton', font =
                  ('calibri', 20, 'bold'),
                        borderwidth = '4')
    style.configure('red.Horizontal.TProgressbar', foreground='red', background='red',borderwidth = '40')
    
    # Changes will be reflected
    # by the movement of mouse.
    style.map('TButton', foreground = [('active', '!disabled', 'green')],
                        background = [('active', 'black')])
    