from WORKER.worker import Worker


class RepoWorker(Worker):
    def mapper(self, repo:dict):
        return {'id': repo['id'],
                'org_name': repo['owner']['login'],
                'repo_name': repo['name'],
                'stars': repo['stargazers_count']}

    def run(self, url:str):
        response = self.get_info(url)
        repos = list(map(self.mapper, response['json']))
        while 'next' in response:
            url = response['next']
            response = self.get_info(url)
            temp_repos = [self.mapper(repo) for repo in response['json']]
            repos.extend(temp_repos)
        return repos