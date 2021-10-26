import json
import heapq
import requests
from requests.sessions import session
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, Session
from tkinter import *
from tkinter import messagebox, scrolledtext 

Base = declarative_base()
metadata = MetaData()


def auth():
    return ('Client ID', 'Client secret')


class Top(Base):
    __tablename__ = 'Top'
    id = Column(Integer, primary_key=True)
    org_name = Column(String(100), nullable=False)
    repo_name = Column(String(100), nullable=False)
    stars_count = Column(Integer())


def get_names(orgs):
    names = []
    for entry in orgs:
        names.append(entry['login'])
    return names


def get_orgs(pages):
    global last_id
    text = ''
    iteration = 0
    while iteration < pages:
        response_API = requests.get(f'https://api.github.com/organizations?since={last_id}&per_page=100', auth=auth()).json()
        last_id = response_API[-1]['id']
        iteration += 1
        yield response_API
    

def get_repos(name):
    global repoStars, repoNames
    response_API = requests.get(f'https://api.github.com/orgs/{name}/repos', auth=auth()).json()
    for repo in response_API:
        id = repo['id']
        name = repo['full_name']
        stars = repo['stargazers_count']
        repoStars[id] = stars
        repoNames[id] = name
    return response_API


def Create_db():
    global engine, session, last_id, orgs, repoNames, repoStars, repos
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    for i in get_orgs(2):
        orgs.extend(i)
    names = get_names(orgs)
    repos.extend(get_repos("Jedi-University"))
    for name in names:
        repos.extend(get_repos(name))
    repoStars = heapq.nlargest(20, repoStars.items(), key=lambda i: i[1])
    toprepos = []
    for repo in repoStars:
        toprepos.append(Top(id = repo[0], org_name = repoNames[repo[0]].split('/')[0], repo_name = repoNames[repo[0]].split('/')[1],\
            stars_count = repo[1]))
    session.add_all(toprepos)
    session.commit()
    messagebox.showinfo('', 'Успешно')


def Show_db():
    show = session.query(Top).all()
    showWin = Tk()
    showWin.title('Top')
    #showWin.geometry("1024x768")
    txt = scrolledtext.ScrolledText(showWin, width=120, height=45)
    txt.delete(1.0, END)
    txt.insert(INSERT, 'id\t\torg_name\t\trepo_name\t\tstars_count\n')
    for item in show:
        txt.insert(INSERT, f'{item.id}\t\t{item.org_name}\t\t{item.repo_name}\t\t{item.stars_count}\n')
    txt.grid(column=0, row=1)
    Pbtn = Button(showWin, text="ok", command=showWin.destroy)
    Pbtn.grid(column=0, row=0)


engine = create_engine('sqlite:///reptop.db')
engine.connect()
session = Session(bind=engine)

last_id = 0
orgs = []
repoStars = {}
repoNames = {}
repos = []


window = Tk()
window.geometry('200x50')

btnCreate = Button(window, text="Create db", command=Create_db)  
btnCreate.grid(column=0, row=0)


btnShow = Button(window, text="Show db", command=Show_db)
btnShow.grid(column=1, row=0)
window.bind('<Return>', lambda event=None: btnShow.invoke())

window.mainloop()
