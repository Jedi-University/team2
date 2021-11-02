import threading
from threading import Thread

import multiprocessing
from multiprocessing import Pool, queues
from multiprocessing.queues import Queue


class Thread_Worker():
    def work(func, queue, auth):
        results = multiprocessing.Queue()
        while queue.empty() is False:
            threads = []
            for i in range(int(multiprocessing.cpu_count())*2):
                threads.append(Thread(target = func, args = (queue, auth, results)))
                threads[i].start()
            for thread in threads:
                thread.join()
        return results


class Process_Worker():
    def work(func, queue, auth):
        results = multiprocessing.Queue()
        while queue.empty() is False:
            procs = []
            for i in range(multiprocessing.cpu_count()*2):
                if queue.empty() is False:
                    procs.append(multiprocessing.Process(target=func, args=(queue, auth, results)))
                    procs[i].start()
                else:
                    continue
            for proc in procs:
                proc.join()
        return results