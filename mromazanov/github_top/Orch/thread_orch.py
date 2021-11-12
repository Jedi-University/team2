import concurrent.futures

from .orch import Orch


class TOrch(Orch):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Thread', self.type])

    def orch(self, *args):
        ctx = super().orch(*args)
        repos = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
            repos.extend(e.map(args[1].get_repos, ctx))
        ctx = []
        for elem in repos:
            ctx.extend(elem)
        return super().finalize(ctx, *args)