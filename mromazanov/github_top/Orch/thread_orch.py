import concurrent.futures

from .orch import Orch


class TOrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Thread', self.type])

    def orch(self, workers):
        names = super().orch(workers)
        repos = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
            repos.extend(e.map(workers['repo'].get_repos, names))
        templist = repos
        repos = []
        for elem in templist:
            repos.extend(elem)
        return super().finalize(workers, repos)