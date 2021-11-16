from workers import Worker


class Orchestrator:
    def run(self, workers: list[Worker]) -> None:
        ctx = None
        for worker in workers:
            print(f"{type(worker)}")
            ctx = worker.exec(ctx)
