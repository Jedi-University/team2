from db import GitHubDB, Top

from .worker import Worker


class DatabaseWorker(Worker):
    def __init__(self, repository_data: tuple[dict]):
        self.repository_data: tuple[dict] = repository_data

        self.db: GitHubDB = GitHubDB(clear_data=True)

    def exec(self) -> None:
        print(f"{self.__class__.__name__} is working")
        topic = [Top(**repo) for repo in self.repository_data]
        self.db.add_all(topic)
