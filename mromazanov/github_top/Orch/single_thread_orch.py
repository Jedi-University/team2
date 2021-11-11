from .orch import Orch

class STOrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Single_Thread', self.type])
    
    def orch(self, workers):
        names = super().orch(workers)
        repos = []
        for name in names:
            repos.extend(workers['repo'].get_repos(name))
        return super().finalize(workers, repos)