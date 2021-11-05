from db import GitHubDB, Top

from .worker import Worker


class DatabaseWorker(Worker):
    def __init__(self, repository_data: list[dict]):
        self.repository_data: list[dict] = repository_data

        self.db: GitHubDB = GitHubDB(clear_data=True)

    def exec(self) -> None:
        super().exec()
        topic = [Top(**repo) for repo in self.repository_data]
        self.db.add_all(topic)
