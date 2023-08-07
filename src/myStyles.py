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
  s.map('Big.TButton')
  s.map('Grey.TLabelframe')
  s.map('Grey.TLabel')
  s.map('Blue.THorizontal.Progressbar')
  s.map('Red.Horizontal.TProgressbar')
  s.map("Green.TLabel")
  s.map("Red.TLabel")
  s.map("Yellow.TLabel")
  s.configure('Grey.TLabelframe', background='#202020',bordercolor = '#505050',lightcolor = "#0F0F0F", darkcolor = "#040404")
  s.configure('Grey.TLabelframe.Label', fg = "#EFEFEF", background='#202020',lightcolor = "#0F0F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA")
  s.configure('Green.TLabelframe', background='#202020',bordercolor = '#505050',lightcolor = "#0FAF0F", darkcolor = "#0AAF0A")
  s.configure('Green.TLabelframe.Label', fg = "#EFEFEF", background='#202020',lightcolor = "#0FAF0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA")
  s.configure('Grey.TLabel', background='#202020',foreground = "#EFEFEF")
  s.configure('Big.TButton', background='#202020',fg="red",relief="ridge", font=('Optima',12))
  s.configure('Blue.Horizontal.Tscale', background="#4582ec",bordercolor="#4582ec", lightcolor = "#4582ec", darkcolor="#4582ec", height = 2)
  s.configure('Grey.Horizontal.Tscale', bg="#4582ec",highlightcolor = "white",fg = "white",highlightbackground = "#bfbfbf")
  s.configure('Red.Horizontal.TProgressbar', foreground = "red")
  s.configure('Blue.Horizontal.TProgressbar', foreground = "green")
  s.configure('Grey.TRadiobutton', foreground = "#bfbfbf", background = '#202020')
  s.configure("Green.TLabel", foreground = 'green', background = '#202020')
  s.configure("Red.TLabel", foreground = 'red', background = '#202020')
  s.configure("Yellow.TLabel", foreground = 'yellow', background = '#202020')
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
    
