import requests

from config import config
from distribution.builder import Builder
from distribution.processes.process_builder import ProcessBuilder
from distribution.threads.thread_builder import ThreadBuilder
from github_db import GitHubDB, Top

headers = {"Authorization": f"token {config['GitHub']['access_token']}"}


def fetch() -> None:
    print("Data is taken from github:")
    num_of_orgs = int(config["GitHub"]["num_of_orgs"])
    repos_urls_with_id = get_repos_urls_with_id(num_of_orgs=num_of_orgs)
    repos_urls = tuple(repos_urls_with_id.values())
    repos_data = get_builder(repos_urls).worker.do_work(get_repos_data)
    print("done!")

    print(f"Top {config['GitHub']['top_number']} repositories determined:", end=" ")
    top_number = int(config["GitHub"]["top_number"])
    top_repos = get_top(repos_data, top_number)
    print("done!")

    print("Loading data into a database:", end=" ")
    load_repos_into_db(top_repos)
    print("done!")


def get_repos_urls_with_id(num_of_orgs: int = 100) -> dict[int, str]:
    repos_urls_with_id = {}
    max_orgs = 100
    if num_of_orgs <= max_orgs:
        repos_urls_with_id.update(get_given_num_of_repos_urls(per_page=num_of_orgs))
    else:
        for _ in range(num_of_orgs // max_orgs):
            repos_urls_with_id.update(
                get_given_num_of_repos_urls(since=get_since(repos_urls_with_id))
            )

        remain = num_of_orgs % max_orgs
        if remain != 0:
            repos_urls_with_id.update(
                get_given_num_of_repos_urls(
                    per_page=remain, since=get_since(repos_urls_with_id)
                )
            )

    return repos_urls_with_id


def get_given_num_of_repos_urls(per_page: int = 100, since: int = 0) -> dict[int, str]:
    url = "https://api.github.com/organizations"
    params = {"per_page": per_page, "since": since}
    response = requests.get(url, params=params, headers=headers).json()
    repos_urls_with_id = {org["id"]: org["repos_url"] for org in response}
    return repos_urls_with_id


def get_since(dictionary: dict[int, str]) -> int:
    return 0 if len(dictionary) == 0 else list(dictionary.keys())[-1]


def get_builder(repos_urls: tuple[str]) -> Builder:
    # плюсы: легко модифицировать при появлении новых строителей
    builders = {"thread": ThreadBuilder, "process": ProcessBuilder}
    return builders[config["Build"]["builder"]](repos_urls)


def load_repos_into_db(repos: tuple[dict]) -> None:
    db = GitHubDB(clear_data=True)
    topic = [Top(**repo) for repo in repos]
    db.add_all(topic)


def get_repos_data(repos_urls: tuple[str]) -> tuple[dict]:
    repos = []
    for counter, url in enumerate(repos_urls):
        print(f"{counter + 1}/{len(repos_urls)} organizations")
        repos.extend(get_all_repos(url))

    return get_top(repos, int(config["GitHub"]["top_number"]))


def get_all_repos(url: str) -> tuple[dict]:
    page = 1
    repos = []
    response = requests.get(url, headers=headers).json()
    while response:
        page += 1
        repos.extend(map(mapping_repo, response))
        params = {"page": page}
        response = requests.get(url, params=params, headers=headers).json()

    return tuple(repos)


def get_top(repos_data: list[dict], top_number: int) -> tuple[dict]:
    return tuple(
        sorted(repos_data, key=lambda repo: repo["stars_count"], reverse=True)
    )[:top_number]


def mapping_repo(repo: dict) -> dict:
    return {
        "id": repo["id"],
        "org_name": repo["owner"]["login"],
        "repo_name": repo["name"],
        "stars_count": repo["stargazers_count"],
    }
