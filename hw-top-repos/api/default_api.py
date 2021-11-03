import requests

from .api import GitHubAPI


class DefaultGitHubAPI(GitHubAPI):
    def get(self, url: str, params=None):
        if params is None:
            params = {}

        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"{response.json()['message']}")
