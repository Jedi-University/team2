from multiprocessing import Queue
from threading import Thread
from typing import Callable

from ..worker import Worker


class ThreadWorker(Worker):

    def do_work(self, func: Callable[[tuple[str]], tuple[str]]):
        threads = []
        queue = Queue()
        for urls in self._data:
            thread = Thread(target=lambda q, u: q.put(func(u)), args=(queue, urls))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        result = []
        while not queue.empty():
            result.extend(queue.get())

        return result
