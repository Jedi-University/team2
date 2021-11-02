from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, Session

from tkinter import *
from tkinter import messagebox, scrolledtext

import githubapi

base = declarative_base()


class Top(base):
    __tablename__ = 'Top'
    id = Column(Integer, primary_key=True)
    org_name = Column(String(100), nullable=False)
    repo_name = Column(String(100), nullable=False)
    stars_count = Column(Integer())
    
    def show(self,sep):
        return (self.id, sep, self.org_name, sep, self.repo_name, sep, self.stars_count, '\n')


def create_db(r_var, auth):
    global repo_stars, repo_names
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)

    top_repos_dict = githubapi.create_top(r_var, auth)
    top_repos = []
    for repo in top_repos_dict:
        top_repos.append(Top(id = repo['id'], org_name = repo['org_name'], repo_name = repo['repo_name'], stars_count = repo['stars_count']))
    session.add_all(top_repos)
    session.commit()
    messagebox.showinfo('', 'Успешно')


def show_db():
    show = session.query(Top).all()
    show_win = Tk()
    show_win.title('Top')
    #show_win.geometry("1024x768")
    txt = scrolledtext.ScrolledText(show_win, width=120, height=45)
    txt.delete(1.0, END)
    txt.insert(INSERT, 'id\t\torg_name\t\trepo_name\t\tstars_count\n')
    for item in show:
        txt.insert(INSERT, f'{item.id}\t\t{item.org_name}\t\t{item.repo_name}\t\t{item.stars_count}\n')
    txt.grid(column=0, row=1)
    ok_button = Button(show_win, text="ok", command=show_win.destroy)
    ok_button.grid(column=0, row=0)


engine = create_engine('sqlite:///reptop.db')
engine.connect()
session = Session(bind=engine)
