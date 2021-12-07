import logging

from azavarzin.github_top_repos import Worker

logger = logging.getLogger("Top GitHub")


class Orchestrator:

    def run(workers: list[Worker], ctx=None) -> None:
        for worker in workers:
            logger.debug(f"{str(worker)} is working")
            ctx = worker.exec(ctx)
