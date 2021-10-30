import requests

from config import config
from distribution.processes.process_builder import ProcessBuilder
from distribution.threads.thread_builder import ThreadBuilder
from top import get_session, Top, drop_db

headers = {"Authorization": f"token {config['GitHub']['access_token']}"}


def fetch():
    print("Data is taken from github:")
    num_of_orgs = int(config["GitHub"]["num_of_orgs"])
    repos_urls_with_id = get_repos_urls_with_id(num_of_orgs=num_of_orgs)
    repos_urls = list(repos_urls_with_id.values())
    repos_data = get_builder(repos_urls).worker.do_work(get_repos_data)
    print("done!")

    print(f"Top {config['GitHub']['top_number']} repositories determined:", end=" ")
    top_number = int(config["GitHub"]["top_number"])
    top_repos = get_top(repos_data, top_number)
    print("done!")

    print("Loading data into a database:", end=" ")
    load_repos_into_db(top_repos)
    print("done!")


def get_repos_urls_with_id(num_of_orgs=100) -> dict:
    data = {}
    max_org = 100
    if num_of_orgs <= max_org:
        data.update(get_given_num_of_repos_urls(per_page=num_of_orgs))
    else:
        for _ in range(num_of_orgs // max_org):
            data.update(get_given_num_of_repos_urls(since=get_since(data)))
        
        remain = num_of_orgs % max_org
        if remain != 0:
            data.update(get_given_num_of_repos_urls(per_page=remain, since=get_since(data)))
    return data


def get_given_num_of_repos_urls(per_page=100, since=0) -> dict:
    url = "https://api.github.com/organizations"
    params = {"per_page": per_page, "since": since}
    response = requests.get(url, params=params, headers=headers).json()
    data = {org["id"]: org["repos_url"] for org in response}
    return data


def get_since(dictionary) -> int:
    return 0 if len(dictionary) == 0 else list(dictionary.keys())[-1]


def get_builder(data):
    # плюсы: будет создан только нужный строитель
    # минусы: при добавлении новых строителей падает читаемость и лаконичность кода
    if config["Build"]["builder"] == "thread":
        return ThreadBuilder(data)
    elif config["Build"]["builder"] == "process":
        return ProcessBuilder(data)
    else:
        raise Exception("There is no such builder")


def get_builder_bad_way(data):
    # плюсы: легко модифицировать при появлении новых строителей
    # минусы: в словаре создаются все экземпляры строителей, их может быть очень много или они могут быть тяжеловесными
    builders = {
        "thread": ThreadBuilder(data),
        "process": ProcessBuilder(data)
    }
    return builders[config["Build"]["builder"]]


def load_repos_into_db(repos):
    drop_db()
    session = get_session()
    for repo in repos:
        top = Top(
            id=repo["id"],
            org_name=repo["org_name"],
            repo_name=repo["repo_name"],
            stars_count=repo["stars_count"]
        )
        session.add(top)
    session.commit()


def get_repos_data(repos_urls) -> list:
    data = []
    for counter, url in enumerate(repos_urls):
        print(f"{counter + 1}/{len(repos_urls)} organizations")
        repos = get_all_repos(url)
        for inner_counter, repo in enumerate(repos):
            # print(f"\t{inner_counter + 1}/{len(repos)} repositories")
            data.append({
                "id": repo["id"],
                "org_name": repo["owner"]["login"],
                "repo_name": repo["name"],
                "stars_count": repo["stargazers_count"]
            })
    return get_top(data, int(config["GitHub"]["top_number"]))


def get_all_repos(url) -> list:
    page = 1
    repos = []
    response = requests.get(url, headers=headers).json()
    while response:
        page += 1
        repos.extend(response)
        params = {"page": page}
        response = requests.get(url, params=params, headers=headers).json()
    return repos


def get_top(data, top_number):
    return sorted(data, key=lambda rd: rd["stars_count"], reverse=True)[:top_number]
