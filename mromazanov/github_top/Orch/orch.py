class Orch():
    get_class = lambda x: globals()[x]

    def __init__(self) -> None:
        self.type = 'Orchestrator'

    def orch(self, *args):
        types = [self.type]
        print(types)
        ctx = []
        for org in args[0].get_orgs(2):
            ctx.extend(org)
        ctx = args[0].get_names(ctx)
        return ctx

    def finalize(self, ctx, *args):
        print(args)
        top_repos = args[2].filter(ctx)
        args[3].create_db(top_repos)
        args[3].show_db()
