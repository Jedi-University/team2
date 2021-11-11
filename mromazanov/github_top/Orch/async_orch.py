import asyncio
from asyncio import tasks
from asyncio.tasks import Task
from queue import Queue

from .orch import Orch

class AsyncOrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Async', self.type])

    def orch(self, workers):
        names = super().orch(workers)
        repos = []
        tasks = [workers['async_repo'].get_repos(name, repos) for name in names]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        super().finalize(workers, repos)