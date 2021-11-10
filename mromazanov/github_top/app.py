from concurrent.futures import process, thread
from tkinter import *
from tkinter import messagebox, scrolledtext

#from Modules.Orch import single_thread_orch, thread_orch, process_orch, async_orch
#from Modules.Worker import org_worker, repo_worker, filter_worker, db_worker
from Orch import *
from Worker import *
from API import *

import time

def orch_choose(r_var):
    t0 = time.time()
    orchestrator = orch_dict[r_var.get()](workers)
    orchestrator.orch()
    t1 = time.time()
    print("Time elapsed: ", t1 - t0) # CPU seconds elapsed (floating point)


orch_dict = {0:STOrch, 1:TOrch, 2:POrch, 3:AsyncOrch}
workers = {
    'org':{'st':OrgWorker},
    'repo':{'st':RepoWorker, 'async':AsyncRepoWorker},
    'filter':{'st':FilterWorker},
    'db':{'st':DbWorker},
    'api':{'st':APIRequest, 'async':AsyncAPIRequest}
}
Db = workers['db']['st']()

window = Tk()
window.geometry('200x130')

r_var = IntVar()
r_var.set(0)
r0 = Radiobutton(text='single thread',
                 variable=r_var, value=0)
r1 = Radiobutton(text='threads',
                 variable=r_var, value=1)
r2 = Radiobutton(text='processes',
                 variable=r_var, value=2)
r3 = Radiobutton(text='async',
                 variable=r_var, value=3)
r0.grid(column=0, row=0, sticky=W)
r1.grid(column=0, row=1, sticky=W)
r2.grid(column=0, row=2, sticky=W)
r3.grid(column=0, row=3, sticky=W)

button_create = Button(window, text="Create db", command=lambda:orch_choose(r_var))
button_create.grid(column=0, row=4, sticky=W)

button_show = Button(window, text="Show db", command=lambda:Db.show_db())
button_show.grid(column=1, row=4)
window.bind('<Return>', lambda event=None: button_show.invoke())

window.mainloop()