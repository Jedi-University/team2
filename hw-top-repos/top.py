import os

from sqlalchemy import Integer, String, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

db_file = "db/github-top.db"
Base = declarative_base()


class Top(Base):
    __tablename__ = "top"
    id = Column(Integer, primary_key=True)
    org_name = Column(String(100), nullable=False)
    repo_name = Column(String(100), nullable=False)
    stars_count = Column(Integer, nullable=False)


def get_session():
    engine = create_engine(f"sqlite:///{db_file}")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    Base.metadata.create_all(engine)
    return session


def drop_db():
    if os.path.exists(db_file):
        os.remove(db_file)
