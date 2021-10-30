from config import config
from top import get_session, Top


def show():
    session = get_session()
    top_repos = session.query(Top).all()
    id, org_name, repo_name, stars_count = "id", "org_name", "repo_name", "stars_count"

    print(f"Show top {config['GitHub']['top_number']} repositories:")
    print(f"{id:>15} {org_name:>20} {repo_name:>25} {stars_count:>15}")
    print("-" * 80)
    for repo in top_repos:
        print(f"{repo.id:>15} {repo.org_name:>20} {repo.repo_name:>25} {repo.stars_count:>15}")
    print(f"Count: {session.query(Top).count()}")
