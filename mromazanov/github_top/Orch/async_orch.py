import asyncio
from asyncio import tasks
from asyncio.tasks import Task
from queue import Queue

from .orch import Orch

class AsyncOrch(Orch):
    def __init__(self, workers) -> None:
        super().__init__()
        self.type = '_'.join(['Async', self.type])
        self.org_worker = workers['org']['st'](workers['api']['st'])
        self.repo_worker = workers['repo']['async'](workers['api']['async'])
        self.filter_worker = workers['filter']['st']()
        self.db_worker = workers['db']['st']()

    def orch(self):
        types = [self.type]
        types.extend([self.org_worker.type, self.repo_worker.type, self.filter_worker.type, self.db_worker.type])
        print(types)
        orgs = []
        repos = []
        for org in self.org_worker.get_orgs(2):
            orgs.extend(org)
        names = self.org_worker.get_names(orgs)
        tasks = [self.repo_worker.get_repos(name, repos) for name in names]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        top_repos = self.filter_worker.filter(repos)
        self.db_worker.create_db(top_repos)
        self.db_worker.show_db()