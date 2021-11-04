import concurrent.futures

from ..Worker import org_worker, repo_worker, filter_worker, db_worker


def orch():
    orgs = []
    repos = []
    for org in org_worker.get_orgs(2):
        orgs.extend(org)
    names = org_worker.get_names(orgs)
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as e:
        repos.extend(e.map(repo_worker.get_repos, names))
    templist = repos
    repos = []
    for elem in templist:
        repos.extend(elem)
    top_repos = filter_worker.filter(repos)
    db_worker.create_db(top_repos)
    db_worker.show_db()