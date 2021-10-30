from abc import ABC, abstractmethod


class Builder(ABC):

    def __init__(self, data):
        self._data = data

    @property
    @abstractmethod
    def worker(self):
        pass
