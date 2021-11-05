import aiohttp

from .api import GitHubAPI


class AsyncGitHubAPI(GitHubAPI):
    async def get(self, url: str, params=None):
        if params is None:
            params = {}

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url, params=params) as response:
                assert response.status == 200, f"{response.json()}"
                data = await response.json()

        return data
