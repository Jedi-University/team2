import concurrent.futures

from .orch import Orch

class POrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Process', self.type])

    def orch(self, *args):
        ctx = super().orch(*args)
        repos = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=8) as e:
            repos.extend(e.map(args[1].get_repos, ctx))
        ctx = []
        for elem in repos:
            ctx.extend(elem)
        super().finalize(ctx, *args)