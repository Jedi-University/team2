import os
import subprocess
import sys
import pathlib

from tkinter import *
from tkinter import messagebox


def Make_file():
    coin = coinEntry.get()
    period = periodEntry.get()

    messagebox.showinfo('', 'running 01_make_file.py')
    subprocess.Popen([sys.executable, path + '/01_make_file.py', coin, period])    


def Divide_into_files():
    messagebox.showinfo('', 'running 2_division_into_files.py')
    try:
        subprocess.check_call([sys.executable, path + '/02_division_into_files.py'])
    except subprocess.CalledProcessError:
        messagebox.showinfo('', 'There is no such file or directory!')
    


def Make_files():
    Make_file()
    Divide_into_files()


def Count_SMA30():
    messagebox.showinfo('', 'running 03_mean_analyzer.py')
    try:
        subprocess.check_call([sys.executable, path + '/03_mean_analyzer.py'])
    except subprocess.CalledProcessError:
        messagebox.showinfo('', 'There is no "coin_folder" directory!')


path = os.path.realpath('./')
window = Tk()
window.title("pipe.py")
window.geometry('250x150') 

coinLbl = Label(window, text="Coin:")
coinLbl.grid(column=0, row=0)
coinEntry = Entry(window, width=10)
coinEntry.insert(END, "ethereum")  
coinEntry.grid(column=1, row=0) 
coinEntry.focus()

btnMake = Button(window, text="Make file", command=Make_file)  
btnMake.grid(column=0, row=2)

periodLbl = Label(window, text="Period:")
periodLbl.grid(column=0, row=1)
periodEntry = Entry(window,width=10)
periodEntry.insert(END, "365")
periodEntry.grid(column=1, row=1)

btnDiv = Button(window, text="Divide into files", command=Divide_into_files)
btnDiv.grid(column=1, row=2)

btnMakeDiv = Button(window, text="Make files", command=Make_files)
btnMakeDiv.grid(column=0, row=3)

btnCount = Button(window, text="Count SMA30", command=Count_SMA30)
btnCount.grid(column=1, row=3)

window.mainloop()
