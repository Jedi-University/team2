from .thread_worker import ThreadWorker
from ..builder import Builder


class ThreadBuilder(Builder):
    def __init__(self, data):
        super().__init__(data)

    @property
    def worker(self) -> ThreadWorker:
        return ThreadWorker(self._data)
