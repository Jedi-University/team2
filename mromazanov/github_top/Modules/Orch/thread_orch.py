import concurrent.futures

from .orch import Orch
from ..Worker import org_worker, repo_worker, filter_worker, db_worker


class TOrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Thread', self.type])

    def orch(self):
        workers = [org_worker.OrgWorker(), repo_worker.RepoWorker(), filter_worker.FilterWorker(), db_worker.DbWorker()]
        types = [self.type]
        types.extend([worker.type for worker in workers])
        print(types)
        orgs = []
        repos = []
        for org in workers[0].get_orgs(2):
            orgs.extend(org)
        names = workers[0].get_names(orgs)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
            repos.extend(e.map(workers[1].get_repos, names))
        templist = repos
        repos = []
        for elem in templist:
            repos.extend(elem)
        top_repos = workers[2].filter(repos)
        workers[3].create_db(top_repos)
        workers[3].show_db()