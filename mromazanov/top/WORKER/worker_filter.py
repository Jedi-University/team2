from WORKER.worker import Worker

class FilterWorker(Worker):
    def run(self, repos:list):
        repos = self.top_by_stars(repos)
        return repos