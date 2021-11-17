from workers import Worker

import logging

logger = logging.getLogger("Top GitHub")


class Orchestrator:
    @staticmethod
    def run(workers: list[Worker]) -> None:
        ctx = None
        for worker in workers:
            logger.debug(f"{str(worker).split()[0][1:]} is working")
            ctx = worker.exec(ctx)
