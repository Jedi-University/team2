from db import GitHubDB, Top

from .worker import Worker


class DatabaseWorker(Worker):
    def __init__(self):
        self.db: GitHubDB = GitHubDB(clear_data=True)

    def exec(self, repository_data: list[dict]) -> None:
        topic = [Top(**repo) for repo in repository_data]
        self.db.add_all(topic)
