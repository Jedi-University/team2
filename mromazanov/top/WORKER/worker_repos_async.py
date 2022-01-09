from WORKER.worker_async import WorkerAsync


class AsyncRepoWorker(WorkerAsync):
    def repo_mapper(self, repo: dict) -> dict:
        return {'id': repo['id'],
                'org_name': repo['owner']['login'],
                'repo_name': repo['name'],
                'stars': repo['stargazers_count']}

    async def run(self, url: str) -> list:
        response = await self.get_api_response(url, per_page=self.per_page)
        repos = list(map(self.repo_mapper, response['json']))
        while 'url' in response:
            url = response['url']
            response = await self.get_api_response(url)
            cur_repos = map(self.repo_mapper, response['json'])
            repos.extend(cur_repos)
        repos = self.top_by_stars(repos)
        return repos