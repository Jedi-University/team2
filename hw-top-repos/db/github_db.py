import os

from sqlalchemy import Integer, String, Column
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Top(Base):
    __tablename__ = "top"

    id = Column(Integer, primary_key=True)
    org_name = Column(String(100), nullable=False)
    repo_name = Column(String(100), nullable=False)
    stars_count = Column(Integer, nullable=False)


class GitHubDB:
    FILE_PATH = "db/github-topic.db"

    def __init__(self, clear_data: bool = False):
        if clear_data:
            GitHubDB.remove_db_file()

        self.engine = create_engine(f"sqlite:///{GitHubDB.FILE_PATH}")
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def add(self, instance: Top) -> None:
        self.session.add(instance)
        self.session.commit()

    def add_all(self, instances: list[Top]) -> None:
        self.session.add_all(instances)
        self.session.commit()

    def get_whole_top(self) -> list[Top]:
        return self.session.query(Top).all()

    def get_top_size(self) -> int:
        return self.session.query(Top).count()

    @staticmethod
    def remove_db_file() -> None:
        if os.path.exists(GitHubDB.FILE_PATH):
            os.remove(GitHubDB.FILE_PATH)
