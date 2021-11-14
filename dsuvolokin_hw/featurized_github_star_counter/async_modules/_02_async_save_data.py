from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine,Table,Column,Integer,String

Base = declarative_base()

repo_table = Table(
    'repo',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('org', String(50)),
    Column('repo_id', Integer),
    Column('name', String(50)),
    Column('stars_count', Integer)
)

class Repo(Base):
  __table__ = repo_table

def save_data(l):
  engine = create_engine('sqlite:///github_stars.db')
  Base.metadata.create_all(engine)
  engine.execute(Repo.__table__.insert(),l)