from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
#import sv_ttk
#from ttkthemes import ThemedTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def loadStyles(root,s):
   root.config(bg="#1e1e1e")
   s.configure('Grey.TLabelframe', background='#1e1e1e',bordercolor = '#505050',lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Grey.TLabelframe.Label', fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')

   s.configure('GreyBig.TLabelframe', background='#1e1e1e',bordercolor = '#505050',lightcolor = "#1f3556", darkcolor = "#1f3556", font ='Calibri 12 normal')
   s.configure('GreyBig.TLabelframe.Label', fg = "#EFEFEF", background='#1e1e1e',bordercolor = '#505050',lightcolor = "#1f3556", darkcolor = "#1f3556",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('GreyBig.TLabel', background='#1e1e1e',foreground = "#bfbfbf",justify='center',font= ('Calibri 14 normal'))
   s.configure('GreyBig.TEntry', background='#1e1e1e',foreground = "#000000",justify='center',font= ('Calibri', 16))

   s.configure('Pause.TLabel', background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#bfbfbf", font= ('Calibri 16 normal'),borderwidth=2, relief="groove", bordercolor = "green", width=10, height = 40, padding = 3,anchor=CENTER)

   s.configure('NonSerif.TLabelframe', background='#1e1e1e',bordercolor = '#505050',lightcolor = "#0F4F0F", darkcolor = "#044404", font= ('Consolas 11 normal'))
   s.configure('NonSerif.TLabel', background='#1e1e1e',foreground = "#EFEFEF",justify='center',font= ('Consolas 11 normal'))
   s.configure('NonSerif.TLabelframe.Label',  fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font= ('Consolas 11 normal'))

   s.configure('NonSerifBlue.TLabelframe', background='#1e1e1e',bordercolor = '#505050',lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Consolas 11 normal'))
   s.configure('NonSerifBlue.TLabel', background='#1e1e1e',foreground = "#EFEFEF",justify='center',font= ('Consolas 11 normal'))
   s.configure('NonSerifBlue.TLabelframe.Label',  fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#1f3556", darkcolor = "#1f3556", foreground = "#FAFAFA", font= ('Consolas 11 normal'))

   s.configure('NonSerifBlueConsolas.TLabelframe', background='#1e1e1e',bordercolor = '#505050',lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Consolas 11 normal'))
   s.configure('NonSerifBlueConsolas.TLabel', background='#1e1e1e',foreground = "#EFEFEF",justify='center',font= ('Consolas 11 normal'))
   s.configure('NonSerifBlueConsolas.TLabelframe.Label',  fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#1f3556", darkcolor = "#1f3556", foreground = "#FAFAFA", font= ('Consolas 11 normal'))

   s.configure('Green.TLabelframe', background='#1e1e1e',bordercolor = '#505050',lightcolor = "#0AAF0A", darkcolor = "#0AAF0A")
   s.configure('Green.TLabelframe.Label', fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0FAF0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('DarkRed.TLabelframe', background='#1e1e1e',bordercolor = '#505050',lightcolor = "#4F0F0F", darkcolor = "#4F0A0A")
   s.configure('DarkRed.TLabelframe.Label', fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#4F0F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')

   s.configure('BigOne.TButton',background='#1e1e1e',fg="white",relief="ridge", font=('Calibri 12 normal'), highlightbackground="#4582ec", width = 18, height = 5)
   s.configure('Big.TButton', background='#1e1e1e',fg="red",relief="ridge", font=('Consolas 12 normal'))
   s.configure('View.TButton', background='#1e1e1e',fg="red",relief="ridge", font=('Calibri 10 normal'))
   s.configure('Blue.Horizontal.Tscale', background="#4582ec",bordercolor="#4582ec", lightcolor = "#4582ec", darkcolor="#4582ec", height = 2)
   s.configure('Grey.Horizontal.TScale')
   #bg="#4582ec",highlightcolor = "white" , length=uiMetrics.systemScaleWidth,highlightbackground = "#bfbfbf"
   s.configure('Red.Horizontal.TProgressbar', foreground = "red")
   s.configure('Blue.Horizontal.TProgressbar', foreground = "green")
   s.configure('Grey.TRadiobutton', foreground = "#bfbfbf", background = '#1e1e1e')
   s.configure('Red.TCheckbutton',foreground = "#bfbfbf", background = '#1e1e1e',font='Calibri 12 normal')
   s.configure('Disabled.TCheckbutton',font='Calibri 12 normal',foreground='#4F4F4F', background='#1e1e1e', lightcolor="#000000", darkcolor= "#000000")
   #s.map('Disabled.TCheckbutton', foreground=[('disabled', '#4F4F4F')], background=[('disabled', '#1e1e1e')], lightcolor=[('disabled', "#000000")], darkcolor=[('disabled', "#000000")])
   s.configure('Grey.TLabel', background='#1e1e1e',foreground = "#EFEFEF",justify='center',font= ('Calibri 12 normal'))
   s.configure('SmallGrey.TLabel', background='#1e1e1e',foreground = "#EFEFEF",justify='center',font= ('Calibri 9 normal'), padding = 0, margin = 0)
   s.configure("Green.TLabel", foreground = 'green', background = '#1e1e1e',justify='center',font= ('Calibri 12 normal'))
   s.configure("Red.TLabel", foreground = 'red', background = '#1e1e1e',justify='center',font= ('Calibri 12 normal'))
   s.configure("Yellow.TLabel", foreground = 'yellow', background = '#1e1e1e',justify='center',font= ('Calibri 12 normal'))
   s.configure("Blue.TLabel", foreground = '#4582ec', background = '#1e1e1e',justify='center',font= ('Calibri 12 normal'))
   s.configure("TMenubutton", background="#4582ec", foreground = "white", padding = 3)
   s.map('Grey.TRadiobutton',
         foreground=[('disabled', 'black'),
                     ('pressed', '#bfbfbf'),
                     ('active', '#505050')])
   s.configure("Info.TButton",background='#505050',fg="red",relief="ridge", font=('Consolas 12 bold'), #width = 20, height = 20
                activeforeground='red', activebackground='#505050')
   

   s.configure('DarkOrchid1.TLabelframe',    relief=GROOVE, background='#1e1e1e',bordercolor = 'DarkOrchid1',lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('DarkOrchid2.TLabelframe',    relief=GROOVE, background='#1e1e1e',bordercolor = 'DarkOrchid2',lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('IndianRed.TLabelframe' ,     relief=GROOVE, background='#1e1e1e',bordercolor = 'indian red' ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('DarkSlateGrey.TLabelframe' , relief=GROOVE, background='#1e1e1e',bordercolor = 'dark slate grey' ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Orchid4.TLabelframe'    ,    relief=GROOVE, background='#1e1e1e',bordercolor = 'Orchid4'    ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Grey60.TLabelframe'     ,    relief=GROOVE, background='#1e1e1e',bordercolor = 'Grey60'     ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('White.TLabelframe'      ,    relief=GROOVE, background='#1e1e1e',bordercolor = 'white'      ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Brown2.TLabelframe'     ,    relief=GROOVE, background='#1e1e1e',bordercolor = 'brown2'     ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Brown4.TLabelframe'     ,    relief=GROOVE, background='#1e1e1e',bordercolor = 'brown4'     ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Gold.TLabelframe'       ,    relief=GROOVE, background='#1e1e1e',bordercolor = 'Gold'       ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Yellow.TLabelframe'       ,  relief=GROOVE, background='#1e1e1e',bordercolor = 'Yellow'       ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Goldenrod3.TLabelframe' ,    relief=GROOVE, background='#1e1e1e',bordercolor = 'goldenrod3' ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Purple.TLabelframe'  ,      relief=GROOVE, background='#1e1e1e',bordercolor = 'Purple' ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Purple2.TLabelframe'  ,      relief=GROOVE, background='#1e1e1e',bordercolor = 'Purple2' ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))
   s.configure('Red.TLabelframe'  ,          relief=GROOVE, background='#1e1e1e',bordercolor = 'Red' ,lightcolor = "#1f3556", darkcolor = "#1f3556", font= ('Calibri 14 normal'))

   s.configure('DarkOrchid1.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('DarkOrchid2.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('IndianRed.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('DarkSlateGrey.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Orchid4.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Grey60.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('White.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Brown2.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Brown4.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Gold.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Yellow.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Goldenrod3.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Purple.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Purple2.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')
   s.configure('Red.TLabelframe.Label' , fg = "#EFEFEF", background='#1e1e1e',lightcolor = "#0F4F0F", darkcolor = "#FAFAFA",foreground = "#FAFAFA", font ='Calibri 12 normal')

  # s.configure('MenuB.TButton',   font=('Optima',11))
 
   
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
    
