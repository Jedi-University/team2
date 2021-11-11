from .worker import Worker


class RepoWorker(Worker):
    def __init__(self, api) -> None:
        super().__init__()
        self.type = '_'.join(['Repo', self.type])
        self.api = api

    def get_repos(self, org_name):
        page = 1
        repos = []
        while True:
            response = self.api.repos_request(org_name, page)
            response_API = response.json()
            for repo in response_API:
                try:
                    repos.append({'id':repo['id'],'name':repo['full_name'].split('/'),'stars':repo['stargazers_count']})
                except TypeError:
                    break
            page += 1
            if response.status_code == 503:
                print(response_API)
                exit()
            if (response.status_code == 404) or (response_API == []):
                break
        return repos


class AsyncRepoWorker(Worker):
    def __init__(self, api) -> None:
        super().__init__()
        self.type = '_'.join(['Async_Repo', self.type])
        self.api = api

    async def get_repos(self, org_name, repos):
        page = 1
        while True:
            response = await self.api.repos_request(org_name, page)
            for repo in response[1]:
                try:
                    repos.append({'id':repo['id'],'name':repo['full_name'].split('/'),'stars':repo['stargazers_count']})
                except TypeError:
                    break
            page += 1
            if (response[0] == 404) or (response[1] == []):
                break
        return repos