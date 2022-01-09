import asyncio
from ORCH.orch import Orch

class AsyncOrch(Orch):
    def run(self) -> list:
        top = asyncio.run(self.async_run())
        return top

    async def async_run(self):
        org_worker = self.workers['org'].run
        repo_worker = self.workers['repo'].run
        filter_worker = self.workers['filter'].run

        ctx = org_worker()
        repos = []
        tasks = [repo_worker(url) for url in ctx]
        repos = await asyncio.gather(*tasks)
        ctx = sum(repos,[])
        repos = filter_worker(ctx)
        return repos