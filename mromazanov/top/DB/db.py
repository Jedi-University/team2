from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, Session

from tkinter import *
from tkinter import scrolledtext


base = declarative_base()
engine = create_engine('sqlite:///reptop.db')
engine.connect()
session = Session(bind=engine)


class Top(base):
    __tablename__ = 'Top'
    id = Column(Integer, primary_key=True)
    org_name = Column(String(100), nullable=False)
    repo_name = Column(String(100), nullable=False)
    stars_count = Column(Integer())


class Db():
    def create_db(self, top_repos):
        base.metadata.drop_all(engine)
        base.metadata.create_all(engine)
        top_repos_base = []
        for repo in top_repos:
            top_repos_base.append(Top(id = repo['id'], org_name = repo['org_name'], repo_name = repo['repo_name'], stars_count = repo['stars']))
        session.add_all(top_repos_base)
        session.commit()

    def get(self):
        show = session.query(Top).all()
        return show
        # show_win = Tk()
        # show_win.title('Top')
        # txt = scrolledtext.ScrolledText(show_win, width=120, height=45)
        # txt.delete(1.0, END)
        # txt.insert(INSERT, 'id\t\t\torg_name\t\t\trepo_name\t\t\tstars_count\n')
        # for item in show:
        #     txt.insert(INSERT, f'{item.id}\t\t\t{item.org_name}\t\t\t{item.repo_name}\t\t\t{item.stars_count}\n')
        # txt.grid(column=0, row=0)
        # show_win.mainloop()
        