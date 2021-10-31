import json
import heapq

from os import read

from tkinter import *
from tkinter import messagebox, scrolledtext

import db


def auth():
    with open('github.auth', 'r') as auth:
        info = auth.readline().strip().split(',')
    return (info[0], info[1])


auth = auth()

window = Tk()
window.geometry('200x50')

button_create = Button(window, text="Create db", command=lambda:db.create_db(auth))
button_create.grid(column=0, row=0)

button_show = Button(window, text="Show db", command=db.show_db)
button_show.grid(column=1, row=0)
window.bind('<Return>', lambda event=None: button_show.invoke())

window.mainloop()
