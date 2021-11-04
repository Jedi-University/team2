import asyncio
from asyncio import tasks
from asyncio.tasks import Task
from queue import Queue
from ..Worker import org_worker, async_repo_worker, filter_worker, db_worker


def orch():
    orgs = []
    repos = []
    for org in org_worker.get_orgs(2):
        orgs.extend(org)
    names = org_worker.get_names(orgs)
    tasks = [async_repo_worker.get_repos(name, repos) for name in names]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    top_repos = filter_worker.filter(repos)
    db_worker.create_db(top_repos)
    db_worker.show_db()