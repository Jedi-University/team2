from concurrent.futures import process, thread
from tkinter import *
from tkinter import messagebox, scrolledtext

#from Modules.Orch import single_thread_orch, thread_orch, process_orch, async_orch
#from Modules.Worker import org_worker, repo_worker, filter_worker, db_worker
from Orch import *
from Worker import *
from API import *

import time
import configparser

get_class = lambda x: globals()[x]

def orch_choose(r_var):
    t0 = time.time()
    orchestrator = orch_dict[r_var.get()][0]()
    orchestrator.orch(*orch_dict[r_var.get()][1:])
    t1 = time.time()
    print("Time elapsed: ", t1 - t0) # CPU seconds elapsed (floating point)


config = configparser.ConfigParser()
config.read("config.ini")
orch_dict = {
    0:[STOrch, OrgWorker(APIRequest()), RepoWorker(APIRequest()), FilterWorker(), DbWorker()],
    1:[TOrch, OrgWorker(APIRequest()), RepoWorker(APIRequest()), FilterWorker(), DbWorker()],
    2:[POrch, OrgWorker(APIRequest()), RepoWorker(APIRequest()), FilterWorker(), DbWorker()],
    3:[AsyncOrch, OrgWorker(APIRequest()), AsyncRepoWorker(AsyncAPIRequest()), FilterWorker(), DbWorker()]
}

#workers = {
#    'org':get_class(config['Workers']['org'])(),
#    'repo':get_class(config['Workers']['repo'])(get_class(config['Api']['api'])()),
#    'async_repo':get_class(config['Workers']['async_repo'])(get_class(config['Api']['async_api'])()),
#    'filter':get_class(config['Workers']['filter'])(),
#    'db':get_class(config['Workers']['db'])(),
#    'api':get_class(config['Api']['api'])(),
#    'async_api':get_class(config['Api']['async_api'])()
#}
#workers = {
#    'org':{'st':OrgWorker},
#    'repo':{'st':RepoWorker, 'async':AsyncRepoWorker},
#    'filter':{'st':FilterWorker},
#    'db':{'st':DbWorker},
#    'api':{'st':APIRequest, 'async':AsyncAPIRequest}
#}

Db = get_class(config['Workers']['db'])()

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