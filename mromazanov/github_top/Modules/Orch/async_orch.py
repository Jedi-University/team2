import asyncio
from asyncio import tasks
from asyncio.tasks import Task
from queue import Queue

from .orch import Orch
from ..Worker import org_worker, repo_worker, filter_worker, db_worker


class AsyncOrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Async', self.type])

    def orch(self):
        workers = [org_worker.OrgWorker(), repo_worker.AsyncRepoWorker(), filter_worker.FilterWorker(), db_worker.DbWorker()]
        types = [self.type]
        types.extend([worker.type for worker in workers])
        print(types)
        orgs = []
        repos = []
        for org in workers[0].get_orgs(2):
            orgs.extend(org)
        names = workers[0].get_names(orgs)
        tasks = [workers[1].get_repos(name, repos) for name in names]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        top_repos = workers[2].filter(repos)
        workers[3].create_db(top_repos)
        workers[3].show_db()