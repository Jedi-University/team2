import concurrent.futures

from .orch import Orch


class TOrch(Orch):
    def __init__(self, workers) -> None:
        super().__init__()
        self.type = '_'.join(['Thread', self.type])
        self.org_worker = workers['org']['st'](workers['api']['st'])
        self.repo_worker = workers['repo']['st'](workers['api']['st'])
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
            repos.extend(e.map(self.repo_worker.get_repos, names))
        templist = repos
        repos = []
        for elem in templist:
            repos.extend(elem)
        top_repos = self.filter_worker.filter(repos)
        self.db_worker.create_db(top_repos)
        self.db_worker.show_db()