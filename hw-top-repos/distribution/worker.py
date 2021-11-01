from abc import ABC, abstractmethod
from multiprocessing import cpu_count
from typing import Callable


class Worker(ABC):

    def __init__(self, data):
        splitting_data_into_equal_parts = lambda l, s: [l[i: i + s] for i in range(0, len(l), s)]
        size = (len(data) // (cpu_count() * 2)) + 1
        self._data = splitting_data_into_equal_parts(data, size)

    @abstractmethod
    def do_work(self, func: Callable[[tuple[str]], tuple[dict]]):
        pass
