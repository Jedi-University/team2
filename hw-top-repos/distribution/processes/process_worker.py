from concurrent.futures import ProcessPoolExecutor
from functools import reduce
from typing import Callable

from ..worker import Worker


class ProcessWorker(Worker):

    def do_work(self, func: Callable[[tuple[str]], tuple[str]]):
        with ProcessPoolExecutor(max_workers=len(self._data)) as executor:
            result = executor.map(func, self._data)

        join_list_of_lists_into_list = lambda l: reduce(lambda a, b: a + b, l)
        result = join_list_of_lists_into_list(list(result))

        return result
