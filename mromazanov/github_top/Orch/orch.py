class Orch():
    get_class = lambda x: globals()[x]

    def __init__(self) -> None:
        self.type = 'Orchestrator'

    def orch(self, workers):
        types = [self.type]
        print(types)
        orgs = []
        for org in workers['org'].get_orgs(workers, 2):
            orgs.extend(org)
        names = workers['org'].get_names(orgs)
        return names

    def finalize(self, workers, repos):
        top_repos = workers['filter'].filter(repos)
        workers['db'].create_db(top_repos)
        workers['db'].show_db()
