from WORKER.worker import Worker

class OrgWorker(Worker):
    def run(self):
        url=f"https://api.github.com/organizations"
        response = self.get_info(url)
        orgs = response['json']
        while len(orgs) < self.orgs_count and 'next' in response:
            url = response['next']
            response = self.get_info(url)
            orgs.extend(response['json'])
        orgs = orgs[:self.orgs_count]
        repos_url = [org['repos_url'] for org in orgs]
        return repos_url

