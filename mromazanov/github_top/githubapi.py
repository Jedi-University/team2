import requests
import heapq


def get_repos(name, auth):
    global repo_stars, repo_names
    response_API = requests.get(f'https://api.github.com/orgs/{name}/repos', auth=auth).json()
    for repo in response_API:
        id = repo['id']
        name = repo['full_name']
        stars = repo['stargazers_count']
        repo_stars[id] = stars
        repo_names[id] = name
    return response_API


def get_names(orgs):
    names = []
    for entry in orgs:
        names.append(entry['login'])
    return names


def get_orgs(pages, auth):
    global last_id
    iteration = 0
    while iteration < pages:
        response_API = requests.get(f'https://api.github.com/organizations'
            f'?since={last_id}&per_page=100', auth=auth).json()
        last_id = response_API[-1]['id']
        iteration += 1
        yield response_API


def create_top(auth):
    global last_id, orgs, repo_names, repo_stars, repos
    for org in get_orgs(2, auth):
        orgs.extend(org)
    names = get_names(orgs)
    for name in names:
        repos.extend(get_repos(name, auth))
    repo_stars = heapq.nlargest(20, repo_stars.items(), key=lambda i: i[1])

    top_repos = []
    for repo in repo_stars:
        top_repos.append({'id':repo[0], 'org_name':repo_names[repo[0]].split('/')[0], 'repo_name':repo_names[repo[0]].split('/')[1], 'stars_count':repo[1]})

    last_id = 0
    orgs = []
    repo_stars = {}
    repo_names = {}
    repos = []
    return top_repos


last_id = 0
orgs = []
repo_stars = {}
repo_names = {}
repos = []
