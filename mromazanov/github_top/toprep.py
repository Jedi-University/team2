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
window.geometry('200x60')

r_var = BooleanVar()
r_var.set(0)
r1 = Radiobutton(text='threads',
                 variable=r_var, value=0)
r2 = Radiobutton(text='processes',
                 variable=r_var, value=1)
r1.grid(column=0, row=0)
r2.grid(column=1, row=0)

button_create = Button(window, text="Create db", command=lambda:db.create_db(r_var, auth))
button_create.grid(column=0, row=1)

button_show = Button(window, text="Show db", command=db.show_db)
button_show.grid(column=1, row=1)
window.bind('<Return>', lambda event=None: button_show.invoke())

window.mainloop()
