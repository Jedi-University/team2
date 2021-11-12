from .orch import Orch

class STOrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Single_Thread', self.type])
    
    def orch(self, *args):
        ctx = super().orch(*args)
        repos = []
        for name in ctx:
            repos.extend(args[1].get_repos(name))
        return super().finalize(repos, *args)