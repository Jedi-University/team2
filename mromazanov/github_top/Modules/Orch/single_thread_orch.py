from ..Worker import org_worker, repo_worker, filter_worker, db_worker


def orch():
    orgs = []
    repos = []
    for org in org_worker.get_orgs(2):
        orgs.extend(org)
    names = org_worker.get_names(orgs)
    for name in names:
        repos.extend(repo_worker.get_repos(name))
    top_repos = filter_worker.filter(repos)
    db_worker.create_db(top_repos)
    db_worker.show_db()