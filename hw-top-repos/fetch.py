import requests

from secrets import ACCESS_TOKEN
from top import get_session, Top, drop_db

headers = {"Authorization": f"token {ACCESS_TOKEN}"}


def fetch():
    print("Data is taken from github:")
    repos_urls_with_id = _get_repos_urls(num_of_ors=200)
    repos_data = _get_repos_data(repos_urls_with_id.values())

    print("\nTop 20 repositories determined:")
    top_repos = sorted(repos_data, key=lambda rd: rd["stars_count"], reverse=True)[:20]

    print("\nLoading data into a database:")
    _load_repos_into_db(top_repos)


def _get_repos_urls(num_of_ors=100) -> dict:
    data = {}
    max_org = 100
    if num_of_ors < max_org:
        data.update(_get_given_num_of_repos_urls(per_page=num_of_ors))
    else:
        for _ in range(num_of_ors // max_org):
            data.update(_get_given_num_of_repos_urls(since=_get_since(data)))
        
        remainder = num_of_ors % max_org
        if remainder != 0:
            data.update(_get_given_num_of_repos_urls(per_page=remainder, since=_get_since(data)))
    return data


def _get_given_num_of_repos_urls(per_page=100, since=0) -> dict:
    params = {"per_page": per_page, "since": since}
    url = "https://api.github.com/organizations"
    response = requests.get(url, params=params, headers=headers).json()
    data = {org["id"]: org["repos_url"] for org in response}
    return data


def _get_since(dictionary) -> int:
    return 0 if len(dictionary) == 0 else list(dictionary.keys())[-1]


def _get_repos_data(repos_urls) -> list:
    data = []
    for counter, url in enumerate(repos_urls):
        print(f"{counter + 1}/{len(repos_urls)} organizations")
        repos = _get_all_repos(url)
        for inner_counter, repo in enumerate(repos):
            print(f"\t{inner_counter + 1}/{len(repos)} repositories")
            data.append({
                "id": repo["id"],
                "org_name": repo["owner"]["login"],
                "repo_name": repo["name"],
                "stars_count": repo["stargazers_count"]
            })
    return data


def _get_all_repos(url) -> list:
    page = 1
    repos = []
    response = requests.get(url, headers=headers).json()
    while response:
        page += 1
        repos.extend(response)
        params = {"page": page}
        response = requests.get(url, params=params, headers=headers).json()
    return repos


def _load_repos_into_db(repos):
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
    print("Done!")
