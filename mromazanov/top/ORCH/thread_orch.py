import concurrent.futures

from ORCH.orch import Orch

class ThreadOrch(Orch):
    def run(self):
        org_worker = self.workers['org'].run
        repo_worker = self.workers['repo'].run
        filter_worker = self.workers['filter'].run

        ctx = org_worker()
        repos = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
            repos.extend(e.map(repo_worker, ctx))
        ctx = sum(repos,[])
        repos = filter_worker(ctx)
        return repos