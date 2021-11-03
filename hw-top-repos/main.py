from configparser import ConfigParser

from db.github_db import GitHubDB
from orchestrator import Orchestrator


def show() -> None:
    db = GitHubDB()
    top_repos = db.get_whole_top()
    id, org_name, repo_name, stars_count = "id", "org_name", "repo_name", "stars_count"

    print(f"\nShow top {config['GitHub']['top_number']} repositories:")
    print(f"{id:>15} {org_name:>30} {repo_name:>30} {stars_count:>15}")
    print("-" * 95)
    for repo in top_repos:
        print(f"{repo.id:>15} {repo.org_name:>30} {repo.repo_name:>30} {repo.stars_count:>15}")
    print(f"Count: {db.get_top_size()}")


if __name__ == "__main__":
    config = ConfigParser()
    config.read("settings.ini")

    orchestrator = Orchestrator(config)
    orchestrator.run()

    show()
