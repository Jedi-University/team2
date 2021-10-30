from .process_worker import ProcessWorker
from ..builder import Builder


class ProcessBuilder(Builder):

    def __init__(self, data):
        super().__init__(data)

    @property
    def worker(self) -> ProcessWorker:
        return ProcessWorker(self._data)
