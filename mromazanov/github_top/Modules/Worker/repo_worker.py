from ..API.API_request import repos_request


def get_repos(org_name):
    page = 1
    repos = []
    while True:
        response = repos_request(org_name, page)
        response_API = response.json()
        for repo in response_API:
            try:
                repos.append({'id':repo['id'],'name':repo['full_name'].split('/'),'stars':repo['stargazers_count']})
            except TypeError:
                break
        page += 1
        if (response.status_code == 404) or (response_API == []):
            break
    return repos