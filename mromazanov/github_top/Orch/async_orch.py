import asyncio
from asyncio import tasks
from asyncio.tasks import Task
from queue import Queue

from .orch import Orch

class AsyncOrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Async', self.type])

    def orch(self, *args):
        ctx = super().orch(*args)
        repos = []
        tasks = [args[1].get_repos(name, repos) for name in ctx]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        super().finalize(repos, *args)