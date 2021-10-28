from top import get_session, Top


def show():
    print("Show top 20 repositories:")
    session = get_session()
    top_repos = session.query(Top).all()
    id, org_name, repo_name, stars_count = "id", "org_name", "repo_name", "stars_count"
    print(f"{id:<15} {org_name:<25} {repo_name:<25} {stars_count:<10}")
    print("-" * 80)
    for repo in top_repos:
        print(f"{repo.id:<15} {repo.org_name:<25} {repo.repo_name:<25} {repo.stars_count:<10}")
    print(f"Count: {session.query(Top).count()}")
