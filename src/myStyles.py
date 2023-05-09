from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
#import sv_ttk
#from ttkthemes import ThemedTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def loadStyles(root,s):
  x=10
  root.config(bg="#202020")
  s.configure('Grey.TLabelframe.Label', background='#202020',fg="red",relief="ridge")

   # print(sv_ttk.get_theme())  # Get what theme the app uses (either 'light' or 'dark')

 #   s.configure('TButton', font =
 #                 ('calibri', 20, 'bold'),
 #                       borderwidth = '4')
    # Changes will be reflected
    # by the movement of mouse.
 #   s.map('TButton', foreground = [('active', '!disabled', 'green')],
 #                       background = [('active', 'black')])
 #   s.configure("red.Horizontal.TProgressbar", thickness=10, background = "red", bordercolor = "green", darkcolor = "brown", lightcolor = "cyan")
 #   
 #   s.configure("bar.Horizontal.TProgressbar", troughcolor ='blue', background='green',foreground='red')
#
 #   s.map('gameSpeed.Horizontal.TScale', foreground = [('active', '!disabled', 'green')],
 #                       background = [('active', 'black')])
 #   s.configure("gameSpeed.Horizontal.TScale",foreground='green', background='green',height = 10)
#
 #   s.map('system.Horizontal.TProgressbar')
 #   s.configure('system.Horizontal.TProgressbar',foreground='blue', background='yellow',height = 1)
    
