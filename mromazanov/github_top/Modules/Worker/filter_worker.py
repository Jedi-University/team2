import heapq
from .worker import Worker


class FilterWorker(Worker):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Filter', self.type])

    def filter(self, repos):
        top_repos = heapq.nlargest(20, repos, key=lambda x:int(x['stars']))
        return top_repos