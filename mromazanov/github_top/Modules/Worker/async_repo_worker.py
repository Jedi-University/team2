from ..API.async_API_request import repos_request


async def get_repos(org_name, repos):
    page = 1
    while True:
        response = await repos_request(org_name, page)
        for repo in response[1]:
            try:
                repos.append({'id':repo['id'],'name':repo['full_name'].split('/'),'stars':repo['stargazers_count']})
            except TypeError:
                break
        page += 1
        if (response[0] == 404) or (response[1] == []):
            break
    return repos