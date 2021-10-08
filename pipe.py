import os
import subprocess
from tkinter import *  

def Make_file():
    coin = coinEntry.get()
    period = periodEntry.get()

    subprocess.Popen(['python3', 'make_file.py', coin, period])

def Divide_into_files():
    print("Div")
    #subprocess.Popen(['python3'])

def Make_files():
    Make_file()
    Divide_into_files()

def Count_SMA30():
    print("SMA30")

window = Tk()  
window.title("")  
window.geometry('400x250') 

coinLbl = Label(window, text = "Coin:")
coinLbl.grid(column = 0, row = 0)
coinEntry = Entry(window, width= 10)
coinEntry.insert(END, "ethereum")  
coinEntry.grid(column = 1, row = 0) 
coinEntry.focus()

btnMake = Button(window, text = "Make file", command = Make_file)  
btnMake.grid(column = 0, row = 2)

periodLbl = Label(window, text = "Period:")
periodLbl.grid(column = 0, row = 1)
periodEntry = Entry(window,width = 10)
periodEntry.insert(END, "365")
periodEntry.grid(column = 1, row = 1)

btnDiv = Button(window, text = "Divide into files", command = Divide_into_files)
btnDiv.grid(column = 1, row = 2)

btnMakeDiv = Button(window, text = "", command = Make_files)
btnMakeDiv.grid(column = 2, row = 2)

btnCount = Button(window, text = "", command = Count_SMA30)
btnCount.grid(column = 3, row = 2)

window.mainloop()
